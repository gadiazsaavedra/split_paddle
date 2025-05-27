#!/bin/bash
# Script para desplegar la aplicación en una instancia EC2

# Verificar que se proporcionaron los parámetros necesarios
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 ruta-a-clave-privada dirección-ip-ec2"
    echo "Ejemplo: $0 ~/mi-clave.pem ec2-user@ec2-12-34-56-78.compute-1.amazonaws.com"
    exit 1
fi

KEY_PATH=$1
EC2_ADDRESS=$2

echo "Desplegando aplicación en $EC2_ADDRESS..."

# Crear directorio remoto
ssh -i "$KEY_PATH" "$EC2_ADDRESS" "mkdir -p ~/split_paddle"

# Copiar archivos al servidor
echo "Copiando archivos..."
scp -i "$KEY_PATH" split_paddle.py "$EC2_ADDRESS:~/split_paddle/"
scp -i "$KEY_PATH" setup_ec2.sh "$EC2_ADDRESS:~/"

# Ejecutar script de configuración
echo "Configurando el entorno..."
ssh -i "$KEY_PATH" "$EC2_ADDRESS" "chmod +x ~/setup_ec2.sh && ~/setup_ec2.sh"

echo "¡Despliegue completado!"
echo "Para conectarte y ejecutar la aplicación:"
echo "  1. ssh -i $KEY_PATH $EC2_ADDRESS"
echo "  2. cd ~/split_paddle && python3 split_paddle.py"