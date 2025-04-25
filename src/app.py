from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import Video, Playlist, Base
from youtube_manager import YouTubeManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.secret_key = os.urandom(24)

# Configuração do banco de dados
engine = create_engine('sqlite:///database/youtube.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Configuração do YouTube Manager
yt_manager = YouTubeManager()

# Filtro para formatar datas
@app.template_filter('datetime')
def format_datetime(value):
    if not value:
        return ""
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return dt.strftime('%d/%m/%Y %H:%M')

@app.before_request
def before_request():
    if not hasattr(app, 'youtube'):
        try:
            app.youtube = yt_manager.authenticate()
            sync_playlists()
        except Exception as e:
            flash(f"Erro de autenticação: {str(e)}", "error")

def sync_playlists():
    """Sincroniza as playlists do YouTube com o banco de dados local."""
    try:
        playlists_response = yt_manager.get_playlists()
        for item in playlists_response.get('items', []):
            youtube_id = item['id']
            playlist = session.query(Playlist).filter_by(youtube_id=youtube_id).first()
            if not playlist:
                playlist = Playlist(
                    title=item['snippet']['title'],
                    description=item['snippet'].get('description', ''),
                    youtube_id=youtube_id
                )
                session.add(playlist)
        session.commit()
    except Exception as e:
        flash(f"Erro ao sincronizar playlists: {str(e)}", "error")

@app.route('/')
def index():
    # return redirect(url_for('videos'))
    return render_template('index.html', playlists=playlists)

@app.route('/playlists')
def playlists():
    playlists = session.query(Playlist).all()
    return render_template('playlists.html', playlists=playlists)

@app.route('/videos')
def videos():
    draft_videos = yt_manager.get_draft_videos()
    playlists = session.query(Playlist).all()
    
    # Se uma playlist foi selecionada, busca seus vídeos
    selected_playlist_id = request.args.get('playlist_id')
    playlist_videos = []
    if selected_playlist_id:
        playlist_videos = yt_manager.get_playlist_videos(selected_playlist_id)
    
    return render_template('videos.html', 
                         draft_videos=draft_videos,
                         playlists=playlists,
                         playlist_videos=playlist_videos,
                         selected_playlist_id=selected_playlist_id)

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    try:
        video_ids = request.form.get('video_ids', '').split(',')
        playlist_id = request.form.get('playlist_id')
        made_for_kids = request.form.get('made_for_kids') == 'true'
        privacy_status = request.form.get('privacy_status', 'unlisted')
        insert_position = request.form.get('insert_position', 'end')
        after_video_position = int(request.form.get('after_video_position', 0))
        
        if not video_ids or not playlist_id:
            flash("Por favor, selecione os vídeos e a playlist.", "error")
            return redirect(url_for('videos'))
            
        # Obtém a lista de vídeos atual da playlist
        existing_videos = yt_manager.get_playlist_videos(playlist_id)
        existing_video_ids = {v['id'] for v in existing_videos} if existing_videos else set()
        
        # Filtra vídeos que já existem na playlist
        new_video_ids = [vid for vid in video_ids if vid not in existing_video_ids]
        
        if not new_video_ids:
            flash("Todos os vídeos selecionados já existem na playlist.", "warning")
            return redirect(url_for('videos'))
        
        # Determina a posição inicial baseado na escolha do usuário
        if insert_position == 'start':
            starting_position = 0
        elif insert_position == 'after':
            starting_position = after_video_position + 1
        else:  # 'end'
            starting_position = len(existing_videos) if existing_videos else 0
            
        # Adiciona os vídeos à playlist
        for idx, video_id in enumerate(new_video_ids):
            response = yt_manager.add_video_to_playlist_with_settings(
                playlist_id,
                video_id,
                position=starting_position + idx,
                made_for_kids=made_for_kids,
                privacy_status=privacy_status
            )
            
            # Atualiza o banco de dados local
            video_data = next(v for v in yt_manager.get_draft_videos() if v['id'] == video_id)
            video_obj = session.query(Video).filter_by(youtube_id=video_id).first()
            if not video_obj:
                video_obj = Video(
                    title=video_data['snippet']['title'],
                    description=video_data['snippet']['description'],
                    youtube_id=video_id
                )
                session.add(video_obj)
            
            playlist = session.query(Playlist).filter_by(youtube_id=playlist_id).first()
            if playlist and playlist not in video_obj.playlists:
                video_obj.playlists.append(playlist)
        
        session.commit()
        flash(f"{len(new_video_ids)} vídeos adicionados com sucesso!", "success")
        
    except Exception as e:
        flash(f"Erro ao adicionar vídeos: {str(e)}", "error")
    
    return redirect(url_for('videos', playlist_id=playlist_id))

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    try:
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        if not title:
            flash("O título da playlist é obrigatório.", "error")
            return redirect(url_for('playlists'))
            
        # Cria a playlist no YouTube
        response = yt_manager.create_playlist(title, description)
        
        # Adiciona ao banco de dados local
        playlist = Playlist(
            title=title,
            description=description,
            youtube_id=response['id']
        )
        session.add(playlist)
        session.commit()
        
        flash("Playlist criada com sucesso!", "success")
        
    except Exception as e:
        flash(f"Erro ao criar playlist: {str(e)}", "error")
        
    return redirect(url_for('playlists'))

if __name__ == '__main__':
    app.run(debug=True)