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
    Solicita un número flotante o una hora flexible, con ayuda rápida y mensajes cortos.
    """
    ayuda = (
        "\nEjemplos:\n"
        "  18.5   → 18:30\n"
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
                print(f"Error: mínimo {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Error: máximo {maximo}")
                continue
            return valor
        except Exception:
            print("Formato inválido. Escribe '?' para ayuda.")


def pedir_jugadores(hora_inicio_cancha, hora_fin_cancha):
    """
    Carga los 4 jugadores iniciales (deben estar desde el inicio) y permite agregar más.
    Para los 4 iniciales, llegada = hora de inicio. Permite editar antes de calcular.
    """
    jugadores = []
    print("Carga los 4 jugadores iniciales (deben estar desde el inicio):")
    for i in range(4):
        while True:
            nombre = input(f"Nombre jugador #{i+1}: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue
            if any(j["nombre"].lower() == nombre.lower() for j in jugadores):
                print("Ese nombre ya fue ingresado. Usa otro.")
                continue
            break
        llegada = hora_inicio_cancha
        hasta_el_final = (
            input(
                f"{nombre.upper()} ¿se queda hasta el final ({hora_fin_cancha})? (s/n): "
            )
            .strip()
            .lower()
        )
        if hasta_el_final == "s":
            salida = hora_fin_cancha
        else:
            salida = pedir_float(
                f"¿A qué hora se va {nombre.upper()}? (ej: {hora_fin_cancha}): ",
                minimo=llegada,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
        jugadores.append({"nombre": nombre, "llegada": llegada, "salida": salida})

    print("\n¿Hay jugadores que se suman después del inicio?")
    while True:
        nombre = input("Nombre jugador adicional (vacío para terminar): ").strip()
        if not nombre:
            break
        if any(j["nombre"].lower() == nombre.lower() for j in jugadores):
            print("Ese nombre ya fue ingresado. Usa otro.")
            continue
        llegada = pedir_float(
            f"¿A qué hora llega {nombre.upper()}? (>= {hora_inicio_cancha}): ",
            minimo=hora_inicio_cancha,
            maximo=hora_fin_cancha,
            flexible_hora=True,
        )
        hasta_el_final = (
            input(
                f"{nombre.upper()} ¿se queda hasta el final ({hora_fin_cancha})? (s/n): "
            )
            .strip()
            .lower()
        )
        if hasta_el_final == "s":
            salida = hora_fin_cancha
        else:
            salida = pedir_float(
                f"¿A qué hora se va {nombre.upper()}? (ej: {hora_fin_cancha}): ",
                minimo=llegada,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
        jugadores.append({"nombre": nombre, "llegada": llegada, "salida": salida})

    # Edición fácil antes de calcular
    while jugadores:
        print("\nJugadores:")
        for idx, j in enumerate(jugadores, 1):
            print(
                f"{idx}. {j['nombre'].upper()} - Llegada: {j['llegada']} - Salida: {j['salida']}"
            )
        opcion = input("¿Corregir algún dato? (s/n): ").strip().lower()
        if opcion != "s":
            break
        seleccion = input("Nro o nombre a editar: ").strip()
        seleccionado = None
        if seleccion.isdigit():
            idx = int(seleccion) - 1
            if 0 <= idx < len(jugadores):
                seleccionado = jugadores[idx]
        else:
            for j in jugadores:
                if j["nombre"].lower() == seleccion.lower():
                    seleccionado = j
                    break
        if not seleccionado:
            print("No encontrado.")
            continue
        campo = input("¿Editar nombre/llegada/salida/eliminar?: ").strip().lower()
        if campo == "nombre":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre and not any(
                j["nombre"].lower() == nuevo_nombre.lower() for j in jugadores
            ):
                seleccionado["nombre"] = nuevo_nombre
            else:
                print("Nombre inválido o repetido.")
        elif campo == "llegada":
            nuevo_llegada = pedir_float(
                f"Nueva llegada para {seleccionado['nombre'].upper()} (ej: {hora_inicio_cancha}):",
                minimo=hora_inicio_cancha,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
            if nuevo_llegada > seleccionado["salida"]:
                print("La llegada no puede ser después de la salida.")
            else:
                seleccionado["llegada"] = nuevo_llegada
        elif campo == "salida":
            nuevo_salida = pedir_float(
                f"Nueva salida para {seleccionado['nombre'].upper()} (ej: {hora_fin_cancha}):",
                minimo=seleccionado["llegada"],
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
            if nuevo_salida < seleccionado["llegada"]:
                print("La salida no puede ser antes de la llegada.")
            else:
                seleccionado["salida"] = nuevo_salida
        elif campo == "eliminar":
            if len(jugadores) <= 4:
                print(
                    "No puedes eliminar jugadores iniciales. Debe haber al menos 4 jugadores."
                )
            else:
                jugadores.remove(seleccionado)
                print("Jugador eliminado.")
        else:
            print("Campo no válido.")
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
    Muestra el total recaudado y advierte si hay diferencia por redondeo.
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
    # Ajustar ancho para columnas de pago y horas
    ancho_pago = max(
        12, max(len(f"{p['pago']:,.0f}".replace(",", ".")) for p in lista_pagos) + 2
    )
    ancho_horas = max(5, max(len(f"{p['tiempo']:.2f}") for p in lista_pagos))

    print("\n=== RESUMEN ===")
    print(
        f"{'JUGADOR'.ljust(max_nombre)} | {'PAGO':>{ancho_pago}} | {'HORAS':>{ancho_horas}}"
    )
    print("-" * (max_nombre + ancho_pago + ancho_horas + 7))

    suma_pagos = 0

    for i, pago in enumerate(lista_pagos):
        nombre = pago["nombre"].upper().ljust(max_nombre)
        monto = f"${pago['pago']:,.0f}".replace(",", ".").rjust(ancho_pago)
        horas = f"{pago['tiempo']:.2f}".rjust(ancho_horas)
        suma_pagos += pago["pago"]

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
        # Mostrar pago exacto antes de redondear si está disponible
        if pagos_detallados:
            pago_exact = pagos_detallados[i]["pago"]
            print(f"    Pago exacto antes de redondear: ${pago_exact:.2f}")

    print("-" * (max_nombre + ancho_pago + ancho_horas + 7))
    if hora_inicio is not None and hora_fin is not None:
        total_horas_cancha = hora_fin - hora_inicio
        horas = int(total_horas_cancha)
        minutos = int(round((total_horas_cancha - horas) * 60))
        print(f"Cancha: {horas}h {minutos}min ({total_horas_cancha:.2f}h)")

    # Formatea el total recaudado con separador de miles
    print(f"Total recaudado: ${suma_pagos:,.0f}".replace(",", "."))

    # Advertencia si la suma de pagos no coincide exactamente con el monto total
    if monto_total is not None and suma_pagos != round(monto_total):
        print(
            f"{COLOR_YELLOW}Advertencia: La suma de pagos (${suma_pagos:,.0f}) no coincide con el monto total (${monto_total:,.0f}).{COLOR_RESET}".replace(
                ",", "."
            )
        )


def main():
    """
    Función principal. Solicita los datos, calcula y muestra los pagos.
    Incluye validaciones proactivas.
    """
    print("=== Paddle Split ===")
    while True:
        # Permitir formatos flexibles para hora de inicio y fin de cancha
        hora_inicio = pedir_float(
            "Hora de inicio de la cancha (ej: 18.0, 18:30, 18,5, 18.5, 18,30): ",
            minimo=0,
            flexible_hora=True,
        )
        hora_fin = pedir_float(
            "Hora de fin de la cancha (ej: 20.0, 20:30, 20,5, 20.5, 20,30): ",
            minimo=hora_inicio,
            flexible_hora=True,
        )
        if hora_fin < hora_inicio:
            print("Error: La hora de fin no puede ser menor que la hora de inicio.")
            continue
        monto_total = pedir_float("Total a pagar ($): ", minimo=0.01)
        jugadores = pedir_jugadores(
            hora_inicio_cancha=hora_inicio, hora_fin_cancha=hora_fin
        )
        if not jugadores or len(jugadores) < 4:
            print("Error: Debes ingresar al menos 4 jugadores.")
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
