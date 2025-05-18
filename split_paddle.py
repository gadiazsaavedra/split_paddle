import math


def pedir_jugadores():
    jugadores = []
    while True:
        nombre = input("Nombre del jugador (deja vacío para terminar): ")
        if not nombre:
            break
        llegada = float(input(f"Hora de llegada de {nombre} (ej: 18.0): "))
        salida = float(input(f"Hora de salida de {nombre} (ej: 20.0): "))
        jugadores.append({"nombre": nombre, "llegada": llegada, "salida": salida})
    return jugadores


def calcular_pagos(jugadores, total, inicio, fin):
    tiempos = []
    for j in jugadores:
        tiempo = max(0, min(j["salida"], fin) - max(j["llegada"], inicio))
        tiempos.append(tiempo)
    suma_tiempos = sum(tiempos)
    pagos = []
    for i, j in enumerate(jugadores):
        pago = total * (tiempos[i] / suma_tiempos) if suma_tiempos > 0 else 0
        pagos.append(
            {"nombre": j["nombre"], "pago": math.ceil(pago), "tiempo": tiempos[i]}
        )
    return pagos


def main():
    print("=== Paddle Split ===")
    inicio = float(input("Hora de inicio de la cancha (ej: 18.0): "))
    fin = float(input("Hora de fin de la cancha (ej: 20.0): "))
    total = float(input("Total a pagar ($): "))
    jugadores = pedir_jugadores()
    pagos = calcular_pagos(jugadores, total, inicio, fin)
    print("\n--- Pagos ---")
    for p in pagos:
        monto = f"{p['pago']:,.0f}".replace(",", ".")
        print(f"{p['nombre']}: ${monto} ({p['tiempo']:.2f} horas)")


if __name__ == "__main__":
    main()
