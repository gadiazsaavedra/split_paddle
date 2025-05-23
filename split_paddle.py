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
        valor_ingresado = input(mensaje)
        try:
            valor = float(valor_ingresado)
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
        nombre_jugador = input("Nombre del jugador (deja vacío para terminar): ")
        if not nombre_jugador:
            break
        hora_llegada = pedir_float(
            f"Hora de llegada de {nombre_jugador} (ej: 18.0): ", minimo=0
        )
        while True:
            hora_salida = pedir_float(
                f"Hora de salida de {nombre_jugador} (ej: 20.0): ", minimo=hora_llegada
            )
            if hora_salida < hora_llegada:
                print("La hora de salida no puede ser menor que la hora de llegada.")
            else:
                break
        jugadores.append(
            {"nombre": nombre_jugador, "llegada": hora_llegada, "salida": hora_salida}
        )
    return jugadores


def calcular_pagos(jugadores, monto_total, hora_inicio, hora_fin):
    """
    Calcula el pago correspondiente a cada jugador según el tiempo jugado.
    No usa input() ni print().

    Args:
        jugadores (list): Lista de diccionarios con los datos de cada jugador.
        monto_total (float): Monto total a repartir.
        hora_inicio (float): Hora de inicio de la cancha.
        hora_fin (float): Hora de fin de la cancha.

    Returns:
        list: Lista de diccionarios con el nombre, pago y tiempo jugado de cada jugador.
    """
    tiempos_jugados = []
    for jugador in jugadores:
        # Calcula el tiempo jugado por cada jugador dentro del rango permitido
        tiempo = max(
            0, min(jugador["salida"], hora_fin) - max(jugador["llegada"], hora_inicio)
        )
        tiempos_jugados.append(tiempo)
    suma_tiempos = sum(tiempos_jugados)
    pagos_detallados = []
    pagos_redondeados = []
    suma_pagos_redondeados = 0

    # Calcula el pago proporcional para cada jugador
    for i, jugador in enumerate(jugadores):
        if suma_tiempos > 0:
            pago = monto_total * (tiempos_jugados[i] / suma_tiempos)
        else:
            pago = 0
        pagos_detallados.append(
            {"nombre": jugador["nombre"], "pago": pago, "tiempo": tiempos_jugados[i]}
        )

    # Redondea los pagos y ajusta el último para que la suma sea exacta
    for i, pago_info in enumerate(pagos_detallados):
        if i < len(pagos_detallados) - 1:
            pago_redondeado = round(pago_info["pago"])
            pagos_redondeados.append(
                {
                    "nombre": pago_info["nombre"],
                    "pago": pago_redondeado,
                    "tiempo": pago_info["tiempo"],
                }
            )
            suma_pagos_redondeados += pago_redondeado
        else:
            pago_redondeado = round(monto_total - suma_pagos_redondeados)
            pagos_redondeados.append(
                {
                    "nombre": pago_info["nombre"],
                    "pago": pago_redondeado,
                    "tiempo": pago_info["tiempo"],
                }
            )
    return pagos_redondeados


def mostrar_pagos(lista_pagos):
    """
    Muestra los pagos por pantalla en formato de tabla.
    """
    if lista_pagos:
        ancho_nombre = max(len(pago["nombre"]) for pago in lista_pagos)
        print(
            f"{'Jugador'.ljust(ancho_nombre)} | {'Pago'.rjust(8)} | {'Horas'.rjust(7)}"
        )
        print("-" * (ancho_nombre + 22))
        for pago in lista_pagos:
            monto_str = f"{pago['pago']:,.0f}".replace(",", ".")
            print(
                f"{pago['nombre'].ljust(ancho_nombre)} | ${monto_str.rjust(7)} | {pago['tiempo']:7.2f}"
            )
    else:
        print("No se ingresaron jugadores.")


def main():
    """
    Función principal. Solicita los datos, calcula y muestra los pagos.
    """
    print("=== Paddle Split ===")
    hora_inicio = pedir_float("Hora de inicio de la cancha (ej: 18.0): ", minimo=0)
    hora_fin = pedir_float("Hora de fin de la cancha (ej: 20.0): ", minimo=hora_inicio)
    if hora_fin < hora_inicio:
        print("La hora de fin no puede ser menor que la hora de inicio.")
        return
    monto_total = pedir_float("Total a pagar ($): ", minimo=0.01)
    jugadores = pedir_jugadores()
    # Validación adicional: ningún jugador puede salir después de la hora de fin de la cancha
    for jugador in jugadores:
        if jugador["salida"] > hora_fin:
            print(
                f"Advertencia: {jugador['nombre']} tiene hora de salida después del fin de la cancha. Se ajustará a {hora_fin}."
            )
            jugador["salida"] = hora_fin
    lista_pagos = calcular_pagos(jugadores, monto_total, hora_inicio, hora_fin)
    print("\n--- Pagos ---")
    mostrar_pagos(lista_pagos)


if __name__ == "__main__":
    main()
