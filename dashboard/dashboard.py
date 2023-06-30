import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import psycopg2

class GraphGenerator:
    def generate_graph(self):
        # Conectar ao banco de dados
        conn = psycopg2.connect(
            host="localhost",
            database="imagens-bd",
            user="airflow",
            password="airflow"
        )

        # Recuperar os dados do banco de dados
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, ultima_atualizacao FROM tabela_imagens")
        rows = cursor.fetchall()

        # Criar um DataFrame com os dados
        df = pd.DataFrame(rows, columns=['Codigo', 'Ultima_Atualizacao'])
        
        # Converter a coluna 'Ultima_Atualizacao' em formato de data
        df['Ultima_Atualizacao'] = pd.to_datetime(df['Ultima_Atualizacao'], format='%Y-%m-%d')

        df.sort_values(by='Ultima_Atualizacao', inplace=True)

        # Configurar o tamanho do gráfico
        plt.figure(figsize=(12, 6))

        # Plotar o gráfico de linha
        plt.plot(df['Ultima_Atualizacao'].dt.strftime('%Y-%m-%d'), df['Codigo'], marker='o')

        # Configurar o título e os rótulos dos eixos
        plt.title('Relação Código de Rastreamento x Última Atualização')
        plt.xlabel('Última Atualização')
        plt.ylabel('Código de Rastreamento')

        # Girar os rótulos do eixo x para melhor visualização
        plt.xticks(rotation=45)

        # Salvar o gráfico em um arquivo
        graph_file = 'graph.png'
        plt.savefig(graph_file, bbox_inches='tight')

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        return graph_file


class EmailSender:
    def send_email_with_graph(self, graph_file):
        # Configurar as informações de email
        remetente = 'guilherme.enviar.email@gmail.com'
        senha_remetente = 'zqfrwbqcelagcnkv'
        destinatario = 'gui.anonimo.correia@gmail.com'
        assunto = 'Gráfico de Linha - Relação Código de Rastreamento x Última Atualização'

        # Configurar o email
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Criar o corpo do email
        corpo_email = 'Olá,\n\nSegue em anexo o gráfico de linha com a relação Código de Rastreamento x Última Atualização.\n\n'
        msg.attach(MIMEText(corpo_email, 'plain'))

        # Anexar o gráfico ao email
        with open(graph_file, 'rb') as f:
            img_data = f.read()

        img_part = MIMEImage(img_data)
        img_part.add_header('Content-Disposition', 'attachment', filename=graph_file)
        msg.attach(img_part)

        # Enviar o email
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_smtp.starttls()
        servidor_smtp.login(remetente, senha_remetente)
        servidor_smtp.send_message(msg)
        servidor_smtp.quit()


# Utilizar as classes para gerar o gráfico e enviar o email
graph_generator = GraphGenerator()
graph_file = graph_generator.generate_graph()

email_sender = EmailSender()
email_sender.send_email_with_graph(graph_file)
