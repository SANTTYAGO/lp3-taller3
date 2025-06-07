class FavoriteComponent:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_favorites(self, user_id):
        """Fetch the favorite songs for a specific user."""
        response = self.api_client.get(f"/api/usuarios/{user_id}/favoritos")
        return response.json() if response.status_code == 200 else []

    def add_favorite(self, user_id, song_id):
        """Add a song to the user's favorites."""
        data = {"id_usuario": user_id, "id_cancion": song_id}
        response = self.api_client.post("/api/favoritos", json=data)
        return response.status_code == 201

    def remove_favorite(self, favorite_id):
        """Remove a song from the user's favorites."""
        response = self.api_client.delete(f"/api/favoritos/{favorite_id}")
        return response.status_code == 204