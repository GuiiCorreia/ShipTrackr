# ShipTrackr
Projeto de Automação usando Selenium e Docker

Este repositório contém scripts em Python para coletar dados de rastreamento de um site, salvar capturas de tela e dados em um banco de dados PostgreSQL, gerar gráficos e enviar notificações por e-mail.

## Requisitos

- Python 3.x
- Selenium
- ChromeDriverManager
- psycopg2
- PIL (Biblioteca Python Imaging)
- pandas
- matplotlib

## Pesquisa do codigo de rastreamento

A classe `ImageScraper` utiliza o Selenium para coletar dados de rastreamento de um site, salvar capturas de tela e enviar dados para um banco de dados PostgreSQL.

- `initialize_driver()`: Inicializa o Chrome WebDriver.
- `search_tracking_code(code)`: Procura pelo código de rastreamento no site.
- `save_screenshot_and_send_to_database(code)`: Salva uma captura de tela e a envia para o banco de dados.
- `close_driver()`: Fecha o WebDriver.

## Remetente de E-mail

A classe `EmailSender` envia notificações por e-mail com imagens anexadas do banco de dados.

- `send_images_by_email()`: Envia notificações por e-mail com imagens anexadas.

## Gerenciador de Imagens

A classe `ImageManager` exclui imagens do banco de dados.

- `delete_images()`: Exclui imagens do banco de dados.

## Principal

A classe `Main` orquestra a coleta de dados, o envio de notificações por e-mail e o gerenciamento de imagens.

- `run_scraper()`: Executa o coletor de imagens.
- `send_images_by_email()`: Envia notificações por e-mail com imagens anexadas.
- `delete_images()`: Exclui imagens do banco de dados.
- `main()`: Função principal para executar todo o processo.

## Gerador de Gráficos

A classe `GraphGenerator` gera um gráfico de linhas a partir dos dados no banco de dados PostgreSQL.

- `generate_graph()`: Gera um gráfico de linhas com dados de rastreamento.
- `send_email_with_graph(graph_file)`: Envia um e-mail com o gráfico como anexo.

## Uso

1. Instale as dependências necessárias usando `pip install -r requirements.txt`.
2. Atualize as credenciais do banco de dados no código.
3. Execute a classe `Main` para realizar a coleta de dados, gerar gráficos e enviar notificações por e-mail.

## Observação

Como inciar a atomação:

Primeiro de tudo, voce deve preparar seu servidor Postgree para poder salvar as informações coletadas 
pelas automações. Isso pode ser configurado dentro da pasta *Servidor* no arquivo *docker-compose.yaml*.

Lá você pode configurar o host, password e o nome do seu banco de dados para iniciar ele. Com o servidor
iniciado, será necessario fazer as crações das tabelas, mas isso voce pode resolver por meio desse comando sql:

- -- Criação da tabela "tabela_imagens"
- CREATE TABLE tabela_imagens (
    - id SERIAL PRIMARY KEY,
    - codigo VARCHAR(255) NOT NULL,
    - imagem BYTEA,
    - ultima_atualizacao TIMESTAMP
- );

O resultado esperado é essa mensagem: *CREATE TABLE - Query returned successfully in 50 msec* ou algo parecido.





