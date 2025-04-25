from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

class YouTubeManager:
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/youtube.upload'
        ]
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.CLIENT_SECRETS_FILE = 'config/client_secrets.json'
        self.CREDENTIALS_FILE = 'config/credentials.pickle'
        self.youtube = None
        # Tentar autenticar na inicialização
        self.authenticate()

    def authenticate(self):
        """Autenticar e construir o serviço do YouTube."""
        if self.youtube is not None:
            return self.youtube

        credentials = None
        if os.path.exists(self.CREDENTIALS_FILE):
            print("Carregando credenciais do arquivo...")
            with open(self.CREDENTIALS_FILE, 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Atualizando token expirado...")
                credentials.refresh(Request())
            else:
                print("Obtendo novas credenciais...")
                if not os.path.exists(self.CLIENT_SECRETS_FILE):
                    raise FileNotFoundError(
                        f"Arquivo {self.CLIENT_SECRETS_FILE} não encontrado. "
                        "Por favor, siga as instruções em INSTRUCOES_CREDENCIAIS.md"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRETS_FILE, self.SCOPES)
                credentials = flow.run_local_server(port=0)

            with open(self.CREDENTIALS_FILE, 'wb') as token:
                pickle.dump(credentials, token)

        print("Construindo serviço do YouTube...")
        self.youtube = build(
            self.API_SERVICE_NAME, 
            self.API_VERSION, 
            credentials=credentials,
            cache_discovery=False  # Evita warnings de cache
        )
        return self.youtube

    def _ensure_youtube_client(self):
        """Garante que o cliente do YouTube está autenticado e disponível."""
        if self.youtube is None:
            self.authenticate()
        return self.youtube

    def get_draft_videos(self):
        """Obtém os vídeos em rascunho (privados) do usuário autenticado."""
        youtube = self._ensure_youtube_client()
        
        try:
            # Primeiro, obtém o ID do canal do usuário autenticado
            print("Buscando canal do usuário...")
            channels_response = youtube.channels().list(
                part="id,snippet",
                mine=True
            ).execute()
            
            if not channels_response.get('items'):
                print("Nenhum canal encontrado para o usuário autenticado")
                return []
                
            channel_id = channels_response['items'][0]['id']
            channel_title = channels_response['items'][0]['snippet']['title']
            print(f"Canal encontrado: {channel_title} (ID: {channel_id})")
            
            # Busca diretamente os vídeos usando uploads playlist
            print("Buscando playlist de uploads do canal...")
            playlist_response = youtube.channels().list(
                part="contentDetails",
                id=channel_id
            ).execute()
            
            if not playlist_response.get('items'):
                print("Nenhuma playlist de uploads encontrada")
                return []
                
            uploads_playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            print(f"Playlist de uploads ID: {uploads_playlist_id}")
            
            # Busca os vídeos da playlist de uploads
            print("Buscando vídeos...")
            playlistitems_response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50
            ).execute()
            
            if not playlistitems_response.get('items'):
                print("Nenhum vídeo encontrado na playlist de uploads")
                return []
                
            # Coleta os IDs dos vídeos
            video_ids = [item['contentDetails']['videoId'] 
                        for item in playlistitems_response.get('items', [])]
            
            if not video_ids:
                print("Nenhum ID de vídeo encontrado")
                return []
                
            print(f"Encontrados {len(video_ids)} vídeos. Buscando detalhes...")
            
            # Obtém detalhes completos dos vídeos, incluindo status
            videos_response = youtube.videos().list(
                part="snippet,status",
                id=','.join(video_ids)
            ).execute()
            
            # Filtra apenas os vídeos privados
            private_videos = [
                video for video in videos_response.get('items', [])
                if video['status']['privacyStatus'] == 'private'
            ]
            
            print(f"Encontrados {len(private_videos)} vídeos privados")
            return private_videos
            
        except Exception as e:
            print(f"Erro ao buscar vídeos: {str(e)}")
            return []

    def create_playlist(self, title, description=""):
        youtube = self._ensure_youtube_client()
        request = youtube.playlists().insert(
            part="snippet,status,contentDetails",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"
                },
                "contentDetails": {
                    "sortManually": True
                }
            }
        )
        return request.execute()

    def add_video_to_playlist(self, playlist_id, video_id, position=0):
        youtube = self._ensure_youtube_client()
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "position": position,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        return request.execute()

    def get_playlists(self):
        youtube = self._ensure_youtube_client()
        request = youtube.playlists().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50
        )
        return request.execute()

    def update_video_settings(self, video_id, made_for_kids=None, privacy_status=None):
        """Atualiza as configurações de um vídeo."""
        youtube = self._ensure_youtube_client()
        
        # Primeiro obtém as configurações atuais do vídeo
        current_video = youtube.videos().list(
            part="status",
            id=video_id
        ).execute()
        
        if not current_video.get('items'):
            raise Exception(f"Vídeo {video_id} não encontrado")
            
        # Prepara o body com as partes que serão atualizadas
        body = {
            "id": video_id,
            "status": current_video['items'][0]['status']
        }
        
        # Atualiza apenas os campos necessários
        if made_for_kids is not None:
            body["status"]["madeForKids"] = made_for_kids
            
        if privacy_status:
            body["status"]["privacyStatus"] = privacy_status
            
        request = youtube.videos().update(
            part="status",  # Usando apenas a parte 'status'
            body=body
        )
        return request.execute()

    def set_playlist_manual_sorting(self, playlist_id):
        """Configura a playlist para usar ordenação manual."""
        youtube = self._ensure_youtube_client()
        request = youtube.playlists().update(
            part="id,contentDetails",
            body={
                "id": playlist_id,
                "contentDetails": {
                    "sortManually": True
                }
            }
        )
        return request.execute()

    def reorder_playlist_item(self, playlist_id, item_id, new_position):
        """Reordena um item específico na playlist."""
        youtube = self._ensure_youtube_client()
        request = youtube.playlistItems().update(
            part="snippet",
            body={
                "id": item_id,
                "snippet": {
                    "playlistId": playlist_id,
                    "position": new_position
                }
            }
        )
        return request.execute()
        
    def add_video_to_playlist_with_settings(self, playlist_id, video_id, position=0, 
                                          made_for_kids=None, privacy_status=None):
        """Adiciona um vídeo à playlist e atualiza suas configurações."""
        # Primeiro configura a playlist para ordenação manual
        try:
            self.set_playlist_manual_sorting(playlist_id)
            
            # Se estamos adicionando em uma posição específica, precisamos buscar os itens existentes
            if position > 0:
                existing_items = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50
                ).execute()
                
                # Adiciona o novo vídeo na posição desejada
                playlist_response = self.add_video_to_playlist(playlist_id, video_id, position)
                
                # Reordena os itens existentes se necessário
                if existing_items.get('items'):
                    for idx, item in enumerate(existing_items['items']):
                        if idx >= position:
                            try:
                                self.reorder_playlist_item(playlist_id, item['id'], idx + 1)
                            except Exception as e:
                                print(f"Aviso: Erro ao reordenar item {item['id']}: {str(e)}")
            else:
                # Adiciona normalmente se for no início ou fim
                playlist_response = self.add_video_to_playlist(playlist_id, video_id, position)
            
        except Exception as e:
            print(f"Aviso: Não foi possível configurar ordenação manual: {str(e)}")
            playlist_response = self.add_video_to_playlist(playlist_id, video_id, position)
        
        # Atualiza as configurações do vídeo
        if made_for_kids is not None or privacy_status:
            video_response = self.update_video_settings(
                video_id, 
                made_for_kids=made_for_kids, 
                privacy_status=privacy_status
            )
            return {
                "playlist": playlist_response,
                "video": video_response
            }
        return {"playlist": playlist_response}

    def get_playlist_videos(self, playlist_id):
        """Obtém todos os vídeos de uma playlist."""
        youtube = self._ensure_youtube_client()
        
        try:
            # Busca os vídeos da playlist
            videos = []
            next_page_token = None
            
            while True:
                request = youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                if not response.get('items'):
                    break
                    
                # Coleta os IDs dos vídeos
                video_ids = [item['contentDetails']['videoId'] 
                           for item in response.get('items', [])]
                
                if video_ids:
                    # Obtém detalhes completos dos vídeos
                    videos_response = youtube.videos().list(
                        part="snippet,status",
                        id=','.join(video_ids)
                    ).execute()
                    
                    videos.extend(videos_response.get('items', []))
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            return videos
            
        except Exception as e:
            print(f"Erro ao buscar vídeos da playlist: {str(e)}")
            return []