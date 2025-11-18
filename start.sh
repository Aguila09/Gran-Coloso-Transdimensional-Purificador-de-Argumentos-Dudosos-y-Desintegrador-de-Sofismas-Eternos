#!/bin/bash
# Script para iniciar El Gran Coloso Transdimensional

echo "========================================================================"
echo "Iniciando El Gran Coloso Transdimensional"
echo "Purificador de Argumentos Dudosos y Desintegrador de Sofismas Eternos"
echo "========================================================================"
echo ""
echo "La interfaz estará disponible en: http://localhost:7861"
echo ""

cd "$(dirname "$0")"
python app.py
