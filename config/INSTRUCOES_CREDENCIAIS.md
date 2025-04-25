# Configuração das Credenciais do YouTube

## 1. Acesse o Google Cloud Console

1. Vá para https://console.cloud.google.com
2. Faça login com sua conta Google

## 2. Crie um Novo Projeto

1. Na barra superior, clique no seletor de projetos
2. Clique em "Novo Projeto"
3. Nome do projeto: YTManager (ou outro nome de sua escolha)
4. Clique em "Criar"

## 3. Habilite a API do YouTube

1. No menu lateral, vá em "APIs e Serviços" > "APIs e serviços ativados"
2. Clique em "+ ATIVAR APIS E SERVIÇOS"
3. Na barra de pesquisa, digite "YouTube Data API v3"
4. Clique na API do YouTube quando aparecer
5. Clique em "ATIVAR"

## 4. Configure a Tela de Consentimento OAuth

1. No menu lateral, clique em "APIs e Serviços" > "Tela de consentimento OAuth"
2. Selecione "Externo" como tipo de usuário e clique em "CRIAR"
3. Preencha as informações obrigatórias:
   - Nome do app: YTManager
   - Email do suporte ao usuário: seu email
   - Logo do app: opcional
   - Domínio do app: pode deixar em branco
   - Email para contato do desenvolvedor: seu email
4. Clique em "SALVAR E CONTINUAR"
5. Na seção "Escopos", clique em "ADICIONAR OU REMOVER ESCOPOS"
6. Selecione os seguintes escopos:
   - `https://www.googleapis.com/auth/youtube.force-ssl`
   - `https://www.googleapis.com/auth/youtube.upload`
7. Clique em "ATUALIZAR"
8. Clique em "SALVAR E CONTINUAR"
9. Na seção "Usuários de teste":
   - Clique em "ADICIONAR USUÁRIOS"
   - Adicione seu email
   - **IMPORTANTE**: Durante o desenvolvimento, apenas emails adicionados aqui poderão usar o aplicativo
10. Clique em "SALVAR E CONTINUAR"
11. Revise todas as configurações e clique em "VOLTAR AO PAINEL"

## 5. Crie as Credenciais OAuth

1. No menu lateral, vá em "APIs e Serviços" > "Credenciais"
2. Clique em "CRIAR CREDENCIAIS" > "ID do Cliente OAuth"
3. Em "Tipo de aplicativo", selecione "Aplicativo para Desktop"
4. Digite um nome para o aplicativo (ex: "YTManager Desktop")
5. Clique em "CRIAR"
6. Na janela que aparecer, clique em "FAZER DOWNLOAD" para baixar o arquivo JSON com as credenciais
7. **IMPORTANTE**: Este arquivo contém suas credenciais privadas, não compartilhe ou commite ele no repositório

## 6. Configure no Projeto

1. Renomeie o arquivo JSON baixado para `client_secrets.json`
2. Mova o arquivo para a pasta `config/` deste projeto

## Observações Importantes

- Na primeira execução, o navegador abrirá pedindo autorização
- Como você está em modo de teste, apenas os emails adicionados como "Usuários de teste" poderão autenticar
- A cota padrão é de 10.000 unidades por dia. Principais custos de quota:
  - Listagem de recursos: 1 unidade
  - Operações de gravação: 50 unidades
  - Pesquisa: 100 unidades
  - Upload de vídeo: 1600 unidades
- Se tiver problemas, verifique se:
  - A API do YouTube está ativada
  - Os escopos foram adicionados corretamente
  - Seu email está na lista de usuários de teste
  - O arquivo client_secrets.json está na pasta config/
