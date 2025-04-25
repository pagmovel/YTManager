from sqlalchemy import create_engine, Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Tabela de associação entre vídeos e playlists
video_playlist = Table(
    'video_playlist',
    Base.metadata,
    Column('video_id', Integer, ForeignKey('videos.id')),
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('order', Integer)
)

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(5000))
    youtube_id = Column(String(20), unique=True)
    is_draft = Column(Boolean, default=True)
    playlists = relationship("Playlist", secondary=video_playlist, back_populates="videos")

class Playlist(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(5000))
    youtube_id = Column(String(20), unique=True)
    videos = relationship("Video", secondary=video_playlist, back_populates="playlists")