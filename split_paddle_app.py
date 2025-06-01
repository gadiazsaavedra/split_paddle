import streamlit as st
import math


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
        minutos_decimal = {0: 0, 15: 0.25, 30: 0.5, 45: 0.75}[minutos]
        return horas + minutos_decimal
    except Exception:
        return None


def calcular_pagos_por_intervalos(jugadores, monto_total, hora_inicio, hora_fin):
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


def mostrar_pagos_streamlit(
    pagos_detallados,
    hora_inicio,
    hora_fin,
    monto_total,
    total_efectivo,
    total_billetera,
):
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

        # Ícono y color según forma de pago
        if pago.get("forma_pago") == "Efectivo":
            icono = "💵"
            color_fondo = "#e6ffe6"
            color_borde = "#2ecc40"
            color_pago = "green"
            forma_pago_str = "Efectivo"
            pago_mostrar = f"<b>${pago['pago']:,.0f}</b> <span style='font-size:0.9em;'>(redondeado)</span>"
        else:
            icono = "📲"
            color_fondo = "#e6f0ff"
            color_borde = "#3498db"
            color_pago = "#1976d2"
            forma_pago_str = "Billetera"
            pago_redondeado = round(pago["pago"], 2)
            pago_mostrar = f"<b>${pago_redondeado:,.2f}</b>"

        st.markdown(
            f"""
            <div style="
                border:2px solid {color_borde};
                border-radius:10px;
                padding:12px;
                margin-bottom:14px;
                background:{color_fondo};
                color:var(--text-color);
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                font-size:1.1em;
            ">
                <span style="font-size:1.5em;">{icono}</span>
                <b style="font-size:1.2em;"> {pago['nombre'].upper()}</b> {marca}<br>
                <span style="color:{color_pago}; font-weight:bold;">{forma_pago_str}</span><br>
                <span style="color:var(--text-color);">Pago:</span>
                <span style="color:{color_pago}; font-size:1.2em;">{pago_mostrar}</span><br>
                <span style="color:var(--text-color);">Tiempo:</span> {tiempo_str}
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
        mensaje = "¡Atención! Suma ≠ total"
        if total_efectivo > 0 and total_billetera == 0:
            mensaje += f"   |   Recaudado: ${total_efectivo:,.2f}"
        st.warning(mensaje)


# --- Sugerencias y nombres ---
sugerencias_inicio = ["17", "17.30", "18", "18.30", "19", "19.30", "20"]
sugerencias_fin = ["18", "18.30", "19", "19.30", "20", "20.30", "21", "21.30", "22"]
nombres_sugeridos = [
    "Dario",
    "El Crack",
    "Federico",
    "Hugo",
    "Mariano",
    "Yel",
    "Diego",
    "Claudio",
]

# --- Estado para cantidad de jugadores ---
if "num_jugadores" not in st.session_state:
    st.session_state.num_jugadores = 4

st.title("Paddle Split (Web)")
st.info("Usa solo números y puntos para las horas. Ejemplo: 18, 18.15, 18.30, 18.45")

# Botón para agregar jugador (fuera del form)
if st.session_state.num_jugadores < 12:
    if st.button("Agregar jugador"):
        st.session_state.num_jugadores += 1

# Botón para quitar jugador (fuera del form)
if st.session_state.num_jugadores > 4:
    if st.button("Quitar último jugador"):
        st.session_state.num_jugadores -= 1

with st.form("datos_cancha"):
    st.markdown("#### Datos de la cancha")
    col1, col2 = st.columns(2)
    with col1:
        hora_inicio_str = st.selectbox(
            "Hora de inicio", options=sugerencias_inicio, index=2, key="hora_inicio"
        )
    with col2:
        hora_fin_str = st.selectbox(
            "Hora de fin", options=sugerencias_fin, index=2, key="hora_fin"
        )
    monto_total = st.number_input(
        "Total a pagar ($)", min_value=0.0, value=10000.0, step=1000.0
    )

    st.markdown("#### Jugadores")
    jugadores = []
    for i in range(st.session_state.num_jugadores):
        st.markdown(f"**Jugador #{i+1}**")
        nombre = st.selectbox(
            "Nombre",
            options=[""] + nombres_sugeridos,
            key=f"nombre{i}",
            help="Escribe o selecciona el nombre",
        )
        cols = st.columns(3)
        llegada = cols[0].selectbox(
            "Llegada",
            options=sugerencias_inicio + sugerencias_fin,
            index=(
                (sugerencias_inicio + sugerencias_fin).index(hora_inicio_str)
                if hora_inicio_str in (sugerencias_inicio + sugerencias_fin)
                else 0
            ),
            key=f"llegada{i}",
        )
        salida = cols[1].selectbox(
            "Salida",
            options=sugerencias_fin,
            index=(
                sugerencias_fin.index(hora_fin_str)
                if hora_fin_str in sugerencias_fin
                else 0
            ),
            key=f"salida{i}",
        )
        forma_pago = cols[2].selectbox(
            "Forma de pago",
            options=["Efectivo", "Billetera"],  # <--- Cambiado aquí
            key=f"pago{i}",
        )
        jugadores.append(
            {
                "nombre": nombre,
                "llegada": parsear_hora(llegada),
                "salida": parsear_hora(salida),
                "forma_pago": forma_pago,
            }
        )
    submitted = st.form_submit_button("Calcular pagos")

if submitted:
    hora_inicio = parsear_hora(hora_inicio_str)
    hora_fin = parsear_hora(hora_fin_str)
    jugadores_validos = [j for j in jugadores if j["nombre"]]
    # Validación visual inmediata
    error = False
    if hora_inicio is None or hora_fin is None or hora_fin <= hora_inicio:
        st.error(
            "Las horas de inicio y fin deben ser válidas y la de fin mayor a la de inicio."
        )
        error = True
    elif not jugadores_validos or len(jugadores_validos) < 4:
        st.error("Debes ingresar al menos 4 jugadores.")
        error = True
    else:
        for j in jugadores_validos:
            if (
                j["llegada"] is None
                or j["salida"] is None
                or j["llegada"] >= j["salida"]
            ):
                st.error(f"La llegada debe ser menor que la salida para {j['nombre']}.")
                error = True
                break
    if not error:
        pagos_detallados = calcular_pagos_por_intervalos(
            jugadores_validos, monto_total, hora_inicio, hora_fin
        )
        # Antes de calcular pagos_detallados:
        forma_pago_dict = {j["nombre"]: j["forma_pago"] for j in jugadores_validos}

        # Después de calcular pagos_detallados:
        for pago in pagos_detallados:
            pago["forma_pago"] = forma_pago_dict.get(pago["nombre"], "Efectivo")

        # 1. Redondear pagos en efectivo hacia abajo de a 100
        diferencia_total = 0
        for pago in pagos_detallados:
            if pago.get("forma_pago") == "Efectivo":
                pago_original = pago["pago"]
                pago_redondeado = math.floor(pago_original / 100) * 100
                diferencia = pago_original - pago_redondeado
                pago["pago"] = pago_redondeado
                diferencia_total += diferencia

        # 2. Sumar la diferencia a los de billetera (proporcionalmente)
        billetera_jugadores = [
            p for p in pagos_detallados if p.get("forma_pago") == "Billetera"
        ]
        if billetera_jugadores and diferencia_total > 0:
            suma_billetera = sum(p["pago"] for p in billetera_jugadores)
            for p in billetera_jugadores:
                proporcion = (
                    p["pago"] / suma_billetera
                    if suma_billetera > 0
                    else 1 / len(billetera_jugadores)
                )
                p["pago"] += diferencia_total * proporcion

        # (Opcional) Redondear visualmente los pagos de billetera a 2 decimales
        for p in billetera_jugadores:
            p["pago"] = round(p["pago"], 2)

        # Calcula los totales ANTES de mostrar los pagos
        total_efectivo = sum(
            p["pago"] for p in pagos_detallados if p.get("forma_pago") == "Efectivo"
        )
        total_billetera = sum(
            p["pago"] for p in pagos_detallados if p.get("forma_pago") == "Billetera"
        )

        # Pasa los totales a la función
        mostrar_pagos_streamlit(
            pagos_detallados,
            hora_inicio,
            hora_fin,
            monto_total,
            total_efectivo,
            total_billetera,
        )

        # --- Mejor presentación de resultados ---
        st.markdown("---")
        st.subheader("Resumen por forma de pago")

        col_efectivo, col_billetera = st.columns(2)
        with col_efectivo:
            st.markdown(
                f"""
                <div style="background: #e6ffe6; border-radius: 10px; padding: 16px; text-align: center; border: 2px solid #2ecc40;">
                    <span style="font-size: 2em;">💵</span><br>
                    <b>Total efectivo:</b><br>
                    <span style="color:green; font-size:1.5em;"><b>${total_efectivo:,.2f}</b></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_billetera:
            st.markdown(
                f"""
                <div style="background: #e6f0ff; border-radius: 10px; padding: 16px; text-align: center; border: 2px solid #3498db;">
                    <span style="font-size: 2em;">📲</span><br>
                    <b>Total billetera:</b><br>
                    <span style="color:#1976d2; font-size:1.5em;"><b>${total_billetera:,.2f}</b></span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("")

        # Mensaje de éxito
        st.success(
            "¡Pagos calculados correctamente! Cada jugador puede ver su forma de pago y monto en el detalle de arriba."
        )

        # Opcional: leyenda de íconos
        st.markdown(
            "<small>💵 = Efectivo &nbsp;&nbsp;&nbsp; 📲 = Billetera virtual</small>",
            unsafe_allow_html=True,
        )

        # Si todos pagan en efectivo, mostrar recaudación total
        if total_efectivo > 0 and total_billetera == 0:
            st.markdown(
                f"""
                <div style="background: #e6ffe6; border-radius: 10px; padding: 16px; text-align: center; border: 2px solid #2ecc40; margin-top: 10px;">
                    <span style="font-size: 1.5em;">💵</span><br>
                    <b>Todos pagan en efectivo</b><br>
                    <span style="color:green; font-size:1.3em;"><b>Total recaudado: ${total_efectivo:,.2f}</b></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
