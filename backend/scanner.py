import os
from mutagen import File
from sqlalchemy.orm import Session
from .models import Track
from .database import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

SUPPORTED_EXTENSIONS = ('.mp3', '.flac', '.wav')

def scan_music_folder(folder_path: str):
    db = SessionLocal()
    try:
        # Clear existing tracks for simplicity in this version,
        # or we could do a smart update.
        # For now, let's just add new ones or update.

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(SUPPORTED_EXTENSIONS):
                    file_path = os.path.join(root, file)

                    # Check if already in DB
                    existing_track = db.query(Track).filter(Track.path == file_path).first()
                    if existing_track:
                        continue

                    try:
                        audio = File(file_path)
                        if audio is None:
                            continue

                        title = file
                        artist = "Unknown"
                        album = "Unknown"

                        if audio.tags:
                            # Try common tag names for different formats
                            if 'TIT2' in audio.tags: title = str(audio.tags['TIT2'])
                            elif 'title' in audio.tags: title = str(audio.tags['title'][0])

                            if 'TPE1' in audio.tags: artist = str(audio.tags['TPE1'])
                            elif 'artist' in audio.tags: artist = str(audio.tags['artist'][0])

                            if 'TALB' in audio.tags: album = str(audio.tags['TALB'])
                            elif 'album' in audio.tags: album = str(audio.tags['album'][0])

                        duration = audio.info.length

                        track = Track(
                            title=title,
                            artist=artist,
                            album=album,
                            duration=duration,
                            path=file_path,
                            file_type=os.path.splitext(file)[1]
                        )
                        db.add(track)
                    except Exception as e:
                        print(f"Error scanning {file_path}: {e}")

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "music"
    scan_music_folder(folder)
