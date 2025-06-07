from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from dotenv import load_dotenv
from utils.api_client import APIClient
from components.user_component import UserComponent
from components.song_component import SongComponent
from components.favorite_component import FavoriteComponent
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize API client and components
api_client = APIClient(base_url=os.getenv('API_BASE_URL', 'http://localhost:5000'))
user_component = UserComponent(api_client)
song_component = SongComponent(api_client)
favorite_component = FavoriteComponent(api_client)

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Debe iniciar sesión para acceder a esta página.', 'error')
            return redirect(url_for('login'))
        
        # Set the auth token if available
        if 'access_token' in session:
            api_client.set_auth_token(session['access_token'])
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page - redirect to login if not authenticated"""
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', title='Music App - Dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    # If already logged in, redirect to dashboard
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            
            # Attempt login
            result = user_component.login(nombre, correo)
            
            # Store session data
            session['logged_in'] = True
            session['user_name'] = nombre
            session['user_email'] = correo
            session['access_token'] = result.get('access_token')
            session['user_favorites'] = result.get('favoritos', [])
            
            flash(f'¡Bienvenido, {nombre}!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error en el login: {str(e)}', 'error')
    
    return render_template('login.html', title='Iniciar Sesión')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if request.method == 'POST':
        try:
            user_data = {
                'name': request.form['name'],
                'email': request.form['email']
            }
            result = user_component.create_user(user_data)
            flash('Usuario creado exitosamente. Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al crear usuario: {str(e)}', 'error')
    
    return render_template('register.html', title='Registrarse')

@app.route('/api-status')
@login_required
def api_status():
    """Check API connection status"""
    try:
        api_client.ping()
        status = {
            'status': 'connected',
            'message': 'API connection successful',
            'url': os.getenv('API_BASE_URL', 'http://localhost:5000')
        }
    except Exception as e:
        status = {
            'status': 'disconnected',
            'message': str(e),
            'url': os.getenv('API_BASE_URL', 'http://localhost:5000')
        }
    
    return render_template('api_status.html', status=status, title='API Status')

@app.route('/users')
@login_required
def users():
    """Display all users"""
    try:
        users_data = user_component.get_all_users()
        # Convert API field names to frontend field names for display
        for user in users_data:
            if 'nombre' in user:
                user['name'] = user['nombre']
            if 'correo' in user:
                user['email'] = user['correo']
        return render_template('users.html', users=users_data, title='Users')
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        return render_template('users.html', users=[], title='Users')

@app.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """Create a new user"""
    if request.method == 'POST':
        try:
            user_data = {
                'name': request.form['name'],
                'email': request.form['email']
            }
            result = user_component.create_user(user_data)
            flash('User created successfully!', 'success')
            return redirect(url_for('users'))
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'error')
    
    return render_template('user_form.html', title='Create User', action='Create')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit an existing user"""
    if request.method == 'POST':
        try:
            user_data = {
                'name': request.form['name'],
                'email': request.form['email']
            }
            result = user_component.update_user(user_id, user_data)
            flash('User updated successfully!', 'success')
            return redirect(url_for('users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'error')
    
    try:
        user = user_component.get_user(user_id)
        # Convert API field names to frontend field names
        if 'nombre' in user:
            user['name'] = user['nombre']
        if 'correo' in user:
            user['email'] = user['correo']
        return render_template('user_form.html', user=user, title='Edit User', action='Update')
    except Exception as e:
        flash(f'Error loading user: {str(e)}', 'error')
        return redirect(url_for('users'))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    try:
        user_component.delete_user(user_id)
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('users'))

@app.route('/songs')
@login_required
def songs():
    """Display all songs"""
    try:
        songs_data = song_component.get_all_songs()
        # Convert API field names to frontend field names for display
        for song in songs_data:
            if 'titulo' in song:
                song['title'] = song['titulo']
            if 'artista' in song:
                song['artist'] = song['artista']
            if 'duracion' in song:
                song['duration'] = song['duracion']
        return render_template('songs.html', songs=songs_data, title='Songs')
    except Exception as e:
        flash(f'Error loading songs: {str(e)}', 'error')
        return render_template('songs.html', songs=[], title='Songs')

@app.route('/songs/create', methods=['GET', 'POST'])
@login_required
def create_song():
    """Create a new song"""
    if request.method == 'POST':
        try:
            song_data = {
                'title': request.form['title'],
                'artist': request.form['artist'],
                'album': request.form.get('album', ''),
                'duration': int(request.form.get('duration', 0)) if request.form.get('duration') else None,
                'year': int(request.form.get('year', 0)) if request.form.get('year') else None,
                'genre': request.form.get('genre', '')
            }
            result = song_component.create_song(song_data)
            flash('Song created successfully!', 'success')
            return redirect(url_for('songs'))
        except Exception as e:
            flash(f'Error creating song: {str(e)}', 'error')
    
    return render_template('song_form.html', title='Create Song', action='Create')

@app.route('/songs/<int:song_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_song(song_id):
    """Edit an existing song"""
    if request.method == 'POST':
        try:
            song_data = {
                'title': request.form['title'],
                'artist': request.form['artist'],
                'album': request.form.get('album', ''),
                'duration': int(request.form.get('duration', 0)) if request.form.get('duration') else None,
                'year': int(request.form.get('year', 0)) if request.form.get('year') else None,
                'genre': request.form.get('genre', '')
            }
            result = song_component.update_song(song_id, song_data)
            flash('Song updated successfully!', 'success')
            return redirect(url_for('songs'))
        except Exception as e:
            flash(f'Error updating song: {str(e)}', 'error')
    
    try:
        song = song_component.get_song(song_id)
        # Convert API field names to frontend field names
        if 'titulo' in song:
            song['title'] = song['titulo']
        if 'artista' in song:
            song['artist'] = song['artista']
        if 'duracion' in song:
            song['duration'] = song['duracion']
        if 'año' in song:
            song['year'] = song['año']
        if 'genero' in song:
            song['genre'] = song['genero']
        return render_template('song_form.html', song=song, title='Edit Song', action='Update')
    except Exception as e:
        flash(f'Error loading song: {str(e)}', 'error')
        return redirect(url_for('songs'))

@app.route('/songs/<int:song_id>/delete', methods=['POST'])
@login_required
def delete_song(song_id):
    """Delete a song"""
    try:
        song_component.delete_song(song_id)
        flash('Song deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting song: {str(e)}', 'error')
    
    return redirect(url_for('songs'))

@app.route('/favorites')
@login_required
def favorites():
    """Display all favorites"""
    try:
        favorites_data = favorite_component.get_all_favorites()
        return render_template('favorites.html', favorites=favorites_data, title='Favorites')
    except Exception as e:
        flash(f'Error loading favorites: {str(e)}', 'error')
        return render_template('favorites.html', favorites=[], title='Favorites')

@app.route('/favorites/add', methods=['POST'])
@login_required
def add_favorite():
    """Add a song to favorites"""
    try:
        favorite_data = {
            'user_id': int(request.form['user_id']),
            'song_id': int(request.form['song_id'])
        }
        result = favorite_component.add_favorite(favorite_data)
        flash('Song added to favorites!', 'success')
    except Exception as e:
        flash(f'Error adding to favorites: {str(e)}', 'error')
    
    return redirect(url_for('favorites'))

@app.route('/favorites/<int:favorite_id>/remove', methods=['POST'])
@login_required
def remove_favorite(favorite_id):
    """Remove a song from favorites"""
    try:
        favorite_component.remove_favorite(favorite_id)
        flash('Song removed from favorites!', 'success')
    except Exception as e:
        flash(f'Error removing from favorites: {str(e)}', 'error')
    
    return redirect(url_for('favorites'))

@app.route('/api/users')
@login_required
def api_users():
    """API endpoint to get users for AJAX calls"""
    try:
        users_data = user_component.get_all_users()
        return jsonify(users_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/songs')
@login_required
def api_songs():
    """API endpoint to get songs for AJAX calls"""
    try:
        songs_data = song_component.get_all_songs()
        return jsonify(songs_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Context processor to make session data available in templates
@app.context_processor
def inject_user():
    return dict(
        current_user=session.get('user_name'),
        current_email=session.get('user_email'),
        is_logged_in=session.get('logged_in', False)
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
