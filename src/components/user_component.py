from typing import List, Dict, Any
from utils.api_client import APIClient

class UserComponent:
    """Component for handling user-related operations"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from the API"""
        try:
            response = self.api_client.get('/api/usuarios')
            # The API returns a list directly
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID"""
        try:
            response = self.api_client.get(f'/api/usuarios/{user_id}')
            return response
        except Exception as e:
            print(f"Error fetching user {user_id}: {e}")
            raise e
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            # Convert frontend field names to API field names
            api_data = {
                'nombre': user_data.get('name', user_data.get('nombre')),
                'correo': user_data.get('email', user_data.get('correo'))
            }
            self.validate_user_data(api_data)
            response = self.api_client.post('/api/usuarios', api_data)
            return response
        except Exception as e:
            print(f"Error creating user: {e}")
            raise e
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user"""
        try:
            # Convert frontend field names to API field names
            api_data = {
                'nombre': user_data.get('name', user_data.get('nombre')),
                'correo': user_data.get('email', user_data.get('correo'))
            }
            self.validate_user_data(api_data)
            response = self.api_client.put(f'/api/usuarios/{user_id}', api_data)
            return response
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            raise e
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete a user"""
        try:
            response = self.api_client.delete(f'/api/usuarios/{user_id}')
            return response
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            raise e
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> bool:
        """Validate user data before sending to API"""
        required_fields = ['nombre', 'correo']
        
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Basic email validation
        correo = user_data['correo']
        if '@' not in correo or '.' not in correo:
            raise ValueError("Invalid email format")
        
        return True
    
    def login(self, nombre: str, correo: str) -> Dict[str, Any]:
        """Login user and get JWT token"""
        try:
            response = self.api_client.login(nombre, correo)
        except Exception as e:
            print(f"Error logging in: {e}")
            raise e
        return response
