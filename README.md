# YTManager - Gerenciador de Vídeos e Playlists do YouTube

Sistema de gerenciamento de vídeos e playlists do YouTube com interface web, desenvolvido com Python, Streamlit e YouTube Data API v3.

## Funcionalidades

- 📝 Criar e gerenciar playlists do YouTube
- 📺 Visualizar vídeos em rascunho (privados)
- 📋 Adicionar vídeos às playlists
- 🔄 Sincronização automática com o YouTube
- 💾 Armazenamento local das informações em SQLite

## Pré-requisitos

- Python 3.9 ou superior
- Credenciais da API do YouTube (veja a seção de configuração)
- Docker (opcional, para execução em container)

## Instalação

1. Clone o repositório:

```bash
git clone <seu-repositorio>
cd YTManager
```

2. Crie um ambiente virtual (recomendado):

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

- Windows:

```bash
venv\Scripts\activate
```

- Linux/Mac:

```bash
source venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

1. Configure as credenciais do YouTube seguindo as instruções em `config/INSTRUCOES_CREDENCIAIS.md`
2. Coloque o arquivo `client_secrets.json` na pasta `config/`

## Execução

1. Com o ambiente virtual ativado, execute:

```bash
streamlit run src/app.py
```

2. Acesse a interface web através do navegador (normalmente http://localhost:8501)

### Execução com Docker (opcional)

1. Construa a imagem:

```bash
docker build -t ytmanager .
```

2. Execute o container:

```bash
docker run -p 8501:8501 -v $(pwd)/config:/app/config -v $(pwd)/database:/app/database ytmanager
```

## Estrutura do Projeto

```
YTManager/
├── config/
│   ├── client_secrets.json     # Credenciais da API (não versionado)
│   ├── credentials.pickle      # Cache de autenticação (não versionado)
│   └── INSTRUCOES_CREDENCIAIS.md
├── database/
│   └── youtube.db             # Banco de dados SQLite
├── src/
│   ├── app.py                 # Aplicação Streamlit
│   ├── models.py             # Modelos SQLAlchemy
│   └── youtube_manager.py    # Gerenciador da API do YouTube
├── requirements.txt          # Dependências do projeto
├── README.md
└── .gitignore
```

## Dependências Principais

- `streamlit`: Interface web
- `google-api-python-client`: Cliente da API do YouTube
- `google-auth-oauthlib`: Autenticação OAuth2
- `sqlalchemy`: ORM para banco de dados

## Uso

1. Na primeira execução, você será redirecionado para autenticar com sua conta do Google
2. O sistema possui três seções principais:
   - **Playlists**: Criar e visualizar playlists
   - **Vídeos em Rascunho**: Visualizar vídeos privados e adicionar às playlists
   - **Gerenciar Vídeos**: Visualizar todos os vídeos e suas playlists associadas

## Quotas e Limites

- A API do YouTube possui uma quota diária de 10.000 unidades
- Custos principais:
  - Listagem de recursos: 1 unidade
  - Operações de gravação: 50 unidades
  - Pesquisa: 100 unidades
  - Upload de vídeo: 1600 unidades

## Solução de Problemas

Se encontrar problemas de autenticação:

1. Verifique se o arquivo `client_secrets.json` está na pasta `config/`
2. Certifique-se de que seu email está na lista de usuários de teste
3. Confirme que a API do YouTube está ativada no Console do Google Cloud
4. Delete o arquivo `credentials.pickle` para forçar uma nova autenticação

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT.
