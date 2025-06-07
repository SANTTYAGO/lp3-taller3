"""
Script principal para ejecutar la aplicación Flask.
"""
import os
from musica_api import create_app
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

# Crear la aplicación
app = create_app()

if __name__ == "__main__":
    # Obtener puerto del ambiente o usar 5000 por defecto
    port = int(os.getenv("PORT", 5000))
    
    # Determinar si se debe usar modo debug
    debug = os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]
    
    # Ejecutar aplicación
    app.run(host="0.0.0.0", port=port, debug=debug)
