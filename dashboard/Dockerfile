# Use a base de imagem Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie o código para o contêiner
COPY . .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Defina o comando de execução
CMD [ "python", "dashboard.py" ]
