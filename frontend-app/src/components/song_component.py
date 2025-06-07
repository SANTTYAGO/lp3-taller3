from typing import List, Dict, Any
from utils.api_client import APIClient

class SongComponent:
    """Component for handling song-related operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    def get_all_songs(self) -> List[Dict[str, Any]]:
        """Get all songs from the API"""
        try:
            response = self.api_client.get('/api/canciones')
            # The API returns a list directly
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Error fetching songs: {e}")
            return []
    
    def get_song(self, song_id: int) -> Dict[str, Any]:
        """Get a specific song by ID"""
        try:
            response = self.api_client.get(f'/api/canciones/{song_id}')
            return response
        except Exception as e:
            print(f"Error fetching song {song_id}: {e}")
            raise e
    
    def create_song(self, song_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new song"""
        try:
            # Convert frontend field names to API field names
            api_data = {
                'titulo': song_data.get('title', song_data.get('titulo')),
                'artista': song_data.get('artist', song_data.get('artista')),
                'album': song_data.get('album'),
                'duracion': song_data.get('duration', song_data.get('duracion')),
                'año': song_data.get('year', song_data.get('año')),
                'genero': song_data.get('genre', song_data.get('genero'))
            }
            
            # Remove None values
            api_data = {k: v for k, v in api_data.items() if v is not None}
            
            self.validate_song_data(api_data)
            response = self.api_client.post('/api/canciones', api_data)
            return response
        except Exception as e:
            print(f"Error creating song: {e}")
            raise e
    
    def update_song(self, song_id: int, song_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing song"""
        try:
            # Convert frontend field names to API field names
            api_data = {
                'titulo': song_data.get('title', song_data.get('titulo')),
                'artista': song_data.get('artist', song_data.get('artista')),
                'album': song_data.get('album'),
                'duracion': song_data.get('duration', song_data.get('duracion')),
                'año': song_data.get('year', song_data.get('año')),
                'genero': song_data.get('genre', song_data.get('genero'))
            }
            
            # Remove None values
            api_data = {k: v for k, v in api_data.items() if v is not None}
            
            self.validate_song_data(api_data)
            response = self.api_client.put(f'/api/canciones/{song_id}', api_data)
            return response
        except Exception as e:
            print(f"Error updating song {song_id}: {e}")
            raise e
    
    def delete_song(self, song_id: int) -> Dict[str, Any]:
        """Delete a song"""
        try:
            response = self.api_client.delete(f'/api/canciones/{song_id}')
            return response
        except Exception as e:
            print(f"Error deleting song {song_id}: {e}")
            raise e
    
    def search_songs(self, titulo: str = None, artista: str = None, genero: str = None) -> List[Dict[str, Any]]:
        """Search songs by title, artist, or genre"""
        try:
            params = []
            if titulo:
                params.append(f'titulo={titulo}')
            if artista:
                params.append(f'artista={artista}')
            if genero:
                params.append(f'genero={genero}')
            
            query_string = '&'.join(params)
            endpoint = f'/api/canciones/buscar?{query_string}' if query_string else '/api/canciones/buscar'
            
            response = self.api_client.get(endpoint)
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Error searching songs: {e}")
            return []
    
    def validate_song_data(self, song_data: Dict[str, Any]) -> bool:
        """Validate song data before sending to API"""
        required_fields = ['titulo', 'artista']
        
        for field in required_fields:
            if field not in song_data or not song_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate duration if provided
        if 'duracion' in song_data and song_data['duracion'] is not None:
            try:
                duracion = int(song_data['duracion'])
                if duracion < 0:
                    raise ValueError("Duration must be a positive number")
            except (ValueError, TypeError):
                raise ValueError("Duration must be a valid number")
        
        # Validate year if provided
        if 'año' in song_data and song_data['año'] is not None:
            try:
                año = int(song_data['año'])
                if año < 1900 or año > 2030:
                    raise ValueError("Year must be between 1900 and 2030")
            except (ValueError, TypeError):
                raise ValueError("Year must be a valid number")
        
        return True
    
    def format_duration(self, seconds: int) -> str:
        """Format duration from seconds to MM:SS format"""
        if not seconds or seconds < 0:
            return "0:00"
        
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
