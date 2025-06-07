from typing import List, Dict, Any
from utils.api_client import APIClient

class FavoriteComponent:
    """Component for handling favorite songs operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    def get_all_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite songs from the API"""
        try:
            response = self.api_client.get('/api/favoritos')
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Error fetching favorites: {e}")
            return []
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """Get favorite songs for a specific user"""
        try:
            response = self.api_client.get(f'/api/usuarios/{user_id}/favoritos')
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Error fetching favorites for user {user_id}: {e}")
            return []
    
    def add_favorite(self, favorite_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a song to favorites"""
        try:
            # Convert frontend field names to API field names
            api_data = {
                'id_usuario': favorite_data.get('user_id', favorite_data.get('id_usuario')),
                'id_cancion': favorite_data.get('song_id', favorite_data.get('id_cancion'))
            }
            self.validate_favorite_data(api_data)
            response = self.api_client.post('/api/favoritos', api_data)
            return response
        except Exception as e:
            print(f"Error adding favorite: {e}")
            raise e
    
    def remove_favorite(self, favorite_id: int) -> Dict[str, Any]:
        """Remove a song from favorites"""
        try:
            response = self.api_client.delete(f'/api/favoritos/{favorite_id}')
            return response
        except Exception as e:
            print(f"Error removing favorite {favorite_id}: {e}")
            raise e
    
    def toggle_favorite_for_user(self, user_id: int, song_id: int) -> Dict[str, Any]:
        """Toggle favorite status using the specific user/song endpoint"""
        try:
            # Try to add the favorite using the specific endpoint
            response = self.api_client.post(f'/api/usuarios/{user_id}/favoritos/{song_id}', {})
            return response
        except Exception as e:
            print(f"Error toggling favorite: {e}")
            raise e
    
    def remove_favorite_for_user(self, user_id: int, song_id: int) -> Dict[str, Any]:
        """Remove favorite using the specific user/song endpoint"""
        try:
            response = self.api_client.delete(f'/api/usuarios/{user_id}/favoritos/{song_id}')
            return response
        except Exception as e:
            print(f"Error removing favorite for user: {e}")
            raise e
    
    def is_favorite(self, user_id: int, song_id: int) -> bool:
        """Check if a song is in user's favorites"""
        try:
            user_favorites = self.get_user_favorites(user_id)
            return any(fav.get('id_cancion') == song_id for fav in user_favorites)
        except Exception as e:
            print(f"Error checking favorite status: {e}")
            return False
    
    def validate_favorite_data(self, favorite_data: Dict[str, Any]) -> bool:
        """Validate favorite data before sending to API"""
        required_fields = ['id_usuario', 'id_cancion']
        
        for field in required_fields:
            if field not in favorite_data or not favorite_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate IDs are positive integers
        try:
            user_id = int(favorite_data['id_usuario'])
            song_id = int(favorite_data['id_cancion'])
            
            if user_id <= 0 or song_id <= 0:
                raise ValueError("User ID and Song ID must be positive numbers")
                
        except (ValueError, TypeError):
            raise ValueError("User ID and Song ID must be valid numbers")
        
        return True
