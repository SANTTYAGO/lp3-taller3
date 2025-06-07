import subprocess
import sys
import os
import time
import signal
import atexit

# Colores para la consola
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Configuración
API_COMMAND = ["python", "app.py"]  # Ajusta según la ubicación de tu archivo app.py
FRONTEND_COMMAND = ["python", "src/main.py"]  # Ajusta según la ubicación de tu archivo main.py
API_PORT = 5000
FRONTEND_PORT = 5001

# Lista para almacenar los procesos
processes = []

def start_api():
    """Inicia el servidor API"""
    print(f"{Colors.HEADER}[Launcher]{Colors.ENDC} {Colors.BLUE}Iniciando API en puerto {API_PORT}...{Colors.ENDC}")
    api_process = subprocess.Popen(
        API_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    processes.append(api_process)
    return api_process

def start_frontend():
    """Inicia la aplicación frontend"""
    print(f"{Colors.HEADER}[Launcher]{Colors.ENDC} {Colors.GREEN}Iniciando Frontend en puerto {FRONTEND_PORT}...{Colors.ENDC}")
    frontend_process = subprocess.Popen(
        FRONTEND_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    processes.append(frontend_process)
    return frontend_process

def monitor_output(process, prefix, color):
    """Monitorea la salida de un proceso y la muestra en la consola"""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"{color}[{prefix}]{Colors.ENDC} {output.strip()}")
    
    # Capturar errores
    for line in process.stderr:
        print(f"{Colors.RED}[{prefix} ERROR]{Colors.ENDC} {line.strip()}")

def cleanup():
    """Limpia los procesos al salir"""
    print(f"{Colors.YELLOW}Deteniendo todos los procesos...{Colors.ENDC}")
    for process in processes:
        if process.poll() is None:  # Si el proceso sigue en ejecución
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

# Registrar la función de limpieza para ejecutarse al salir
atexit.register(cleanup)

def handle_signal(sig, frame):
    """Maneja señales como Ctrl+C"""
    print(f"{Colors.YELLOW}Señal recibida, cerrando aplicaciones...{Colors.ENDC}")
    sys.exit(0)  # Esto llamará a cleanup() gracias a atexit

# Registrar manejador de señales
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

def main():
    """Función principal"""
    print(f"{Colors.BOLD}{Colors.HEADER}=== Iniciando API y Frontend ===={Colors.ENDC}")
    
    # Iniciar API
    api_process = start_api()
    
    # Esperar un poco para que la API se inicie
    time.sleep(2)
    
    # Iniciar Frontend
    frontend_process = start_frontend()
    
    # Crear hilos para monitorear la salida
    import threading
    api_thread = threading.Thread(target=monitor_output, args=(api_process, "API", Colors.BLUE))
    frontend_thread = threading.Thread(target=monitor_output, args=(frontend_process, "Frontend", Colors.GREEN))
    
    # Iniciar hilos
    api_thread.daemon = True
    frontend_thread.daemon = True
    api_thread.start()
    frontend_thread.start()
    
    print(f"{Colors.BOLD}{Colors.GREEN}¡Aplicaciones iniciadas correctamente!{Colors.ENDC}")
    print(f"API: http://localhost:{API_PORT}")
    print(f"Frontend: http://localhost:{FRONTEND_PORT}")
    print(f"{Colors.YELLOW}Presiona Ctrl+C para detener ambas aplicaciones{Colors.ENDC}")
    
    # Mantener el script en ejecución
    try:
        while True:
            # Verificar si algún proceso ha terminado
            if api_process.poll() is not None:
                print(f"{Colors.RED}[ERROR] El proceso de la API ha terminado con código {api_process.returncode}{Colors.ENDC}")
                break
            if frontend_process.poll() is not None:
                print(f"{Colors.RED}[ERROR] El proceso del Frontend ha terminado con código {frontend_process.returncode}{Colors.ENDC}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{Colors.YELLOW}Deteniendo aplicaciones...{Colors.ENDC}")

if __name__ == "__main__":
    main()
