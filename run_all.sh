#!/bin/bash

# Colores para la consola
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuración
API_COMMAND="python app.py"
FRONTEND_COMMAND="python src/main.py"
API_PORT=5000
FRONTEND_PORT=5001

# Función para limpiar al salir
cleanup() {
    echo -e "${YELLOW}Deteniendo todos los procesos...${NC}"
    kill $API_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Registrar la función de limpieza
trap cleanup EXIT INT TERM

# Iniciar API en segundo plano
echo -e "${BLUE}Iniciando API en puerto ${API_PORT}...${NC}"
$API_COMMAND > api.log 2>&1 &
API_PID=$!

# Esperar un poco para que la API se inicie
sleep 2

# Verificar si la API se inició correctamente
if ! ps -p $API_PID > /dev/null; then
    echo -e "${RED}Error al iniciar la API. Revisa api.log para más detalles.${NC}"
    exit 1
fi

# Iniciar Frontend en segundo plano
echo -e "${GREEN}Iniciando Frontend en puerto ${FRONTEND_PORT}...${NC}"
$FRONTEND_COMMAND > frontend.log 2>&1 &
FRONTEND_PID=$!

# Verificar si el Frontend se inició correctamente
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}Error al iniciar el Frontend. Revisa frontend.log para más detalles.${NC}"
    kill $API_PID
    exit 1
fi

echo -e "${GREEN}¡Aplicaciones iniciadas correctamente!${NC}"
echo "API: http://localhost:${API_PORT}"
echo "Frontend: http://localhost:${FRONTEND_PORT}"
echo -e "${YELLOW}Los logs se guardan en api.log y frontend.log${NC}"
echo -e "${YELLOW}Presiona Ctrl+C para detener ambas aplicaciones${NC}"

# Mantener el script en ejecución
wait $API_PID $FRONTEND_PID
