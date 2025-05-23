import math


def pedir_float(mensaje, minimo=None):
    """
    Solicita al usuario un número flotante por consola.

    Args:
        mensaje (str): Mensaje a mostrar al usuario.
        minimo (float, optional): Valor mínimo aceptado (inclusive). Si es None, no hay mínimo.

    Returns:
        float: El valor ingresado por el usuario, validado.
    """
    while True:
        valor = input(mensaje)
        try:
            valor = float(valor)
            if minimo is not None and valor < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Por favor, ingresa un número válido.")


def pedir_jugadores():
    """
    Solicita al usuario los datos de los jugadores (nombre, hora de llegada y salida).

    Returns:
        list: Lista de diccionarios con los datos de cada jugador.
    """
    jugadores = []
    while True:
        nombre = input("Nombre del jugador (deja vacío para terminar): ")
        if not nombre:
            break
        llegada = pedir_float(f"Hora de llegada de {nombre} (ej: 18.0): ", minimo=0)
        while True:
            salida = pedir_float(
                f"Hora de salida de {nombre} (ej: 20.0): ", minimo=llegada
            )
            if salida < llegada:
                print("La hora de salida no puede ser menor que la hora de llegada.")
            else:
                break
        jugadores.append({"nombre": nombre, "llegada": llegada, "salida": salida})
    return jugadores


def calcular_pagos(jugadores, total, inicio, fin):
    """
    Calcula el pago correspondiente a cada jugador según el tiempo jugado.
    No usa input() ni print().

    Args:
        jugadores (list): Lista de diccionarios con los datos de cada jugador.
        total (float): Monto total a repartir.
        inicio (float): Hora de inicio de la cancha.
        fin (float): Hora de fin de la cancha.

    Returns:
        list: Lista de diccionarios con el nombre, pago y tiempo jugado de cada jugador.
    """
    tiempos = []
    for j in jugadores:
        tiempo = max(0, min(j["salida"], fin) - max(j["llegada"], inicio))
        tiempos.append(tiempo)
    suma_tiempos = sum(tiempos)
    pagos = []
    pagos_redondeados = []
    suma_redondeada = 0

    for i, j in enumerate(jugadores):
        pago = total * (tiempos[i] / suma_tiempos) if suma_tiempos > 0 else 0
        pagos.append({"nombre": j["nombre"], "pago": pago, "tiempo": tiempos[i]})

    for i, p in enumerate(pagos):
        if i < len(pagos) - 1:
            pago_r = round(p["pago"])
            pagos_redondeados.append(
                {"nombre": p["nombre"], "pago": pago_r, "tiempo": p["tiempo"]}
            )
            suma_redondeada += pago_r
        else:
            pago_r = round(total - suma_redondeada)
            pagos_redondeados.append(
                {"nombre": p["nombre"], "pago": pago_r, "tiempo": p["tiempo"]}
            )
    return pagos_redondeados


def mostrar_pagos(pagos):
    """
    Solo muestra los pagos por pantalla, no hace cálculos.
    """
    if pagos:
        max_nombre = max(len(p["nombre"]) for p in pagos)
        print(f"{'Jugador'.ljust(max_nombre)} | {'Pago'.rjust(8)} | {'Horas'.rjust(7)}")
        print("-" * (max_nombre + 22))
        for p in pagos:
            monto = f"{p['pago']:,.0f}".replace(",", ".")
            print(
                f"{p['nombre'].ljust(max_nombre)} | ${monto.rjust(7)} | {p['tiempo']:7.2f}"
            )
    else:
        print("No se ingresaron jugadores.")


def main():
    """
    Función principal. Solicita los datos, calcula y muestra los pagos.
    """
    print("=== Paddle Split ===")
    inicio = pedir_float("Hora de inicio de la cancha (ej: 18.0): ", minimo=0)
    fin = pedir_float("Hora de fin de la cancha (ej: 20.0): ", minimo=inicio)
    if fin < inicio:
        print("La hora de fin no puede ser menor que la hora de inicio.")
        return
    total = pedir_float("Total a pagar ($): ", minimo=0.01)
    jugadores = pedir_jugadores()
    # Validación adicional: ningún jugador puede salir después de la hora de fin de la cancha
    for jugador in jugadores:
        if jugador["salida"] > fin:
            print(
                f"Advertencia: {jugador['nombre']} tiene hora de salida después del fin de la cancha. Se ajustará a {fin}."
            )
            jugador["salida"] = fin
    pagos = calcular_pagos(jugadores, total, inicio, fin)
    print("\n--- Pagos ---")
    mostrar_pagos(pagos)


if __name__ == "__main__":
    main()
