import math
import re


def parsear_hora(valor):
    """
    Convierte una entrada de hora flexible a decimal de horas.
    Permite: 18.5, 18.50, 18:30, 18,30, 18 (asume minutos=0 si solo hora).
    Acepta punto, coma o dos puntos como separador.
    """
    valor = valor.strip().replace(",", ".")
    # Si es solo un número entero (ej: 18)
    if valor.isdigit():
        return float(valor)
    # Si es formato 18.5, 18.50, 18.30, 18:30
    if ":" in valor:
        partes = valor.split(":")
    elif "." in valor:
        partes = valor.split(".")
    else:
        partes = [valor]

    try:
        horas = int(partes[0])
        minutos = int(partes[1]) if len(partes) > 1 else 0
        if minutos >= 60:
            raise ValueError("Los minutos deben ser menores a 60.")
        return horas + minutos / 60
    except Exception:
        raise ValueError("Formato de hora no reconocido.")


def pedir_float(mensaje, minimo=None, maximo=None, flexible_hora=False):
    """
    Solicita al usuario un número flotante por consola, validando rango.
    Si flexible_hora=True, permite formatos de hora flexibles y los convierte a decimal.
    Permite ingresar '?' para mostrar ayuda rápida.
    """
    ayuda = (
        "\nEjemplos válidos:\n"
        "  18.5   → 18:30\n"
        "  18.50  → 18:50\n"
        "  18:30  → 18:30\n"
        "  18,30  → 18:30\n"
        "  18     → 18:00\n"
        "Usa punto, coma o dos puntos como separador.\n"
    )
    while True:
        valor_ingresado = input(f"{mensaje}\n> ").strip()
        if valor_ingresado == "?":
            print(ayuda)
            continue
        try:
            if flexible_hora:
                valor = parsear_hora(valor_ingresado)
            else:
                valor = float(valor_ingresado.replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"Error: mínimo {minimo}. Escribe '?' para ver ejemplos.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Error: máximo {maximo}. Escribe '?' para ver ejemplos.")
                continue
            return valor
        except Exception:
            print("Formato inválido. Escribe '?' para ver ejemplos y sugerencias.")


def pedir_hora_jugador(nombre_jugador, hora_inicio_cancha=None, hora_fin_cancha=None):
    """
    Solicita la hora de llegada y salida para un jugador, con mensajes breves y validaciones proactivas.
    Si la hora de llegada es igual a la de salida, advierte y pide confirmación.
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
                elif hora_salida == hora_llegada:
                    confirm = (
                        input("Llegada y salida son iguales, ¿confirmar? (s/n): ")
                        .strip()
                        .lower()
                    )
                    if confirm == "s":
                        break
                    else:
                        print("Vuelve a ingresar la hora de salida.")
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
            elif hora_salida == hora_llegada:
                confirm = (
                    input("Llegada y salida son iguales, ¿confirmar? (s/n): ")
                    .strip()
                    .lower()
                )
                if confirm == "s":
                    break
                else:
                    print("Vuelve a ingresar la hora de salida.")
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


def mostrar_pagos(
    lista_pagos,
    hora_inicio=None,
    hora_fin=None,
    pagos_detallados=None,
    monto_total=None,
):
    """
    Muestra los pagos por pantalla en formato breve y claro, adaptado a pantallas chicas.
    Tabla simple y alineada, resaltando el jugador que más y menos jugó con colores si la terminal lo permite.
    Muestra el total recaudado, total de horas jugadas y advierte si hay diferencia por redondeo.
    """
    # ANSI colors
    COLOR_RESET = "\033[0m"
    COLOR_GREEN = "\033[92m"
    COLOR_RED = "\033[91m"
    COLOR_YELLOW = "\033[93m"

    if not lista_pagos:
        print("Sin jugadores.")
        return

    max_tiempo = max(pago["tiempo"] for pago in lista_pagos)
    min_tiempo = min(pago["tiempo"] for pago in lista_pagos)
    max_nombre = max(len(p["nombre"]) for p in lista_pagos)
    print("\n=== RESUMEN ===")
    print(f"{'JUGADOR'.ljust(max_nombre)} | {'PAGO':>6} | {'HORAS':>5}")
    print("-" * (max_nombre + 17))

    suma_pagos = 0
    suma_horas = 0

    for pago in lista_pagos:
        nombre = pago["nombre"].upper().ljust(max_nombre)
        monto = f"${pago['pago']}".rjust(6)
        horas = f"{pago['tiempo']:.2f}".rjust(5)
        suma_pagos += pago["pago"]
        suma_horas += pago["tiempo"]

        # Colores para el que más y menos jugó
        if pago["tiempo"] == max_tiempo and max_tiempo != min_tiempo:
            color = COLOR_GREEN
            marca = " << MÁS"
        elif pago["tiempo"] == min_tiempo and max_tiempo != min_tiempo:
            color = COLOR_RED
            marca = " << MENOS"
        else:
            color = COLOR_RESET
            marca = ""
        print(f"{color}{nombre} | {monto} | {horas}{marca}{COLOR_RESET}")

    print("-" * (max_nombre + 17))
    if hora_inicio is not None and hora_fin is not None:
        total_horas_cancha = hora_fin - hora_inicio
        horas = int(total_horas_cancha)
        minutos = int(round((total_horas_cancha - horas) * 60))
        print(f"Cancha: {horas}h {minutos}min ({total_horas_cancha:.2f}h)")

    print(f"Total recaudado: ${suma_pagos}")
    print(f"Total horas jugadas: {suma_horas:.2f}")

    # Advertencia si la suma de pagos no coincide exactamente con el monto total
    if monto_total is not None and suma_pagos != round(monto_total):
        print(
            f"{COLOR_YELLOW}Advertencia: La suma de pagos (${suma_pagos}) no coincide con el monto total (${monto_total}).{COLOR_RESET}"
        )


def main():
    """
    Función principal. Solicita los datos, calcula y muestra los pagos.
    Incluye validaciones proactivas.
    """
    print("=== Paddle Split ===")
    while True:
        hora_inicio = pedir_float("Hora de inicio de la cancha (ej: 18.0): ", minimo=0)
        hora_fin = pedir_float(
            "Hora de fin de la cancha (ej: 20.0): ", minimo=hora_inicio
        )
        if hora_fin < hora_inicio:
            print("Error: La hora de fin no puede ser menor que la hora de inicio.")
            continue
        monto_total = pedir_float("Total a pagar ($): ", minimo=0.01)
        jugadores = pedir_jugadores(
            hora_inicio_cancha=hora_inicio, hora_fin_cancha=hora_fin
        )
        if not jugadores:
            print("Error: Debes ingresar al menos un jugador.")
            continue

        # Advertir si algún jugador no jugó tiempo
        jugadores_sin_tiempo = [
            j["nombre"] for j in jugadores if j["llegada"] == j["salida"]
        ]
        if jugadores_sin_tiempo:
            print(
                "Advertencia: Los siguientes jugadores no tienen tiempo jugado (llegada = salida):"
            )
            for nombre in jugadores_sin_tiempo:
                print(f"- {nombre.upper()}")
            seguir = input("¿Deseas continuar igual? (s/n): ").strip().lower()
            if seguir != "s":
                continue

        for jugador in jugadores:
            if jugador["llegada"] > jugador["salida"]:
                print(
                    f"Error: {jugador['nombre']} tiene hora de llegada mayor que la de salida."
                )
                break
            if jugador["salida"] > hora_fin:
                print(
                    f"Advertencia: {jugador['nombre']} tiene hora de salida después del fin de la cancha. Se ajustará a {hora_fin}."
                )
                jugador["salida"] = hora_fin

        lista_pagos, pagos_detallados = calcular_pagos(
            jugadores, monto_total, hora_inicio, hora_fin
        )

        # Validar suma de tiempos
        suma_tiempos = sum(p["tiempo"] for p in lista_pagos)
        if suma_tiempos == 0:
            print(
                "Error: La suma de tiempos jugados es cero. Debes ingresar datos válidos."
            )
            continue

        print("\n--- Pagos ---")
        mostrar_pagos(lista_pagos, hora_inicio, hora_fin, pagos_detallados, monto_total)
        break


if __name__ == "__main__":
    print("Usa solo números y puntos para las horas. Ejemplo: 18.5 para 18:30")
    main()
