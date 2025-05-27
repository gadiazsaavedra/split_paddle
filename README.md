# Split Paddle

Aplicación para dividir el costo de una cancha de paddle entre jugadores según el tiempo que cada uno jugó.

## Ejecución en AWS

### Opción 1: AWS EC2

1. Crea una instancia EC2 en la consola de AWS
   - Usa Amazon Linux 2023 o Ubuntu
   - Tipo de instancia: t2.micro (capa gratuita)
   - Configura un par de claves para SSH

2. Conéctate a tu instancia:
   ```
   ssh -i tu-clave.pem ec2-user@tu-ip-publica
   ```

3. Instala Python (si no está instalado):
   ```
   sudo yum update -y
   sudo yum install python3 -y
   ```

4. Sube tu código a la instancia:
   ```
   scp -i tu-clave.pem split_paddle.py ec2-user@tu-ip-publica:~
   ```

5. Ejecuta la aplicación:
   ```
   python3 split_paddle.py
   ```

### Opción 2: AWS Lambda (para versión web)

Para convertir esta aplicación a una versión web que pueda ejecutarse en AWS Lambda, necesitarías:

1. Crear una API con API Gateway
2. Implementar la lógica en una función Lambda
3. Crear una interfaz web para reemplazar las entradas por consola

## Notas

- La aplicación actual es interactiva por consola, por lo que funciona mejor en EC2
- Para una versión web, se necesitaría modificar el código para eliminar las entradas por consola