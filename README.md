# 🎵 Local Music Streamer

A simple, lightweight personal music streaming web app. Stream your local MP3, FLAC, and WAV files directly to your browser. Designed for single-user local use—no authentication, no public hosting, just your music.

---

## ✨ Features

- **High Fidelity**: Stream MP3, FLAC, and WAV files from your local folders.
- **Full Control**: Play, pause, and seek with support for HTTP Range Requests.
- **Library Management**: Browse your music by tracks, albums, and artists.
- **Playlists**: Create and manage your own custom playlists.
- **Minimalist UI**: Clean, dark-themed web interface for a focused listening experience.
- **Local-First**: Runs entirely on your machine.

---

## 🛠️ Tech Stack

- **Backend**: Python + [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Metadata**: [Mutagen](https://mutagen.readthedocs.io/) for audio tag extraction
- **Server**: [Uvicorn](https://www.uvicorn.org/)

---

## 🚀 Quick Start

### 1. Install Dependencies
Ensure you have Python 3.8+ installed.
```bash
pip install -r requirements.txt
```

### 2. Scan Your Music
Place your music files in the `music/` directory. You can organize them into subfolders (e.g., `Artist/Album/Song.mp3`).
```bash
python3 -m backend.scanner music
```

### 3. Run the App
Start the unified server (serves both API and Frontend):
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 4. Start Listening
Open your browser and navigate to:
[**http://localhost:8000**](http://localhost:8000)

---

## 📂 Project Structure

- `backend/`: FastAPI application, database models, and scanner.
- `frontend/`: Web interface (HTML, CSS, JS).
- `music/`: Your local music library.
- `music_streamer.db`: SQLite database (generated after scan).

---

## 🔒 Security & Privacy

- **Local Only**: The server is designed to bind to `localhost` to keep your library private.
- **Your Data**: No data ever leaves your machine.
- **No Uploads**: Files are read directly from your specified local folder.

---

## ⚖️ License

Use your own music library responsibly and stay within legal boundaries. Happy listening! 🎧
