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
    Solicita un número flotante en formato decimal (ej: 18.0, 18.25, 18.5, 18.75).
    No acepta otros formatos como 18:30 ni 18,30.
    """
    ayuda = (
        "\nEjemplos válidos:\n"
        "  18.0   → 18:00\n"
        "  18.25  → 18:15\n"
        "  18.5   → 18:30\n"
        "  18.75  → 18:45\n"
        "Solo se acepta el punto como separador decimal.\n"
    )
    while True:
        valor_ingresado = input(f"{mensaje}\n> ").strip()
        if valor_ingresado == "?":
            print(ayuda)
            continue
        try:
            # Solo acepta punto como separador decimal
            if "," in valor_ingresado or ":" in valor_ingresado:
                raise ValueError
            valor = float(valor_ingresado)
            if minimo is not None and valor < minimo:
                print(f"Error: mínimo {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Error: máximo {maximo}")
                continue
            # Validar que los decimales sean solo .0, .25, .5, .75
            decimales_validos = {0.0, 0.25, 0.5, 0.75}
            parte_decimal = round(valor % 1, 2)
            if parte_decimal not in decimales_validos:
                print(
                    "Solo se permiten decimales .0, .25, .5 o .75 (ej: 18.0, 18.25, 18.5, 18.75)"
                )
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
    print("Jugadores iniciales (4):")
    for i in range(4):
        while True:
            nombre = input(f"Nombre #{i+1}: ").strip()
            if not nombre:
                print("Nombre vacío.")
                continue
            if any(j["nombre"].lower() == nombre.lower() for j in jugadores):
                print("Nombre repetido.")
                continue
            break
        llegada = hora_inicio_cancha
        hasta_el_final = (
            input(f"{nombre.upper()} ¿hasta el final? (s/n): ").strip().lower()
        )
        if hasta_el_final == "s":
            salida = hora_fin_cancha
        else:
            salida = pedir_float(
                f"¿A qué hora se va {nombre.upper()}?: ",
                minimo=llegada,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
        jugadores.append({"nombre": nombre, "llegada": llegada, "salida": salida})

    print("\n¿Agregar más jugadores? (vacío para terminar)")
    while True:
        nombre = input("Nombre (vacío para terminar): ").strip()
        if not nombre:
            break
        if any(j["nombre"].lower() == nombre.lower() for j in jugadores):
            print("Nombre repetido.")
            continue
        llegada = pedir_float(
            f"Llegó {nombre.upper()} (>= {hora_inicio_cancha}): ",
            minimo=hora_inicio_cancha,
            maximo=hora_fin_cancha,
            flexible_hora=True,
        )
        hasta_el_final = (
            input(f"{nombre.upper()} ¿hasta el final? (s/n): ").strip().lower()
        )
        if hasta_el_final == "s":
            salida = hora_fin_cancha
        else:
            salida = pedir_float(
                f"¿A qué hora se va {nombre.upper()}?: ",
                minimo=llegada,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
        jugadores.append({"nombre": nombre, "llegada": llegada, "salida": salida})

    # Edición rápida antes de calcular con menú numérico
    while jugadores:
        print("\nJugadores:")
        for idx, j in enumerate(jugadores, 1):
            print(f"{idx}. {j['nombre'].upper()} {j['llegada']}→{j['salida']}")
        print("0. Continuar")
        seleccion = input("Nro a editar/eliminar (0 para seguir): ").strip()
        if seleccion == "0":
            break
        if not seleccion.isdigit() or not (1 <= int(seleccion) <= len(jugadores)):
            print("Opción inválida.")
            continue
        seleccionado = jugadores[int(seleccion) - 1]
        print(
            f"1. Editar nombre\n2. Editar llegada\n3. Editar salida\n4. Eliminar jugador\n0. Volver"
        )
        accion = input("Elige opción: ").strip()
        if accion == "1":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre and not any(
                j["nombre"].lower() == nuevo_nombre.lower() for j in jugadores
            ):
                seleccionado["nombre"] = nuevo_nombre
            else:
                print("Nombre inválido o repetido.")
        elif accion == "2":
            nuevo_llegada = pedir_float(
                f"Llegada {seleccionado['nombre'].upper()}: ",
                minimo=hora_inicio_cancha,
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
            if nuevo_llegada > seleccionado["salida"]:
                print("Llegada > salida.")
            else:
                seleccionado["llegada"] = nuevo_llegada
        elif accion == "3":
            nuevo_salida = pedir_float(
                f"Salida {seleccionado['nombre'].upper()}: ",
                minimo=seleccionado["llegada"],
                maximo=hora_fin_cancha,
                flexible_hora=True,
            )
            if nuevo_salida < seleccionado["llegada"]:
                print("Salida < llegada.")
            else:
                seleccionado["salida"] = nuevo_salida
        elif accion == "4":
            if len(jugadores) <= 4:
                print("No puedes eliminar iniciales.")
            else:
                jugadores.pop(int(seleccion) - 1)
                print("Eliminado.")
        elif accion == "0":
            continue
        else:
            print("Opción inválida.")
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
    Muestra los pagos por pantalla en formato breve y claro, adaptado a móviles.
    """
    if not lista_pagos:
        print("Sin jugadores.")
        return

    max_tiempo = max(pago["tiempo"] for pago in lista_pagos)
    min_tiempo = min(pago["tiempo"] for pago in lista_pagos)
    max_nombre = max(len(p["nombre"]) for p in lista_pagos)

    print("\n=== RESUMEN ===")
    for i, pago in enumerate(lista_pagos):
        marca = ""
        if pago["tiempo"] == max_tiempo and max_tiempo != min_tiempo:
            marca = " ★"
        elif pago["tiempo"] == min_tiempo and max_tiempo != min_tiempo:
            marca = " →"
        print(
            f"{pago['nombre'].upper().ljust(max_nombre)} {pago['pago']:>6.0f} {pago['tiempo']:>5.2f}{marca}"
        )
        if pagos_detallados:
            pago_exact = pagos_detallados[i]["pago"]
            print(f"  Exacto: ${pago_exact:.2f}")

    if hora_inicio is not None and hora_fin is not None:
        total_horas_cancha = hora_fin - hora_inicio
        horas = int(total_horas_cancha)
        minutos = int(round((total_horas_cancha - horas) * 60))
        print(f"Cancha: {horas}h {minutos}min ({total_horas_cancha:.2f}h)")

    suma_pagos = sum(p["pago"] for p in lista_pagos)
    print(f"Total: ${suma_pagos:.0f}")

    if monto_total is not None and suma_pagos != round(monto_total):
        print(f"¡Atención! Suma ≠ total (${monto_total:.0f})")


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
