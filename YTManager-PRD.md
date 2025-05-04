# PRD: YTManager - Documento de Requisitos do Produto

## 1. Visão Geral do Produto

**Nome do Produto:** YTManager  
**Descrição:** Sistema de gerenciamento de vídeos e playlists do YouTube com interface web.  
**Plataforma:** Aplicação web baseada em Python/Streamlit.  
**Público-alvo:** Criadores de conteúdo do YouTube e gestores de canais.

## 2. Problema e Solução

### Problema
Criadores de conteúdo e gestores de canais do YouTube precisam de uma forma eficiente de gerenciar vídeos e playlists, especialmente ao trabalhar com vídeos privados (rascunhos) que precisam ser organizados antes da publicação.

### Solução
YTManager fornece uma interface unificada para:
- Gerenciar playlists do YouTube
- Visualizar e organizar vídeos em rascunho (privados)
- Adicionar vídeos às playlists de forma eficiente
- Sincronizar dados automaticamente com o YouTube

## 3. Requisitos Funcionais

### 3.1 Gestão de Playlists
- Visualizar lista de playlists existentes
- Criar novas playlists
- Editar playlists existentes
- Excluir playlists

### 3.2 Gestão de Vídeos
- Visualizar vídeos em rascunho (privados)
- Visualizar todos os vídeos do canal
- Adicionar vídeos às playlists
- Remover vídeos das playlists
- Visualizar informações detalhadas de cada vídeo

### 3.3 Sincronização
- Sincronização automática com a API do YouTube
- Cache local das informações em banco de dados SQLite

## 4. Requisitos Não-Funcionais

### 4.1 Técnicos
- Python 3.9 ou superior
- Integração com YouTube Data API v3
- Armazenamento em SQLite
- Interface web responsiva via Streamlit

### 4.2 Desempenho
- Respeitar limites de quota da API do YouTube (10.000 unidades diárias)
- Tempo de resposta aceitável para operações comuns

### 4.3 Segurança
- Autenticação OAuth2 com Google
- Armazenamento seguro de credenciais
- Escopo de permissões mínimo necessário

## 5. Arquitetura do Sistema

### 5.1 Componentes Principais
- **Interface Web:** Streamlit (src/app.py)
- **Gerenciador da API:** Módulo para interação com YouTube API (src/youtube_manager.py)
- **Modelos de Dados:** SQLAlchemy ORM (src/models.py)
- **Banco de Dados:** SQLite (database/youtube.db)

### 5.2 Fluxo de Dados
1. Autenticação do usuário com Google/YouTube
2. Sincronização inicial dos dados (playlists e vídeos)
3. Armazenamento local no SQLite
4. Operações do usuário na interface
5. Sincronização das alterações com o YouTube

## 6. Limitações e Restrições

- Dependência da disponibilidade da API do YouTube
- Limites de quota da API (custos por operação):
  - Listagem: 1 unidade
  - Operações de escrita: 50 unidades
  - Pesquisa: 100 unidades
  - Upload de vídeo: 1600 unidades
- Necessidade de credenciais válidas da API do YouTube

## 7. Implementação e Implantação

### 7.1 Requisitos de Instalação
- Ambiente Python com dependências instaladas
- Arquivo de credenciais da API do YouTube
- Opcional: Docker para implantação containerizada

### 7.2 Opções de Implantação
- Local (desenvolvimento): não usar Streamlit
- Containerizada: Via Docker

## 8. Cronograma e Marcos

### 8.1 Fase 1: Desenvolvimento Inicial (Concluída)
- Implementação da estrutura básica
- Integração com a API do YouTube
- Desenvolvimento da interface Streamlit

### 8.2 Fase 2: Melhorias (Em andamento)
- Otimização do uso de quotas da API
- Melhoria na interface do usuário
- Adição de recursos de automação

### 8.3 Fase 3: Expansões Futuras (Planejada)
- Estatísticas e análises de vídeos
- Integração com outras plataformas
- Suporte a múltiplos canais

## 9. Métricas de Sucesso

- Redução do tempo gasto em gerenciamento de playlists
- Minimização de erros na organização de vídeos
- Satisfação do usuário com a interface e funcionalidades

## 10. Escopo Explícito

### 10.1 Dentro do Escopo (IN)
- Gerenciamento de vídeos e playlists em um único canal do YouTube
- Interação com a API do YouTube para operações básicas de CRUD
- Interface para visualização e edição de metadados de vídeos
- Funcionalidades de arrastar e soltar para organização de playlists
- Armazenamento local de dados para reduzir chamadas à API
- Autenticação via OAuth2 com Google

### 10.2 Fora do Escopo (OUT)
- Upload de vídeos para o YouTube
- Edição de conteúdo de vídeo (corte, edição, etc.)
- Análise avançada de métricas e estatísticas
- Monetização ou gestão de anúncios
- Gestão de comentários ou interações com a comunidade
- Suporte para múltiplos canais em uma única instância

## 11. Funcionalidades Expressamente Não Incluídas

- **Não é um editor de vídeo:** O YTManager não possui capacidades de edição, corte ou modificação do conteúdo dos vídeos.
- **Não é uma ferramenta de análise:** Não fornece análises detalhadas de desempenho, métricas de audiência ou estatísticas avançadas.
- **Não é um substituto para o Studio do YouTube:** Não replica todas as funcionalidades do YouTube Studio, focando apenas na gestão de playlists e vídeos.
- **Não gerencia múltiplos canais simultaneamente:** Cada instância gerencia apenas um canal por vez.
- **Não automatiza publicações:** Não possui agendamento ou publicação automática de conteúdo.
- **Não processa áudio:** Não possui funcionalidades de transcrição, legendas ou processamento de áudio.

## 12. Glossário Técnico

- **API do YouTube:** YouTube Data API v3, interface de programação que permite acessar dados do YouTube.
- **OAuth2:** Protocolo de autorização que permite acesso seguro aos dados do usuário sem compartilhar credenciais.
- **Playlist:** Lista de reprodução contendo vídeos organizados em uma ordem específica.
- **CRUD:** Create, Read, Update, Delete - operações básicas de manipulação de dados.
- **SQLite:** Sistema de gerenciamento de banco de dados relacional embutido.
- **Quota:** Limite de uso da API do YouTube, medido em unidades de custo por operação.
- **Vídeo privado/rascunho:** Vídeo não listado ou privado, visível apenas para o proprietário da conta.
- **Sincronização:** Processo de atualização de dados entre o aplicativo local e o YouTube.
- **Interface web responsiva:** Interface que se adapta a diferentes tamanhos de tela e dispositivos.

## 13. FAQ - Perguntas Frequentes

### 13.1 Funcionalidades
**P:** O YTManager permite fazer upload de vídeos para o YouTube?  
**R:** Não, o upload de vídeos não está no escopo atual do projeto.

**P:** Posso gerenciar múltiplos canais do YouTube?  
**R:** Não, cada instância do YTManager gerencia apenas um canal do YouTube por vez.

**P:** O YTManager pode criar thumbnails para meus vídeos?  
**R:** Não, a criação de thumbnails não está incluída nas funcionalidades.

### 13.2 Técnicas
**P:** Quais são os requisitos de sistema para rodar o YTManager?  
**R:** Python 3.9+, as dependências listadas em requirements.txt, e Docker (opcional).

**P:** Como são armazenadas as credenciais da API?  
**R:** As credenciais são armazenadas localmente seguindo as práticas de segurança da OAuth2.

**P:** O YTManager funciona sem conexão com a internet?  
**R:** Parcialmente. Dados em cache podem ser visualizados, mas operações de modificação requerem conexão.

### 13.3 Limites e Restrições
**P:** Existe um limite para o número de playlists gerenciáveis?  
**R:** O limite é determinado pela API do YouTube, normalmente 200 playlists por canal.

**P:** O YTManager consome muitas unidades de quota da API?  
**R:** O sistema é otimizado para minimizar o uso de quota, utilizando cache local sempre que possível.

**P:** Posso usar o YTManager em ambientes de produção com alta demanda?  
**R:** O sistema é projetado principalmente para uso individual ou em pequena escala.

## 14. Modelo de Dados Detalhado

### 14.1 Esquema do Banco de Dados SQLite

#### Tabela: `playlists`
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | TEXT | ID da playlist no YouTube | Chave Primária |
| title | TEXT | Título da playlist | NOT NULL |
| description | TEXT | Descrição da playlist | |
| published_at | DATETIME | Data de publicação | |
| thumbnail_url | TEXT | URL da miniatura | |
| item_count | INTEGER | Número de vídeos na playlist | DEFAULT 0 |
| last_sync | DATETIME | Última sincronização | |

#### Tabela: `videos`
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | TEXT | ID do vídeo no YouTube | Chave Primária |
| title | TEXT | Título do vídeo | NOT NULL |
| description | TEXT | Descrição do vídeo | |
| published_at | DATETIME | Data de publicação | |
| thumbnail_url | TEXT | URL da miniatura | |
| duration | TEXT | Duração em formato ISO 8601 | |
| view_count | INTEGER | Contagem de visualizações | DEFAULT 0 |
| like_count | INTEGER | Contagem de likes | DEFAULT 0 |
| privacy_status | TEXT | Status de privacidade | |
| last_sync | DATETIME | Última sincronização | |

#### Tabela: `playlist_items`
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | TEXT | ID do item da playlist | Chave Primária |
| playlist_id | TEXT | ID da playlist | Chave Estrangeira → playlists.id |
| video_id | TEXT | ID do vídeo | Chave Estrangeira → videos.id |
| position | INTEGER | Posição na playlist | NOT NULL |
| added_at | DATETIME | Data de adição | |

### 14.2 Relacionamentos

- Uma **playlist** contém múltiplos **playlist_items**
- Um **vídeo** pode estar em múltiplos **playlist_items**
- Um **playlist_item** pertence a exatamente uma **playlist** e se refere a exatamente um **vídeo**

### 14.3 Tipos de Dados Específicos

- Todos os IDs são strings fornecidas pela API do YouTube
- As datas são armazenadas em formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- A duração dos vídeos segue o formato ISO 8601 (PT#H#M#S)
- O status de privacidade pode ser: "public", "private" ou "unlisted"

## 15. Endpoints da API do YouTube Utilizados

### 15.1 Autenticação e Escopo

- **Método de Autenticação:** OAuth2
- **Escopos Necessários:**
  - `https://www.googleapis.com/auth/youtube` (acesso total)
  - `https://www.googleapis.com/auth/youtube.readonly` (somente leitura)

### 15.2 Endpoints de Playlists

#### Listar Playlists do Canal
- **Endpoint:** `GET https://www.googleapis.com/youtube/v3/playlists`
- **Parâmetros principais:**
  - `part=snippet,contentDetails,status`
  - `mine=true`
  - `maxResults=50`
- **Custo de quota:** 1 unidade por requisição
- **Resposta:** Lista de objetos playlist

#### Obter Detalhes de uma Playlist
- **Endpoint:** `GET https://www.googleapis.com/youtube/v3/playlists`
- **Parâmetros principais:**
  - `part=snippet,contentDetails,status`
  - `id={playlistId}`
- **Custo de quota:** 1 unidade por requisição
- **Resposta:** Detalhes de uma única playlist

#### Criar Nova Playlist
- **Endpoint:** `POST https://www.googleapis.com/youtube/v3/playlists`
- **Parâmetros principais:**
  - `part=snippet,status`
- **Body JSON:** Contém title, description e privacyStatus
- **Custo de quota:** 50 unidades por requisição
- **Resposta:** Objeto playlist criado

#### Atualizar Playlist Existente
- **Endpoint:** `PUT https://www.googleapis.com/youtube/v3/playlists`
- **Parâmetros principais:**
  - `part=snippet,status`
- **Body JSON:** Contém id, title, description e privacyStatus
- **Custo de quota:** 50 unidades por requisição
- **Resposta:** Objeto playlist atualizado

#### Excluir Playlist
- **Endpoint:** `DELETE https://www.googleapis.com/youtube/v3/playlists`
- **Parâmetros principais:**
  - `id={playlistId}`
- **Custo de quota:** 50 unidades por requisição
- **Resposta:** HTTP 204 No Content

### 15.3 Endpoints de Vídeos

#### Listar Vídeos do Canal
- **Endpoint:** `GET https://www.googleapis.com/youtube/v3/videos`
- **Parâmetros principais:**
  - `part=snippet,contentDetails,statistics,status`
  - `myRating=like` ou `forMine=true`
  - `maxResults=50`
- **Custo de quota:** 1 unidade por requisição
- **Resposta:** Lista de objetos video

#### Obter Detalhes de um Vídeo
- **Endpoint:** `GET https://www.googleapis.com/youtube/v3/videos`
- **Parâmetros principais:**
  - `part=snippet,contentDetails,statistics,status`
  - `id={videoId}`
- **Custo de quota:** 1 unidade por requisição
- **Resposta:** Detalhes de um único vídeo

### 15.4 Endpoints de Itens de Playlist

#### Listar Itens de uma Playlist
- **Endpoint:** `GET https://www.googleapis.com/youtube/v3/playlistItems`
- **Parâmetros principais:**
  - `part=snippet,contentDetails,status`
  - `playlistId={playlistId}`
  - `maxResults=50`
- **Custo de quota:** 1 unidade por requisição
- **Resposta:** Lista de objetos playlistItem

#### Inserir Vídeo em Playlist
- **Endpoint:** `POST https://www.googleapis.com/youtube/v3/playlistItems`
- **Parâmetros principais:**
  - `part=snippet`
- **Body JSON:** Contém playlistId, resourceId (videoId) e position
- **Custo de quota:** 50 unidades por requisição
- **Resposta:** Objeto playlistItem criado

#### Atualizar Posição de Item na Playlist
- **Endpoint:** `PUT https://www.googleapis.com/youtube/v3/playlistItems`
- **Parâmetros principais:**
  - `part=snippet`
- **Body JSON:** Contém id, playlistId, resourceId e position
- **Custo de quota:** 50 unidades por requisição
- **Resposta:** Objeto playlistItem atualizado

#### Remover Item da Playlist
- **Endpoint:** `DELETE https://www.googleapis.com/youtube/v3/playlistItems`
- **Parâmetros principais:**
  - `id={playlistItemId}`
- **Custo de quota:** 50 unidades por requisição
- **Resposta:** HTTP 204 No Content

### 15.5 Limites e Paginação

- Todas as requisições que retornam listas suportam paginação
- Token de página (`pageToken`) deve ser usado para navegar através dos resultados
- Máximo de 50 itens por página em todas as requisições
- Limite diário de quota: 10.000 unidades por projeto

