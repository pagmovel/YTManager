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
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"
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
        
        # Prepara o body com as partes que serão atualizadas
        body = {
            "id": video_id,
            "status": {},
            "snippet": {}
        }
        
        parts = []
        
        if made_for_kids is not None:
            body["status"]["madeForKids"] = made_for_kids
            parts.append("status")
            
        if privacy_status:
            body["status"]["privacyStatus"] = privacy_status
            if "status" not in parts:
                parts.append("status")
        
        if not parts:
            return None  # Nada para atualizar
            
        request = youtube.videos().update(
            part=",".join(parts),
            body=body
        )
        return request.execute()

    def add_video_to_playlist_with_settings(self, playlist_id, video_id, position=0, 
                                          made_for_kids=None, privacy_status=None):
        """Adiciona um vídeo à playlist e atualiza suas configurações."""
        # Primeiro adiciona à playlist
        playlist_response = self.add_video_to_playlist(playlist_id, video_id, position)
        
        # Depois atualiza as configurações do vídeo
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