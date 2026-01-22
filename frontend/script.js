const API_URL = 'http://localhost:8000';

const trackList = document.getElementById('track-list');
const playlistList = document.getElementById('playlist-list');
const audioPlayer = document.getElementById('audio-player');
const currentTrackTitle = document.getElementById('current-track-title');
const currentTrackArtist = document.getElementById('current-track-artist');
const createPlaylistBtn = document.getElementById('create-playlist');
const newPlaylistNameInput = document.getElementById('new-playlist-name');
const playlistModal = document.getElementById('playlist-modal');
const modalPlaylistList = document.getElementById('modal-playlist-list');
const closeModalBtn = document.getElementById('close-modal');

let allTracks = [];
let allPlaylists = [];
let trackToAddToPlaylist = null;

async function fetchTracks() {
    const response = await fetch(`${API_URL}/tracks`);
    allTracks = await response.json();
    renderTracks();
}

async function fetchPlaylists() {
    const response = await fetch(`${API_URL}/playlists`);
    allPlaylists = await response.json();
    renderPlaylists(allPlaylists);
}

function renderTracks() {
    trackList.innerHTML = '';
    allTracks.forEach(track => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="track-info">
                <span class="track-title">${track.title}</span>
                <span class="track-artist">${track.artist} - ${track.album}</span>
            </div>
            <button class="add-to-playlist" data-id="${track.id}">+</button>
        `;
        li.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-playlist')) return;
            playTrack(track);
        });

        const addBtn = li.querySelector('.add-to-playlist');
        addBtn.addEventListener('click', async (e) => {
            e.stopPropagation();
            trackToAddToPlaylist = track.id;
            showPlaylistModal();
        });

        trackList.appendChild(li);
    });
}

function renderPlaylists(playlists) {
    playlistList.innerHTML = '';
    playlists.forEach(playlist => {
        const li = document.createElement('li');
        li.textContent = playlist.name;
        li.addEventListener('click', () => loadPlaylist(playlist.id));
        playlistList.appendChild(li);
    });
}

async function loadPlaylist(playlistId) {
    const response = await fetch(`${API_URL}/playlists/${playlistId}`);
    const data = await response.json();
    allTracks = data.tracks;
    renderTracks();
}

async function createPlaylist() {
    const name = newPlaylistNameInput.value;
    if (!name) return;
    await fetch(`${API_URL}/playlists`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    newPlaylistNameInput.value = '';
    fetchPlaylists();
}

async function addToPlaylist(playlistId, trackId) {
    await fetch(`${API_URL}/playlists/${playlistId}/add/${trackId}`, { method: 'POST' });
    alert('Added to playlist');
}

function playTrack(track) {
    audioPlayer.src = `${API_URL}/stream/${track.id}`;
    audioPlayer.play();
    currentTrackTitle.textContent = track.title;
    currentTrackArtist.textContent = track.artist;
}

function showPlaylistModal() {
    modalPlaylistList.innerHTML = '';
    allPlaylists.forEach(playlist => {
        const li = document.createElement('li');
        li.textContent = playlist.name;
        li.addEventListener('click', async () => {
            await addToPlaylist(playlist.id, trackToAddToPlaylist);
            playlistModal.style.display = 'none';
        });
        modalPlaylistList.appendChild(li);
    });
    playlistModal.style.display = 'block';
}

closeModalBtn.addEventListener('click', () => {
    playlistModal.style.display = 'none';
});

createPlaylistBtn.addEventListener('click', createPlaylist);

// Initial load
fetchTracks();
fetchPlaylists();
