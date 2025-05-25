import math
import re


def parsear_hora(valor):
    """
    Convierte una entrada de hora flexible (18.5, 18:30, 18,30, 18.30) a decimal de horas.
    """
    valor = valor.strip().replace(",", ".")
    # Si es formato 18.5 o 18.30 (con punto decimal)
    if re.match(r"^\d{1,2}\.\d{1,2}$", valor):
        partes = valor.split(".")
        horas = int(partes[0])
        minutos = int(partes[1])
        if minutos >= 60:
            raise ValueError("Los minutos deben ser menores a 60.")
        return horas + minutos / 60
    # Si es formato 18:30
    elif ":" in valor:
        partes = valor.split(":")
        horas = int(partes[0])
        minutos = int(partes[1])
        if minutos >= 60:
            raise ValueError("Los minutos deben ser menores a 60.")
        return horas + minutos / 60
    # Si es solo un número entero (ej: 18)
    elif valor.isdigit():
        return float(valor)
    else:
        # Intentar convertir directamente (por si es 18.5)
        try:
            return float(valor)
        except Exception:
            raise ValueError("Formato de hora no reconocido.")


def pedir_float(mensaje, minimo=None, maximo=None, flexible_hora=False):
    """
    Solicita al usuario un número flotante por consola, validando rango.
    Si flexible_hora=True, permite formatos de hora flexibles y los convierte a decimal.
    Mensajes cortos y claros.
    """
    while True:
        valor_ingresado = input(f"{mensaje}\n> ")
        try:
            if flexible_hora:
                valor = parsear_hora(valor_ingresado)
            else:
                valor = float(valor_ingresado.replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"Error: mínimo {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Error: máximo {maximo}")
                continue
            return valor
        except Exception as e:
            print("Formato inválido. Ej: 18.15 o 18:15")


def pedir_hora_jugador(nombre_jugador, hora_inicio_cancha=None, hora_fin_cancha=None):
    """
    Solicita la hora de llegada y salida para un jugador, con mensajes breves.
    """
    # Hora de llegada
    if hora_inicio_cancha is not None:
        usar_inicio = (
            input(
                f"{nombre_jugador.upper()} ¿Llegó al inicio ({hora_inicio_cancha})? (s/n): "
            )
            .strip()
            .lower()
        )
        if usar_inicio == "s":
            hora_llegada = hora_inicio_cancha
        else:
            hora_llegada = pedir_float(
                f"Hora llegada {nombre_jugador} (ej: 18.15 o 18:15):",
                minimo=hora_inicio_cancha,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
    else:
        hora_llegada = pedir_float(
            f"Hora llegada {nombre_jugador} (ej: 18.15 o 18:15):",
            minimo=hora_inicio_cancha,
            maximo=hora_fin_cancha,
            flexible_hora=True,
        )

    # Hora de salida
    if hora_fin_cancha is not None:
        usar_fin = (
            input(
                f"{nombre_jugador.upper()} ¿Se fue al final ({hora_fin_cancha})? (s/n): "
            )
            .strip()
            .lower()
        )
        if usar_fin == "s":
            hora_salida = hora_fin_cancha
        else:
            while True:
                hora_salida = pedir_float(
                    f"Hora salida {nombre_jugador} (ej: 19.45 o 19:45):",
                    minimo=hora_llegada,
                    maximo=hora_fin_cancha,
                    flexible_hora=True,
                )
                if hora_salida < hora_llegada:
                    print("Error: salida < llegada")
                else:
                    break
    else:
        while True:
            hora_salida = pedir_float(
                f"Hora salida {nombre_jugador} (ej: 19.45 o 19:45):",
                minimo=hora_llegada,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
            if hora_salida < hora_llegada:
                print("Error: salida < llegada")
            else:
                break

    return hora_llegada, hora_salida


def pedir_jugadores(hora_inicio_cancha=None, hora_fin_cancha=None):
    """
    Solicita al usuario los datos de los jugadores (nombre, hora de llegada y salida).
    Permite editar los datos antes de calcular los pagos.
    Returns:
        list: Lista de diccionarios con los datos de cada jugador.
    """
    jugadores = []
    while True:
        nombre_jugador = input("Nombre del jugador (deja vacío para terminar): ")
        if not nombre_jugador:
            break
        hora_llegada, hora_salida = pedir_hora_jugador(
            nombre_jugador, hora_inicio_cancha, hora_fin_cancha
        )
        jugadores.append(
            {"nombre": nombre_jugador, "llegada": hora_llegada, "salida": hora_salida}
        )

    # Confirmación y edición fácil
    while jugadores:
        print("\nResumen de jugadores ingresados:")
        for idx, j in enumerate(jugadores, 1):
            print(
                f"{idx}. {j['nombre'].upper()} - Llegada: {j['llegada']} - Salida: {j['salida']}"
            )
        opcion = input("¿Deseas corregir algún dato? (s/n): ").strip().lower()
        if opcion != "s":
            break
        seleccion = input("Ingresa el número o nombre del jugador a editar: ").strip()
        seleccionado = None
        # Buscar por número
        if seleccion.isdigit():
            idx = int(seleccion) - 1
            if 0 <= idx < len(jugadores):
                seleccionado = jugadores[idx]
        # Buscar por nombre
        else:
            for j in jugadores:
                if j["nombre"].lower() == seleccion.lower():
                    seleccionado = j
                    break
        if not seleccionado:
            print("Jugador no encontrado.")
            continue
        # Elegir campo a editar
        campo = input("¿Qué deseas editar? (nombre/llegada/salida): ").strip().lower()
        if campo == "nombre":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre:
                seleccionado["nombre"] = nuevo_nombre
        elif campo == "llegada":
            nuevo_llegada, _ = pedir_hora_jugador(
                seleccionado["nombre"], hora_inicio_cancha, hora_fin_cancha
            )
            seleccionado["llegada"] = nuevo_llegada
        elif campo == "salida":
            _, nuevo_salida = pedir_hora_jugador(
                seleccionado["nombre"], hora_inicio_cancha, hora_fin_cancha
            )
            seleccionado["salida"] = nuevo_salida
        else:
            print("Campo no válido. Usa: nombre, llegada o salida.")
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
    return pagos_redondeados, pagos_detallados


def mostrar_pagos(lista_pagos, hora_inicio=None, hora_fin=None, pagos_detallados=None):
    """
    Muestra los pagos por pantalla en formato breve y claro.
    También muestra el total de horas de cancha (hora_fin - hora_inicio) en horas y minutos.
    Destaca quién jugó más y menos tiempo.
    Si se proveen los pagos_detallados, muestra el pago exacto antes de redondear.
    """
    if lista_pagos:
        # Encontrar máximo y mínimo tiempo jugado
        max_tiempo = max(pago["tiempo"] for pago in lista_pagos)
        min_tiempo = min(pago["tiempo"] for pago in lista_pagos)
        print("=== Pagos ===")
        for i, pago in enumerate(lista_pagos):
            destacado = ""
            if pago["tiempo"] == max_tiempo and max_tiempo != min_tiempo:
                destacado = " (más tiempo)"
            elif pago["tiempo"] == min_tiempo and max_tiempo != min_tiempo:
                destacado = " (menos tiempo)"
            print(
                f"{pago['nombre'].upper()}: ${pago['pago']} - {pago['tiempo']:.2f}h{destacado}"
            )
        if hora_inicio is not None and hora_fin is not None:
            total_horas_cancha = hora_fin - hora_inicio
            horas = int(total_horas_cancha)
            minutos = int(round((total_horas_cancha - horas) * 60))
            print(f"Cancha: {horas}h {minutos}min ({total_horas_cancha:.2f}h)")
    else:
        print("Sin jugadores.")


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
    jugadores = pedir_jugadores(
        hora_inicio_cancha=hora_inicio, hora_fin_cancha=hora_fin
    )
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
    lista_pagos, pagos_detallados = calcular_pagos(
        jugadores, monto_total, hora_inicio, hora_fin
    )
    print("\n--- Pagos ---")
    mostrar_pagos(lista_pagos, hora_inicio, hora_fin, pagos_detallados)


if __name__ == "__main__":
    print("Usa solo números y puntos para las horas. Ejemplo: 18.5 para 18:30")
    main()
