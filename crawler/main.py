import datetime
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import psycopg2
from io import BytesIO
from PIL import Image
import pandas as pd
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


class ImageScraper:
    def __init__(self):
        self.driver = None

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Execute o Chrome no modo headless, sem interface gráfica
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-cookies")
        options.add_argument("--disable-local-storage")
        options.add_argument("--disable-session-storage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get('https://melhorrastreio.com.br/')

    def search_tracking_code(self, code):
        try:
            botutton = self.driver.find_element(By.XPATH, '//*[@id="cookiefirst-root"]/div/div/div[2]/div[2]/div[2]/div[2]/button')
            botutton.click()
        except:
            pass
        time.sleep(5)
        campo_busca = self.driver.find_element(By.XPATH, '//*[@id="tracking"]')
        campo_busca.clear()
        campo_busca.send_keys(code)
        campo_busca.send_keys(Keys.RETURN)
        time.sleep(5)

    def save_screenshot_and_send_to_database(self, code):
        time.sleep(5)
        try:
            botao = self.driver.find_element(By.XPATH, '//*[@id="cookiefirst-root"]/div/div/div[2]/div[2]/div[2]/div[2]/button')
            botao.click()
        except:
            pass
        elemento = self.driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/main/div/div')
        self.driver.execute_script("arguments[0].scrollIntoView();", elemento)
        
        # Verificar se o texto "Seu pacote saiu para entrega" está presente na página
        if "Seu pacote saiu para entrega" in self.driver.page_source:
            output_file = f"print_{code}.png"  # Nomear o arquivo com base no código de rastreamento
            self.driver.save_screenshot(output_file)

            # Enviar a imagem para o banco de dados
            self.send_image_to_database(code, output_file)
        last_update_date = self.get_last_update_date()
        if last_update_date:
            self.save_last_update_date_to_database(code, last_update_date)

    def close_driver(self):
        self.driver.quit()

    def send_image_to_database(self, code, output_file):
        global conn

        try:
            cursor = conn.cursor()

            with open(output_file, 'rb') as file:
                img = Image.open(file)
                byte_stream = BytesIO()
                img.save(byte_stream, format='PNG')
                byte_stream.seek(0)
                binary_data = byte_stream.read()

            cursor.execute("INSERT INTO tabela_imagens (codigo, imagem) VALUES (%s, %s)", (code, binary_data))

            conn.commit()
            print("Imagem enviada para o banco de dados com sucesso!")

        except (Exception, psycopg2.Error) as error:
            print("Erro ao enviar imagem para o banco de dados:", error)

        finally:
            if conn:
                cursor.close()

    def get_last_update_date(self):
        try:
            last_update_element = self.driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/main/div/div/form/div[4]/div/div')
            last_update_text = last_update_element.text.strip()

            # Extrair a data e hora da string usando expressões regulares
            match = re.search(r'(\d{2}/\d{2}/\d{4})\s+às\s+(\d{2}:\d{2})', last_update_text)
            if match:
                date_str = match.group(1)
                time_str = match.group(2)

                # Converter a data e hora para o formato correto
                last_update_date = datetime.datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
                print("Data da última atualização:", last_update_date.date())
                return last_update_date.date()

        except Exception as e:
            print("Erro ao obter a data da última atualização:", str(e))
        return None

    def save_last_update_date_to_database(self, code, last_update_date):
        global conn

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE tabela_imagens SET ultima_atualizacao = %s WHERE codigo = %s", (last_update_date, code))
            conn.commit()
            print("Data da última atualização salva no banco de dados com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao salvar a data da última atualização no banco de dados:", error)
        finally:
            if conn:
                cursor.close()

class EmailSender:
    def send_images_by_email(self):
        # Conectar ao banco de dados
        global conn
        conn = psycopg2.connect(
            host="localhost",
            database="imagens-bd",
            user="airflow",
            password="airflow"
        )
        cursor = conn.cursor()

        # Recuperar as imagens e datas de última atualização do banco de dados
        cursor.execute("SELECT codigo, imagem, ultima_atualizacao FROM tabela_imagens")
        rows = cursor.fetchall()

        # Configurar as informações de email
        remetente = 'guilherme.enviar.email@gmail.com'
        senha_remetente = 'zqfrwbqcelagcnkv'
        destinatario = 'gui.anonimo.correia@gmail.com'
        assunto = 'Imagens do Banco de Dados'

        # Configurar o email
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Criar o corpo do email
        corpo_email = 'Segue anexo as imagens do banco de dados:\n\n'

        for row in rows:
            codigo = row[0]
            imagem = row[1].tobytes()  # Converter o objeto BLOB em bytes
            ultima_atualizacao = row[2].strftime("%d/%m/%Y %H:%M")  # Converter a data em string

            # Criar um objeto MIMEImage com a imagem em bytes
            img_part = MIMEImage(imagem)

            # Definir o nome do arquivo da imagem
            img_part.add_header('Content-Disposition', 'attachment', filename='imagem_{}.png'.format(codigo))

            # Anexar a imagem ao email
            msg.attach(img_part)

            # Adicionar a data de última atualização ao corpo do email
            corpo_email += 'Código: {}\nÚltima atualização: {}\n\n'.format(codigo, ultima_atualizacao)

        # Adicionar o corpo do email à mensagem
        msg.attach(MIMEText(corpo_email, 'plain'))

        # Enviar o email
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_smtp.starttls()
        servidor_smtp.login(remetente, senha_remetente)
        servidor_smtp.send_message(msg)
        servidor_smtp.quit()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()


class ImageManager:
    def delete_images(self):
        # Conectar ao banco de dados
        global conn
        conn = psycopg2.connect(
            host="localhost",
            database="imagens-bd",
            user="airflow",
            password="airflow"
        )
        cursor = conn.cursor()

        # Executar a consulta para apagar as imagens
        cursor.execute("DELETE FROM tabela_imagens")

        # Confirmar as alterações no banco de dados
        conn.commit()

        # Fechar a conexão com o banco de dados
        cursor.close()


class Main:
    def __init__(self):
        global conn
        conn = psycopg2.connect(
            host="localhost",
            database="imagens-bd",
            user="airflow",
            password="airflow"
        )

    def run_scraper(self):
        scraper = ImageScraper()
        scraper.initialize_driver()

        df = pd.read_excel('rastreamento.xlsx')
        tracking_codes = df['Código de rastreamento'].tolist()

        for code in tracking_codes:
            scraper.search_tracking_code(code)
            scraper.save_screenshot_and_send_to_database(code)

        scraper.close_driver()

    def send_images_by_email(self):
        email_sender = EmailSender()
        email_sender.send_images_by_email()

    def delete_images(self):
        image_manager = ImageManager()
        image_manager.delete_images()

    def main(self):
        self.delete_images()
        self.run_scraper()
        self.send_images_by_email()


if __name__ == "__main__":
    main = Main()
    main.main()
