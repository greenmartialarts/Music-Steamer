import os
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tracks")
def get_tracks(db: Session = Depends(get_db)):
    return db.query(models.Track).all()

@app.get("/albums")
def get_albums(db: Session = Depends(get_db)):
    albums = db.query(models.Track.album).distinct().all()
    return [a[0] for a in albums]

@app.get("/artists")
def get_artists(db: Session = Depends(get_db)):
    artists = db.query(models.Track.artist).distinct().all()
    return [a[0] for a in artists]

@app.get("/track/{track_id}")
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

def send_bytes_range_requests(
    file_path: str, range_header: str, content_type: str
):
    file_size = os.stat(file_path).st_size
    range_header = range_header.strip().strip("bytes=")
    range_start, range_end = range_header.split("-")

    start = int(range_start)
    end = int(range_end) if range_end else file_size - 1

    if start >= file_size:
        raise HTTPException(status_code=416, detail="Requested Range Not Satisfiable")

    chunk_size = (end - start) + 1

    def iterfile():
        with open(file_path, "rb") as f:
            f.seek(start)
            remaining = chunk_size
            while remaining > 0:
                chunk = f.read(min(remaining, 64 * 1024)) # 64KB chunks
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": content_type,
    }
    return StreamingResponse(iterfile(), status_code=206, headers=headers)

@app.get("/stream/{track_id}")
def stream_track(track_id: int, request: Request, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    file_path = track.path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    content_type = "audio/mpeg"
    if file_path.endswith(".flac"):
        content_type = "audio/flac"
    elif file_path.endswith(".wav"):
        content_type = "audio/wav"

    range_header = request.headers.get("range")
    if range_header:
        return send_bytes_range_requests(file_path, range_header, content_type)

    return FileResponse(file_path, media_type=content_type)

# Playlists API
class PlaylistCreate(BaseModel):
    name: str

@app.post("/playlists")
def create_playlist(playlist_data: PlaylistCreate, db: Session = Depends(get_db)):
    db_playlist = models.Playlist(name=playlist_data.name)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@app.get("/playlists")
def get_playlists(db: Session = Depends(get_db)):
    return db.query(models.Playlist).all()

@app.post("/playlists/{playlist_id}/add/{track_id}")
def add_to_playlist(playlist_id: int, track_id: int, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    # Get max order
    max_order = db.query(models.PlaylistTrack).filter(models.PlaylistTrack.playlist_id == playlist_id).count()

    pt = models.PlaylistTrack(playlist_id=playlist_id, track_id=track_id, order=max_order)
    db.add(pt)
    db.commit()
    return {"message": "Track added to playlist"}

@app.get("/playlists/{playlist_id}")
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    tracks = db.query(models.Track).join(models.PlaylistTrack).filter(models.PlaylistTrack.playlist_id == playlist_id).order_by(models.PlaylistTrack.order).all()
    return {"id": playlist.id, "name": playlist.name, "tracks": tracks}
