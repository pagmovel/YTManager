import streamlit as st
from models import Video, Playlist, Base
from youtube_manager import YouTubeManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuração do banco de dados
engine = create_engine('sqlite:///database/youtube.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Configuração do YouTube Manager
yt_manager = YouTubeManager()

def sync_playlists():
    """Sincroniza as playlists do YouTube com o banco de dados local."""
    if not hasattr(st.session_state, 'playlists_synced'):
        try:
            print("Sincronizando playlists...")
            playlists_response = yt_manager.get_playlists()
            for item in playlists_response.get('items', []):
                youtube_id = item['id']
                # Verifica se a playlist já existe no banco
                playlist = session.query(Playlist).filter_by(youtube_id=youtube_id).first()
                if not playlist:
                    playlist = Playlist(
                        title=item['snippet']['title'],
                        description=item['snippet'].get('description', ''),
                        youtube_id=youtube_id
                    )
                    session.add(playlist)
            session.commit()
            st.session_state.playlists_synced = True
            print("Playlists sincronizadas com sucesso!")
        except Exception as e:
            print(f"Erro ao sincronizar playlists: {str(e)}")

def init_youtube():
    if not hasattr(st.session_state, 'youtube'):
        try:
            st.session_state.youtube = yt_manager.authenticate()
            sync_playlists()  # Sincroniza playlists após autenticação
        except Exception as e:
            st.error(f"Erro de autenticação: {str(e)}")
            return False
    return True

def main():
    st.title("Gerenciador de Vídeos e Playlists do YouTube")
    
    if not init_youtube():
        return

    menu = st.sidebar.selectbox(
        "Menu",
        ["Playlists", "Vídeos em Rascunho", "Gerenciar Vídeos"]
    )

    if menu == "Playlists":
        st.header("Gerenciar Playlists")
        
        # Criar nova playlist
        with st.form("nova_playlist"):
            title = st.text_input("Título da Playlist")
            description = st.text_area("Descrição")
            if st.form_submit_button("Criar Playlist"):
                try:
                    response = yt_manager.create_playlist(title, description)
                    playlist = Playlist(
                        title=title,
                        description=description,
                        youtube_id=response['id']
                    )
                    session.add(playlist)
                    session.commit()
                    st.success("Playlist criada com sucesso!")
                    # Força nova sincronização
                    st.session_state.playlists_synced = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao criar playlist: {str(e)}")

        # Listar playlists
        st.subheader("Suas Playlists")
        playlists = session.query(Playlist).all()
        if not playlists:
            st.info("Nenhuma playlist encontrada. Crie uma nova playlist ou sincronize com o YouTube.")
        else:
            for playlist in playlists:
                with st.expander(f"📑 {playlist.title}"):
                    st.write(f"Descrição: {playlist.description}")
                    st.write(f"ID do YouTube: {playlist.youtube_id}")
                    videos = playlist.videos
                    if videos:
                        st.write("Vídeos na playlist:")
                        for idx, video in enumerate(videos, 1):
                            st.write(f"{idx}. {video.title}")

    elif menu == "Vídeos em Rascunho":
        st.header("Vídeos em Rascunho")
        
        # Inicializa o estado da sessão para vídeos selecionados se não existir
        if 'selected_videos' not in st.session_state:
            st.session_state.selected_videos = set()

        draft_videos = yt_manager.get_draft_videos()
        
        if not draft_videos:
            st.info("Nenhum vídeo em rascunho encontrado.")
        else:
            st.success(f"Encontrados {len(draft_videos)} vídeos em rascunho")
            
            playlists = session.query(Playlist).all()
            if playlists:
                # Configurações gerais para todos os vídeos
                st.write("### Configurações para todos os vídeos selecionados:")
                
                col1, col2 = st.columns(2)
                with col1:
                    made_for_kids = st.radio(
                        "Conteúdo para crianças?",
                        options=["Sim", "Não"],
                        index=1,  # "Não" como padrão
                        key="made_for_kids"
                    )
                
                with col2:
                    privacy_status = st.radio(
                        "Visibilidade do vídeo",
                        options=["Privado", "Não listado", "Público"],
                        index=1,  # "Não listado" como padrão
                        key="privacy_status"
                    )
                
                st.divider()
                
                # Seleção de playlist
                col1, col2 = st.columns([3, 1])
                with col1:
                    selected_playlist = st.selectbox(
                        "Selecione uma playlist",
                        options=playlists,
                        format_func=lambda x: x.title
                    )
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("Adicionar Selecionados"):
                        if len(st.session_state.selected_videos) > 0:
                            with st.spinner("Adicionando vídeos à playlist..."):
                                # Converte as opções para os valores esperados pela API
                                is_made_for_kids = made_for_kids == "Sim"
                                privacy_map = {
                                    "Privado": "private",
                                    "Não listado": "unlisted",
                                    "Público": "public"
                                }
                                
                                for video_id in st.session_state.selected_videos:
                                    try:
                                        # Encontra o vídeo completo na lista
                                        video_data = next(v for v in draft_videos if v['id'] == video_id)
                                        
                                        # Adiciona à playlist e atualiza configurações
                                        response = yt_manager.add_video_to_playlist_with_settings(
                                            selected_playlist.youtube_id,
                                            video_id,
                                            made_for_kids=is_made_for_kids,
                                            privacy_status=privacy_map[privacy_status]
                                        )
                                        
                                        # Atualiza banco de dados local
                                        video_obj = session.query(Video).filter_by(
                                            youtube_id=video_id
                                        ).first()
                                        if not video_obj:
                                            video_obj = Video(
                                                title=video_data['snippet']['title'],
                                                description=video_data['snippet']['description'],
                                                youtube_id=video_id
                                            )
                                            session.add(video_obj)
                                        if selected_playlist not in video_obj.playlists:
                                            video_obj.playlists.append(selected_playlist)
                                    except Exception as e:
                                        st.error(f"Erro ao adicionar vídeo {video_id}: {str(e)}")
                                
                                session.commit()
                                st.success(f"{len(st.session_state.selected_videos)} vídeos adicionados com sucesso!")
                                st.session_state.selected_videos = set()  # Limpa seleção
                                st.rerun()
                        else:
                            st.warning("Selecione pelo menos um vídeo primeiro.")
                
                # Lista de vídeos com checkboxes
                st.write("### Selecione os vídeos para adicionar:")
                for video in draft_videos:
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        with st.expander(f"📺 {video['snippet']['title']}"):
                            st.write(f"**Descrição:** {video['snippet'].get('description', 'Sem descrição')}")
                            st.write(f"**Data de publicação:** {video['snippet'].get('publishedAt', 'N/A')}")
                            if video['snippet'].get('thumbnails'):
                                thumbnail = video['snippet']['thumbnails'].get('medium', 
                                          video['snippet']['thumbnails'].get('default'))
                                if thumbnail:
                                    st.image(thumbnail['url'], use_column_width=True)
                    with col2:
                        # Checkbox para seleção do vídeo
                        if st.checkbox("Selecionar", key=f"select_{video['id']}", 
                                     value=video['id'] in st.session_state.selected_videos):
                            st.session_state.selected_videos.add(video['id'])
                        else:
                            st.session_state.selected_videos.discard(video['id'])
            else:
                st.warning("Crie uma playlist primeiro para poder adicionar vídeos.")

    elif menu == "Gerenciar Vídeos":
        st.header("Gerenciar Vídeos")
        videos = session.query(Video).all()
        
        if not videos:
            st.info("Nenhum vídeo gerenciado encontrado.")
        else:
            for video in videos:
                with st.expander(f"🎥 {video.title}"):
                    st.write(f"ID do YouTube: {video.youtube_id}")
                    st.write("Playlists:")
                    for playlist in video.playlists:
                        st.write(f"- {playlist.title}")

if __name__ == "__main__":
    main()