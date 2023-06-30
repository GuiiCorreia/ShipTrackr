# ShipTrackr
Projeto de Automação usando Selenium e Docker


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

Feito tudo isso, agora seguiremos esses passos: 
- Agora partimos para a pasta *Crawler*, onde vamos inserir os codigos de rastreamento dos Correios
que queremos fazer o monitoramento dentro do arquivo *xlms*. Seguir como exemplo os codigos que deixei lá, apenas substituindo.
- Após isso, no arquivo *Main.py* vamos atualizar as informações do banco de dados, tendo em vista que devem ser os
mesmos usados na configuração do banco de dados, linhas: "
