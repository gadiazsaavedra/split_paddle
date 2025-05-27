#!/bin/bash
# Script para configurar una instancia EC2 para ejecutar split_paddle.py

# Actualizar el sistema
echo "Actualizando el sistema..."
sudo yum update -y || sudo apt update -y

# Instalar Python
echo "Instalando Python..."
sudo yum install python3 -y || sudo apt install python3 -y

# Crear un directorio para la aplicación
echo "Creando directorio para la aplicación..."
mkdir -p ~/split_paddle

# Copiar el archivo principal
echo "Copiando archivos de la aplicación..."
cp split_paddle.py ~/split_paddle/

# Dar permisos de ejecución
echo "Configurando permisos..."
chmod +x ~/split_paddle/split_paddle.py

echo "¡Configuración completada!"
echo "Para ejecutar la aplicación: cd ~/split_paddle && python3 split_paddle.py"