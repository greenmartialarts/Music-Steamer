import unittest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class TestMusicStreamer(unittest.TestCase):
    def test_get_tracks(self):
        response = client.get("/tracks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_albums(self):
        response = client.get("/albums")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_playlist(self):
        response = client.post("/playlists", json={"name": "Test Playlist"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Playlist")

if __name__ == "__main__":
    unittest.main()
