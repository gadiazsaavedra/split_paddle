import math


def pedir_float(mensaje, minimo=None, maximo=None):
    """
    Solicita al usuario un número flotante por consola, validando rango.

    Args:
        mensaje (str): Mensaje a mostrar al usuario.
        minimo (float, optional): Valor mínimo aceptado (inclusive). Si es None, no hay mínimo.
        maximo (float, optional): Valor máximo aceptado (inclusive). Si es None, no hay máximo.

    Returns:
        float: El valor ingresado por el usuario, validado.
    """
    while True:
        valor_ingresado = input(mensaje)
        try:
            valor = float(valor_ingresado)
            if minimo is not None and valor < minimo:
                print(f"Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Error: El valor debe ser menor o igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Error: Por favor, ingresa un número válido.")


def pedir_hora_jugador(nombre_jugador, hora_fin_cancha=None):
    """
    Solicita la hora de llegada y salida para un jugador, validando que la salida no sea menor que la llegada
    y que no exceda la hora de fin de la cancha si se proporciona.

    Args:
        nombre_jugador (str): Nombre del jugador.
        hora_fin_cancha (float, optional): Hora máxima de salida permitida.

    Returns:
        tuple: (hora_llegada, hora_salida)
    """
    hora_llegada = pedir_float(
        f"Hora in de {nombre_jugador} (ej: 18.0): ",
        minimo=0,
        maximo=hora_fin_cancha,
    )
    while True:
        hora_salida = pedir_float(
            f"Hora out de {nombre_jugador} (ej: 20.0): ",
            minimo=hora_llegada,
            maximo=hora_fin_cancha,
        )
        if hora_salida < hora_llegada:
            print("Error: La hora de salida no puede ser menor que la hora de llegada.")
        else:
            break
    return hora_llegada, hora_salida


def pedir_jugadores(hora_fin_cancha=None):
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
        hora_llegada, hora_salida = pedir_hora_jugador(nombre_jugador, hora_fin_cancha)
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


def mostrar_pagos(lista_pagos, hora_inicio=None, hora_fin=None):
    """
    Muestra los pagos por pantalla en formato amigable para móviles.
    También muestra el total de horas de cancha (hora_fin - hora_inicio) en horas y minutos.
    Destaca quién jugó más y menos tiempo.
    """
    if lista_pagos:
        # Encontrar máximo y mínimo tiempo jugado
        max_tiempo = max(pago["tiempo"] for pago in lista_pagos)
        min_tiempo = min(pago["tiempo"] for pago in lista_pagos)
        print("=== Resumen de Pagos ===")
        for pago in lista_pagos:
            destacado = ""
            if pago["tiempo"] == max_tiempo and max_tiempo != min_tiempo:
                destacado = " (más tiempo)"
            elif pago["tiempo"] == min_tiempo and max_tiempo != min_tiempo:
                destacado = " (menos tiempo)"
            print(f"Jugador: {pago['nombre']}{destacado}")
            print(f"  Pago: ${pago['pago']:,}".replace(",", "."))
            print(f"  Horas jugadas: {pago['tiempo']:.2f}")
            print("-" * 20)
        if hora_inicio is not None and hora_fin is not None:
            total_horas_cancha = hora_fin - hora_inicio
            horas = int(total_horas_cancha)
            minutos = int(round((total_horas_cancha - horas) * 60))
            print(
                f"Total de horas de cancha: {horas}h {minutos}min ({total_horas_cancha:.2f} horas)"
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
        print("Error: La hora de fin no puede ser menor que la hora de inicio.")
        return
    monto_total = pedir_float("Total a pagar ($): ", minimo=0.01)
    jugadores = pedir_jugadores(hora_fin_cancha=hora_fin)
    if not jugadores:
        print("Error: Debes ingresar al menos un jugador.")
        return
    for jugador in jugadores:
        if jugador["llegada"] > jugador["salida"]:
            print(
                f"Error: {jugador['nombre']} tiene hora de llegada mayor que la de salida."
            )
            return
        if jugador["salida"] > hora_fin:
            print(
                f"Advertencia: {jugador['nombre']} tiene hora de salida después del fin de la cancha. Se ajustará a {hora_fin}."
            )
            jugador["salida"] = hora_fin
    lista_pagos = calcular_pagos(jugadores, monto_total, hora_inicio, hora_fin)
    print("\n--- Pagos ---")
    mostrar_pagos(lista_pagos, hora_inicio, hora_fin)


if __name__ == "__main__":
    print("Usa solo números y puntos para las horas. Ejemplo: 18.5 para 18:30")
    main()
