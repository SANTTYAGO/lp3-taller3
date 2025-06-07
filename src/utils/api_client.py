import requests
import json
from typing import Dict, List, Any, Optional

class APIClient:
    """Client for making HTTP requests to the music API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.access_token = None
    
    def set_auth_token(self, token: str):
        """Set JWT authentication token"""
        self.access_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            # Handle empty responses (like 204 No Content)
            if response.status_code == 204 or not response.content:
                return {'success': True}
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {str(e)}")
            raise Exception(f"No se pudo conectar a la API. Verifique que el servidor API esté ejecutándose en {self.base_url}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {str(e)}")
            raise Exception(f"Tiempo de espera agotado al conectar con la API en {self.base_url}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {str(e)}")
            if response.status_code == 404:
                raise Exception("Recurso no encontrado en la API")
            elif response.status_code == 401:
                raise Exception("No autorizado - verifique sus credenciales")
            elif response.status_code == 403:
                raise Exception("Acceso prohibido")
            else:
                raise Exception(f"Error HTTP {response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            raise Exception(f"Error en la solicitud API: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            raise Exception(f"Respuesta inválida del servidor: {str(e)}")
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request('GET', endpoint)
    
    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """Make POST request"""
        return self._make_request('POST', endpoint, data)
    
    def put(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """Make PUT request"""
        return self._make_request('PUT', endpoint, data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint)
    
    def login(self, nombre: str, correo: str) -> Dict[str, Any]:
        """Login and get JWT token"""
        try:
            response = self.post('/api/login', {'nombre': nombre, 'correo': correo})
            if 'access_token' in response:
                self.set_auth_token(response['access_token'])
            return response
        except Exception as e:
            raise Exception(f"Error en el login: {str(e)}")
    
    def ping(self) -> Dict[str, Any]:
        """Test API connection"""
        return self.get('/api/ping')
