import math
import re


def parsear_hora(valor):
    """
    Convierte una entrada de hora en formato decimal (ej: 18.25, 18.5, 18.75, 18)
    a decimal de horas. 18.25 = 18hs 15min, 18.5 = 18hs 30min, 18.75 = 18hs 45min, 18 = 18hs.
    Solo acepta el punto como separador decimal.
    """
    valor = valor.strip()
    if "," in valor or ":" in valor:
        raise ValueError("Solo se acepta el punto como separador decimal.")
    if valor.isdigit():
        return float(valor)
    try:
        partes = valor.split(".")
        horas = int(partes[0])
        minutos = int(partes[1]) if len(partes) > 1 else 0
        # Si los minutos son 25, 5, 50, 75, los convertimos a minutos reales
        if minutos == 25:
            minutos = 15
        elif minutos == 5:
            minutos = 3
        elif minutos == 50:
            minutos = 30
        elif minutos == 75:
            minutos = 45
        if minutos < 0 or minutos >= 60:
            raise ValueError("Los minutos deben estar entre 0 y 59.")
        return horas + minutos / 60
    except Exception:
        raise ValueError(
            "Formato de hora no reconocido. Usa por ejemplo 18.25 para 18:15, 18.5 para 18:30, 18.75 para 18:45."
        )


def pedir_float(mensaje, minimo=None, maximo=None, flexible_hora=False):
    """
    Solicita un número flotante en formato decimal (ej: 18.05, 18.10, 18.15, ..., 18.55).
    Solo acepta el punto como separador decimal y minutos deben ser múltiplos de 5 (00, 05, 10, ..., 55).
    """
    ayuda = (
        "\nEjemplos válidos:\n"
        "  18.00  → 18:00\n"
        "  18.05  → 18:05\n"
        "  18.10  → 18:10\n"
        "  18.15  → 18:15\n"
        "  18.20  → 18:20\n"
        "  18.25  → 18:25\n"
        "  ...\n"
        "  18.55  → 18:55\n"
        "Solo se acepta el punto como separador decimal y minutos múltiplos de 5.\n"
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
            # Validar que los minutos sean múltiplos de 5
            parte_decimal = round(valor % 1, 2)
            minutos = int(round(parte_decimal * 100))
            if minutos < 0 or minutos >= 60 or minutos % 5 != 0:
                print(
                    "Solo se permiten minutos múltiplos de 5 (ej: 18.00, 18.05, ..., 18.55)"
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
        seleccion = input("Nro a editar/eliminar (0 para seguir): ")

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


def calcular_pagos_por_intervalos(jugadores, monto_total, hora_inicio, hora_fin):
    """
    Calcula el pago de cada jugador prorrateando por intervalos según la cantidad de jugadores presentes en cada tramo.
    """
    # 1. Obtener todos los puntos de cambio (llegadas y salidas)
    eventos = []
    for j in jugadores:
        eventos.append((j["llegada"], "in", j["nombre"]))
        eventos.append((j["salida"], "out", j["nombre"]))
    eventos = sorted(eventos)

    # 2. Recorrer los intervalos y calcular el costo de cada uno
    intervalos = []
    jugadores_en_cancha = set()
    ultimo_tiempo = hora_inicio
    for tiempo, tipo, nombre in eventos:
        if tiempo > ultimo_tiempo and jugadores_en_cancha:
            intervalo = {
                "inicio": ultimo_tiempo,
                "fin": tiempo,
                "duracion": tiempo - ultimo_tiempo,
                "jugadores": jugadores_en_cancha.copy(),
            }
            intervalos.append(intervalo)
        if tipo == "in":
            jugadores_en_cancha.add(nombre)
        else:
            jugadores_en_cancha.discard(nombre)
        ultimo_tiempo = tiempo

    # 3. Calcular el costo por hora
    duracion_total = hora_fin - hora_inicio
    costo_por_hora = monto_total / duracion_total if duracion_total > 0 else 0

    # 4. Inicializar pagos
    pagos = {j["nombre"]: 0 for j in jugadores}

    # 5. Sumar a cada jugador lo que le corresponde por cada intervalo
    for intervalo in intervalos:
        if not intervalo["jugadores"]:
            continue
        costo_intervalo = intervalo["duracion"] * costo_por_hora
        pago_por_jugador = costo_intervalo / len(intervalo["jugadores"])
        for nombre in intervalo["jugadores"]:
            pagos[nombre] += pago_por_jugador

    # 6. Preparar la salida en el mismo formato que antes
    pagos_detallados = []
    pagos_redondeados = []
    suma_pagos_redondeados = 0
    nombres_orden = [j["nombre"] for j in jugadores]
    for nombre in nombres_orden:
        pago = pagos[nombre]
        tiempo = sum(
            intervalo["duracion"]
            for intervalo in intervalos
            if nombre in intervalo["jugadores"]
        )
        pagos_detallados.append({"nombre": nombre, "pago": pago, "tiempo": tiempo})

    for i, info in enumerate(pagos_detallados):
        if i < len(pagos_detallados) - 1:
            pago_redondeado = round(info["pago"])
            pagos_redondeados.append(
                {
                    "nombre": info["nombre"],
                    "pago": pago_redondeado,
                    "tiempo": info["tiempo"],
                }
            )
            suma_pagos_redondeados += pago_redondeado
        else:
            pago_redondeado = round(monto_total - suma_pagos_redondeados)
            pagos_redondeados.append(
                {
                    "nombre": info["nombre"],
                    "pago": pago_redondeado,
                    "tiempo": info["tiempo"],
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
            "Hora de inicio de la cancha (ej: 18.0, 18.25, 18.5, 18.75): ",
            minimo=0,
            flexible_hora=True,
        )
        hora_fin = pedir_float(
            "Hora de fin de la cancha (ej: 20.0, 20.25, 20.5, 20.75): ",
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

        lista_pagos, pagos_detallados = calcular_pagos_por_intervalos(
            jugadores, monto_total, hora_inicio, hora_fin
        )

        # Validar suma de tiempos
        suma_tiempos = sum(info["tiempo"] for info in pagos_detallados)
        if suma_tiempos == 0:
            print(
                "Error: La suma de tiempos jugados es cero. Debes ingresar datos válidos."
            )
            continue

        print("\n--- Pagos ---")
        mostrar_pagos(lista_pagos, hora_inicio, hora_fin, pagos_detallados, monto_total)

        # Preguntar si desea volver a ejecutar o salir
        reiniciar = input("\n¿Deseas ingresar nuevos datos? (s/n): ").strip().lower()
        if reiniciar != "s":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    print(
        "Usa solo números y puntos para las horas. Ejemplo: 18.25 para 18:15, 18.5 para 18:30"
    )
    main()
