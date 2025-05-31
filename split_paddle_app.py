import streamlit as st


def parsear_hora(valor):
    """
    Convierte una entrada de hora en formato flexible:
    - 18      → 18.0
    - 18.15   → 18.25
    - 18.30   → 18.5
    - 18.45   → 18.75
    - 18.00   → 18.0
    """
    valor = str(valor).strip()
    if not valor:
        return None
    if "," in valor or ":" in valor:
        st.error("Solo se acepta el punto como separador decimal.")
        return None
    try:
        partes = valor.split(".")
        horas = int(partes[0])
        minutos = int(partes[1]) if len(partes) > 1 else 0
        if minutos not in (0, 15, 30, 45):
            st.error("Minutos válidos: 00, 15, 30, 45.")
            return None
        # Convierte minutos a fracción decimal
        minutos_decimal = {0: 0, 15: 0.25, 30: 0.5, 45: 0.75}[minutos]
        return horas + minutos_decimal
    except Exception:
        return None


def calcular_pagos_por_intervalos(jugadores, monto_total, hora_inicio, hora_fin):
    """
    Calcula el pago de cada jugador prorrateando por intervalos según la cantidad de jugadores presentes en cada tramo.
    """
    eventos = []
    for j in jugadores:
        if j["nombre"] and j["llegada"] is not None and j["salida"] is not None:
            eventos.append((j["llegada"], "in", j["nombre"]))
            eventos.append((j["salida"], "out", j["nombre"]))
    eventos = sorted(eventos)
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
    duracion_total = hora_fin - hora_inicio
    costo_por_hora = monto_total / duracion_total if duracion_total > 0 else 0
    pagos = {j["nombre"]: 0 for j in jugadores if j["nombre"]}
    for intervalo in intervalos:
        if not intervalo["jugadores"]:
            continue
        costo_intervalo = intervalo["duracion"] * costo_por_hora
        pago_por_jugador = costo_intervalo / len(intervalo["jugadores"])
        for nombre in intervalo["jugadores"]:
            pagos[nombre] += pago_por_jugador
    pagos_detallados = []
    for j in jugadores:
        if j["nombre"]:
            tiempo = sum(
                intervalo["duracion"]
                for intervalo in intervalos
                if j["nombre"] in intervalo["jugadores"]
            )
            pagos_detallados.append(
                {"nombre": j["nombre"], "pago": pagos[j["nombre"]], "tiempo": tiempo}
            )
    return pagos_detallados


def mostrar_pagos_streamlit(pagos_detallados, hora_inicio, hora_fin, monto_total):
    st.subheader("Pagos por jugador")
    if not pagos_detallados:
        st.info("Sin jugadores.")
        return

    max_tiempo = max(p["tiempo"] for p in pagos_detallados)
    min_tiempo = min(p["tiempo"] for p in pagos_detallados)
    suma_pagos = 0

    for pago in pagos_detallados:
        marca = ""
        if pago["tiempo"] == max_tiempo and max_tiempo != min_tiempo:
            marca = " (más tiempo)"
        elif pago["tiempo"] == min_tiempo and max_tiempo != min_tiempo:
            marca = " (menos tiempo)"
        horas = int(pago["tiempo"])
        minutos = int(round((pago["tiempo"] - horas) * 60))
        tiempo_str = f"{horas}h {minutos:02d}m"
        pago_redondeado = round(pago["pago"])
        suma_pagos += pago["pago"]

        # Tarjeta amigable para móvil
        st.markdown(
            f"""
            <div style="border:1px solid #ddd; border-radius:8px; padding:10px; margin-bottom:10px; background:#fafafa;">
                <b>{pago['nombre'].upper()}</b> {marca}<br>
                <span style="color:#444;">Pago:</span> <b>${pago_redondeado:,.0f}</b><br>
                <span style="color:#444;">(Exacto: ${pago['pago']:,.2f})</span><br>
                <span style="color:#444;">Tiempo:</span> {tiempo_str}
            </div>
            """,
            unsafe_allow_html=True,
        )

    total_horas_cancha = hora_fin - hora_inicio
    horas = int(total_horas_cancha)
    minutos = int(round((total_horas_cancha - horas) * 60))
    st.markdown(
        f"<b>Cancha:</b> {horas}h {minutos}m ({total_horas_cancha:.2f}h)",
        unsafe_allow_html=True,
    )
    st.markdown(f"<b>Total recaudado:</b> ${suma_pagos:,.2f}", unsafe_allow_html=True)
    if monto_total is not None and round(suma_pagos) != round(monto_total):
        st.warning(f"¡Atención! Suma ≠ total (${monto_total:.2f})")


st.title("Paddle Split (Web)")

st.info("Usa solo números y puntos para las horas. Ejemplo: 18, 18.15, 18.30, 18.45")

# Lista de nombres sugeridos para autocompletar
nombres_sugeridos = ["Dario", "Diego", "Federico", "Gustavo", "Hugo", "Mariano", "Yel"]

with st.form("datos_cancha"):
    col1, col2, col3 = st.columns(3)
    with col1:
        hora_inicio_str = st.text_input("Hora de inicio", "18.0")
    with col2:
        hora_fin_str = st.text_input("Hora de fin", "21.0")
    with col3:
        monto_total = st.number_input(
            "Total a pagar ($)", min_value=0.0, value=10000.0, step=1000.0
        )
    st.markdown("#### Jugadores iniciales (4)")
    jugadores = []
    for i in range(4):
        cols = st.columns(3)
        nombre = cols[0].selectbox(
            f"Nombre jugador #{i+1}",
            options=[""] + nombres_sugeridos,
            key=f"nombre{i}",
            help="Escribe las primeras letras y selecciona el nombre",
        )
        salida = cols[1].text_input(
            f"Salida jugador #{i+1} (ej: 20.0)", key=f"salida{i}"
        )
        jugadores.append(
            {
                "nombre": nombre,
                "llegada": parsear_hora(hora_inicio_str),
                "salida": parsear_hora(salida),
            }
        )
    st.markdown("#### Agregar más jugadores (opcional)")
    for i in range(4, 8):
        cols = st.columns(4)
        nombre = cols[0].selectbox(
            f"Nombre jugador #{i+1}",
            options=[""] + nombres_sugeridos,
            key=f"nombre{i}",
            help="Escribe las primeras letras y selecciona el nombre",
        )
        llegada = cols[1].text_input(f"Llegada jugador #{i+1} ", key=f"llegada{i}")
        salida = cols[2].text_input(f"Salida jugador #{i+1} ", key=f"salida{i}")
        if nombre:
            jugadores.append(
                {
                    "nombre": nombre,
                    "llegada": parsear_hora(llegada),
                    "salida": parsear_hora(salida),
                }
            )
    submitted = st.form_submit_button("Calcular pagos")

if submitted:
    hora_inicio = parsear_hora(hora_inicio_str)
    hora_fin = parsear_hora(hora_fin_str)
    if hora_inicio is None or hora_fin is None or hora_fin <= hora_inicio:
        st.error(
            "Las horas de inicio y fin deben ser válidas y la de fin mayor a la de inicio."
        )
    elif not jugadores or len([j for j in jugadores if j["nombre"]]) < 4:
        st.error("Debes ingresar al menos 4 jugadores.")
    else:
        pagos_detallados = calcular_pagos_por_intervalos(
            jugadores, monto_total, hora_inicio, hora_fin
        )
        mostrar_pagos_streamlit(pagos_detallados, hora_inicio, hora_fin, monto_total)
