from typing import List, Dict, Any
from utils.api_client import APIClient

class FavoriteComponent:
    """Component for handling favorite songs operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    def get_all_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite songs from the API with enhanced data"""
        try:
            print("[DEBUG] Fetching all favorites...")
            response = self.api_client.get('/api/favoritos')
            favorites = response if isinstance(response, list) else []
            
            # Enriquecer los datos de favoritos con información de usuario y canción
            enriched_favorites = []
            for favorite in favorites:
                try:
                    enriched_favorite = self._enrich_favorite_data(favorite)
                    enriched_favorites.append(enriched_favorite)
                except Exception as e:
                    print(f"[WARNING] Error enriching favorite {favorite.get('id', 'unknown')}: {e}")
                    # Agregar el favorito sin enriquecer si hay error
                    enriched_favorites.append(favorite)
            
            print(f"[DEBUG] Successfully fetched {len(enriched_favorites)} favorites")
            return enriched_favorites
            
        except Exception as e:
            print(f"[ERROR] Error fetching favorites: {e}")
            return []
    
    def _enrich_favorite_data(self, favorite: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich favorite data with user and song information"""
        enriched = favorite.copy()
        
        # Obtener información del usuario
        user_id = favorite.get('id_usuario') or favorite.get('user_id')
        if user_id:
            try:
                user_data = self.api_client.get(f'/api/usuarios/{user_id}')
                enriched['user_name'] = user_data.get('nombre', user_data.get('name', 'Usuario Desconocido'))
                enriched['user_email'] = user_data.get('correo', user_data.get('email', ''))
            except Exception as e:
                print(f"[WARNING] Could not fetch user data for user_id {user_id}: {e}")
                enriched['user_name'] = 'Usuario Desconocido'
                enriched['user_email'] = ''
        
        # Obtener información de la canción
        song_id = favorite.get('id_cancion') or favorite.get('song_id')
        if song_id:
            try:
                song_data = self.api_client.get(f'/api/canciones/{song_id}')
                enriched['song_title'] = song_data.get('titulo', song_data.get('title', 'Canción Desconocida'))
                enriched['song_artist'] = song_data.get('artista', song_data.get('artist', 'Artista Desconocido'))
                enriched['song_album'] = song_data.get('album', '')
            except Exception as e:
                print(f"[WARNING] Could not fetch song data for song_id {song_id}: {e}")
                enriched['song_title'] = 'Canción Desconocida'
                enriched['song_artist'] = 'Artista Desconocido'
                enriched['song_album'] = ''
        
        return enriched
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """Get favorite songs for a specific user"""
        try:
            print(f"[DEBUG] Fetching favorites for user {user_id}...")
            response = self.api_client.get(f'/api/usuarios/{user_id}/favoritos')
            favorites = response if isinstance(response, list) else []
            print(f"[DEBUG] Found {len(favorites)} favorites for user {user_id}")
            return favorites
        except Exception as e:
            print(f"[ERROR] Error fetching favorites for user {user_id}: {e}")
            return []
    
    def add_favorite(self, favorite_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a song to favorites"""
        try:
            print(f"[DEBUG] Adding favorite: {favorite_data}")
            
            # Convertir nombres de campos del frontend a la API
            api_data = {
                'id_usuario': favorite_data.get('user_id', favorite_data.get('id_usuario')),
                'id_cancion': favorite_data.get('song_id', favorite_data.get('id_cancion'))
            }
            
            print(f"[DEBUG] API data: {api_data}")
            self.validate_favorite_data(api_data)
            
            response = self.api_client.post('/api/favoritos', api_data)
            print(f"[DEBUG] Favorite added successfully: {response}")
            return response
            
        except Exception as e:
            print(f"[ERROR] Error adding favorite: {e}")
            raise e
    
    def remove_favorite(self, favorite_id: int) -> Dict[str, Any]:
        """Remove a song from favorites"""
        try:
            print(f"[DEBUG] Removing favorite with ID: {favorite_id}")
            response = self.api_client.delete(f'/api/favoritos/{favorite_id}')
            print(f"[DEBUG] Favorite removed successfully")
            return response
        except Exception as e:
            print(f"[ERROR] Error removing favorite {favorite_id}: {e}")
            raise e
    
    def toggle_favorite_for_user(self, user_id: int, song_id: int) -> Dict[str, Any]:
        """Toggle favorite status using the specific user/song endpoint"""
        try:
            print(f"[DEBUG] Toggling favorite for user {user_id}, song {song_id}")
            
            # Verificar si ya es favorito
            if self.is_favorite(user_id, song_id):
                # Si ya es favorito, lo removemos
                return self.remove_favorite_for_user(user_id, song_id)
            else:
                # Si no es favorito, lo agregamos
                response = self.api_client.post(f'/api/usuarios/{user_id}/favoritos/{song_id}', {})
                print(f"[DEBUG] Favorite toggled successfully")
                return response
                
        except Exception as e:
            print(f"[ERROR] Error toggling favorite: {e}")
            raise e
    
    def remove_favorite_for_user(self, user_id: int, song_id: int) -> Dict[str, Any]:
        """Remove favorite using the specific user/song endpoint"""
        try:
            print(f"[DEBUG] Removing favorite for user {user_id}, song {song_id}")
            response = self.api_client.delete(f'/api/usuarios/{user_id}/favoritos/{song_id}')
            print(f"[DEBUG] Favorite removed for user successfully")
            return response
        except Exception as e:
            print(f"[ERROR] Error removing favorite for user: {e}")
            raise e
    
    def is_favorite(self, user_id: int, song_id: int) -> bool:
        """Check if a song is in user's favorites"""
        try:
            print(f"[DEBUG] Checking if song {song_id} is favorite for user {user_id}")
            user_favorites = self.get_user_favorites(user_id)
            is_fav = any(
                fav.get('id_cancion') == song_id or fav.get('song_id') == song_id 
                for fav in user_favorites
            )
            print(f"[DEBUG] Is favorite: {is_fav}")
            return is_fav
        except Exception as e:
            print(f"[ERROR] Error checking favorite status: {e}")
            return False
    
    def validate_favorite_data(self, favorite_data: Dict[str, Any]) -> bool:
        """Validate favorite data before sending to API"""
        required_fields = ['id_usuario', 'id_cancion']
        
        for field in required_fields:
            if field not in favorite_data or not favorite_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Validar que los IDs sean enteros positivos
        try:
            user_id = int(favorite_data['id_usuario'])
            song_id = int(favorite_data['id_cancion'])
            
            if user_id <= 0 or song_id <= 0:
                raise ValueError("User ID and Song ID must be positive numbers")
                
        except (ValueError, TypeError):
            raise ValueError("User ID and Song ID must be valid numbers")
        
        return True
    
    def get_favorites_summary(self) -> Dict[str, Any]:
        """Get a summary of favorites data"""
        try:
            favorites = self.get_all_favorites()
            
            # Contar favoritos por usuario
            user_counts = {}
            song_counts = {}
            
            for fav in favorites:
                user_id = fav.get('id_usuario') or fav.get('user_id')
                song_id = fav.get('id_cancion') or fav.get('song_id')
                
                if user_id:
                    user_counts[user_id] = user_counts.get(user_id, 0) + 1
                if song_id:
                    song_counts[song_id] = song_counts.get(song_id, 0) + 1
            
            return {
                'total_favorites': len(favorites),
                'unique_users': len(user_counts),
                'unique_songs': len(song_counts),
                'most_favorited_song': max(song_counts.items(), key=lambda x: x[1]) if song_counts else None,
                'user_with_most_favorites': max(user_counts.items(), key=lambda x: x[1]) if user_counts else None
            }
            
        except Exception as e:
            print(f"[ERROR] Error getting favorites summary: {e}")
            return {
                'total_favorites': 0,
                'unique_users': 0,
                'unique_songs': 0,
                'most_favorited_song': None,
                'user_with_most_favorites': None
            }
