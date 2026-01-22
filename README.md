🎵 Local Music Streamer

A simple personal music streaming web app that streams your local music files. Designed for one user, no authentication required, and works entirely on your own machine.

Features

Stream MP3/FLAC/WAV files from a local folder

Play, pause, and seek in the browser

Browse by tracks, albums, and artists

Create and play playlists

Minimal, clean web UI

Runs on localhost, no public hosting required

Tech Stack

Backend: Python + FastAPI

Frontend: HTML + JavaScript (or React for optional polish)

Database: SQLite

Audio Streaming: HTTP Range Requests

Metadata Extraction: mutagen

Roadmap
Phase 0 — Setup & Decisions

Choose backend, frontend, database, and storage

Create project folder structure

Install dependencies

Phase 1 — Project Skeleton

Setup Python backend folder structure

Setup frontend folder structure

Add local music/ folder

Phase 2 — Scan Music Library

Walk through music/ folder

Extract metadata (title, artist, album, duration)

Save track info to SQLite database

Cache results for faster startup

Phase 3 — Backend API Endpoints

/tracks — list all tracks

/albums — list albums

/artists — list artists

/track/{id} — get track info

/stream/{id} — stream audio to browser

Phase 4 — Audio Streaming

Support HTTP Range Requests for seeking

Set proper headers (Content-Range, Accept-Ranges, Content-Type)

Handle smooth playback in browser

Phase 5 — Frontend Player

List tracks in the UI

Click to play songs

<audio> element integration

Optional: album grouping, search bar, queue

Phase 6 — Playlists

Database tables: playlists and playlist_tracks

API endpoints to create and manage playlists

Frontend UI for creating playlists and adding songs

Play playlists sequentially

Phase 7 — Polish & Optional Features

Remember last played song

Keyboard shortcuts

Album art display

Dark mode

Mobile-friendly layout

Security Notes

Bind server to localhost to keep it private

No file uploads or public access

Use your own music only to stay safe legally
