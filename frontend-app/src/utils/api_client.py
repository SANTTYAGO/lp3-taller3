import requests

API_BASE_URL = "http://localhost:5000/api"

def get_users():
    response = requests.get(f"{API_BASE_URL}/usuarios")
    response.raise_for_status()
    return response.json()

def get_user(user_id):
    response = requests.get(f"{API_BASE_URL}/usuarios/{user_id}")
    response.raise_for_status()
    return response.json()

def create_user(user_data):
    response = requests.post(f"{API_BASE_URL}/usuarios", json=user_data)
    response.raise_for_status()
    return response.json()

def update_user(user_id, user_data):
    response = requests.put(f"{API_BASE_URL}/usuarios/{user_id}", json=user_data)
    response.raise_for_status()
    return response.json()

def delete_user(user_id):
    response = requests.delete(f"{API_BASE_URL}/usuarios/{user_id}")
    response.raise_for_status()

def get_songs():
    response = requests.get(f"{API_BASE_URL}/canciones")
    response.raise_for_status()
    return response.json()

def get_song(song_id):
    response = requests.get(f"{API_BASE_URL}/canciones/{song_id}")
    response.raise_for_status()
    return response.json()

def create_song(song_data):
    response = requests.post(f"{API_BASE_URL}/canciones", json=song_data)
    response.raise_for_status()
    return response.json()

def update_song(song_id, song_data):
    response = requests.put(f"{API_BASE_URL}/canciones/{song_id}", json=song_data)
    response.raise_for_status()
    return response.json()

def delete_song(song_id):
    response = requests.delete(f"{API_BASE_URL}/canciones/{song_id}")
    response.raise_for_status()

def get_favorites():
    response = requests.get(f"{API_BASE_URL}/favoritos")
    response.raise_for_status()
    return response.json()

def add_favorite(favorite_data):
    response = requests.post(f"{API_BASE_URL}/favoritos", json=favorite_data)
    response.raise_for_status()
    return response.json()

def delete_favorite(favorite_id):
    response = requests.delete(f"{API_BASE_URL}/favoritos/{favorite_id}")
    response.raise_for_status()