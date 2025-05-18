# split_paddle
permite calcular cuanto debe pagar cada jugador
# Paddle Split

Este programa en Python te ayuda a dividir el costo de una cancha de paddle entre varios jugadores, considerando el tiempo real que cada uno jugó. Es ideal para grupos donde los jugadores entran y salen en diferentes horarios.

## ¿Cómo funciona?

1. **Ingresa la hora de inicio y fin de la cancha** (en formato decimal, por ejemplo, 18.0 para 18:00, 18.5 para 18:30).
2. **Ingresa el total a pagar** por la cancha.
3. **Agrega los jugadores** uno por uno, indicando:
   - Nombre
   - Hora de llegada (formato decimal)
   - Hora de salida (formato decimal)
4. El programa calcula cuánto debe pagar cada jugador, proporcional al tiempo jugado, redondeando siempre hacia arriba y mostrando el tiempo jugado.

## Ejemplo de uso

```
=== Paddle Split ===
Hora de inicio de la cancha (ej: 18.0): 18.0
Hora de fin de la cancha (ej: 20.0): 20.0
Total a pagar ($): 4000
Nombre del jugador (deja vacío para terminar): Juan
Hora de llegada de Juan (ej: 18.0): 18.0
Hora de salida de Juan (ej: 20.0): 20.0
Nombre del jugador (deja vacío para terminar): Pedro
Hora de llegada de Pedro (ej: 18.5): 18.5
Hora de salida de Pedro (ej: 20.0): 20.0
Nombre del jugador (deja vacío para terminar): 
--- Pagos ---
Juan: $2.286 (2.00 horas)
Pedro: $1.714 (1.50 horas)
```

## Formato de horas

- **18.0** = 18:00 hs
- **18.5** = 18:30 hs
- **19.25** = 19:15 hs (15 minutos = 0.25 horas)
- **19.75** = 19:45 hs (45 minutos = 0.75 horas)

Para convertir minutos a decimal:  
`hora_decimal = hora + (minutos / 60)`

## Requisitos

- Python 3.x

## Ejecución

Abre una terminal y ejecuta:

```bash
python split_paddle.py
```

---

¡Listo! Así podrás dividir el costo de la cancha de manera justa según el tiempo jugado por cada uno.
