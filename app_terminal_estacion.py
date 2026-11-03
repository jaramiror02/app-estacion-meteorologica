
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape

# =====================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Estación Meteorológica - IES Virgen de Gracia",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

URL_API = "https://servidor-estacion-meteorologica.onrender.com/api/estado"
URL_HISTORICO = "https://servidor-estacion-meteorologica.onrender.com/api/historico"


# =====================================================
# 2. ESTILO VISUAL
# =====================================================

st.markdown("""
<style>
    .stApp {
        background: #030607;
        color: white;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    .cabecera {
        text-align: center;
        padding: 10px 0 18px 0;
    }

    .titulo {
        font-size: 32px;
        font-weight: 800;
        color: white;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }

    .subtitulo {
        font-size: 15px;
        font-weight: 700;
        color: #00e676;
        letter-spacing: 2px;
    }

    .tarjeta {
        border-radius: 15px;
        padding: 15px;
        min-height: 115px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #172329, #0b1115);
        border: 1px solid #26383e;
        box-shadow: 0 3px 12px rgba(0,0,0,0.3);
    }

    .tarjeta-titulo {
        font-size: 13px;
        font-weight: 700;
        color: #c4d1d5;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .tarjeta-valor {
        font-size: 29px;
        font-weight: 800;
        line-height: 1.2;
    }

    .tarjeta-unidad {
        font-size: 14px;
        color: #bdc9ce;
        font-weight: 500;
    }

    .temperatura { color: #ff5252; }
    .humedad { color: #40c4ff; }
    .viento { color: #00e5ff; }
    .rafaga { color: #b388ff; }
    .lluvia { color: #448aff; }
    .uv { color: #ffd740; }
    .radiacion { color: #ffab40; }
    .direccion { color: #69f0ae; }

    .grafica-titulo {
        font-size: 20px;
        font-weight: 750;
        color: #e8f4ff;
        margin-top: 22px;
        margin-bottom: 5px;
    }

    .grafica-subtitulo {
        font-size: 12px;
        color: #8299aa;
        margin-bottom: 15px;
    }

    .pie {
        text-align: center;
        color: #718087;
        font-size: 12px;
        padding: 15px 0 5px 0;
    }

    .estado {
        text-align: center;
        color: #9eabb0;
        font-size: 12px;
        margin-top: 5px;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #132b3b, #091722);
        border: 1px solid #24465c;
        border-radius: 14px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #bdc9ce;
    }

    div[data-testid="stMetricValue"] {
        color: white;
    }

    .aviso {
        background: #38251b;
        border: 1px solid #ff9800;
        border-radius: 10px;
        padding: 12px;
        color: #ffcc80;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. CONSULTA DE DATOS ACTUALES
# =====================================================

def obtener_datos_actuales():

    try:
        respuesta = requests.get(
            URL_API,
            timeout=20
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except (requests.RequestException, ValueError):
        return None


# =====================================================
# 4. CONSULTA DEL HISTÓRICO
# =====================================================

# Los datos históricos se guardan durante 5 minutos.
# Esto evita consultar continuamente la API.

@st.cache_data(ttl=300, show_spinner=False)
def consultar_historico():

    respuesta = requests.get(
        URL_HISTORICO,
        timeout=20
    )

    respuesta.raise_for_status()

    return respuesta.json()


def obtener_historico():

    try:
        return consultar_historico()

    except (requests.RequestException, ValueError):
        return None


# =====================================================
# 5. FUNCIONES AUXILIARES
# =====================================================

def formato(valor, decimales=1):

    if valor is None or valor == "":
        return "--"

    try:
        return f"{float(valor):.{decimales}f}"

    except (ValueError, TypeError):
        return "--"


def tarjeta(titulo, valor, unidad, clase):

    unidad_html = ""

    if unidad:
        unidad_html = (
            f'<span class="tarjeta-unidad">'
            f'{escape(unidad)}'
            f'</span>'
        )

    st.markdown(
        f"""
        <div class="tarjeta">
            <div class="tarjeta-titulo">
                {escape(titulo)}
            </div>
            <div class="tarjeta-valor {clase}">
                {escape(str(valor))}{unidad_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def direccion_viento(grados):

    if grados is None:
        return "--"

    try:
        grados = float(grados)

    except (ValueError, TypeError):
        return "--"

    direcciones = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSO", "SO", "OSO",
        "O", "ONO", "NO", "NNO"
    ]

    indice = round(grados / 22.5) % 16

    return f"{direcciones[indice]} ({grados:.0f}°)"


# =====================================================
# 6. CABECERA
# =====================================================

st.markdown("""
<div class="cabecera">
    <div class="titulo">
        ⛅ ESTACIÓN METEOROLÓGICA
    </div>
    <div class="subtitulo">
        IES VIRGEN DE GRACIA · OLIVA DE LA FRONTERA
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 7. CONSULTAR DATOS ACTUALES
# =====================================================

datos = obtener_datos_actuales()


# =====================================================
# 8. PESTAÑAS PRINCIPALES
# =====================================================

pestana_actual, pestana_historico = st.tabs([
    "🌤️ DATOS ACTUALES",
    "📈 EVOLUCIÓN DE HOY"
])


# =====================================================
# 9. PESTAÑA DE DATOS ACTUALES
# =====================================================

with pestana_actual:

    if datos is None:

        st.error(
            "No se puede conectar con el servidor de la estación meteorológica."
        )

        st.info(
            "Comprueba la conexión con el servidor e inténtalo de nuevo."
        )

    elif "error" in datos:

        st.error(datos["error"])

    else:

        temperatura = datos.get("temperatura_C")
        humedad = datos.get("humedad_pct")
        viento = datos.get("viento_kmh")
        rafaga = datos.get("rafaga_kmh")
        lluvia = datos.get("lluvia_acumulada_mm")
        radiacion = datos.get("radiacion_solar_W_m2")
        uv = datos.get("indice_uv")
        direccion = datos.get("direccion_viento_grados")

        # Primera fila de tarjetas

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            tarjeta(
                "Temperatura",
                formato(temperatura),
                "°C",
                "temperatura"
            )

        with col2:
            tarjeta(
                "Humedad",
                formato(humedad, 0),
                "%",
                "humedad"
            )

        with col3:
            tarjeta(
                "Velocidad del viento",
                formato(viento),
                "km/h",
                "viento"
            )

        with col4:
            tarjeta(
                "Ráfaga de viento",
                formato(rafaga),
                "km/h",
                "rafaga"
            )

        # Segunda fila de tarjetas

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            tarjeta(
                "Lluvia acumulada",
                formato(lluvia),
                "mm",
                "lluvia"
            )

        with col6:
            tarjeta(
                "Índice UV",
                formato(uv, 0),
                "",
                "uv"
            )

        with col7:
            tarjeta(
                "Radiación solar",
                formato(radiacion),
                "W/m²",
                "radiacion"
            )

        with col8:
            tarjeta(
                "Dirección del viento",
                direccion_viento(direccion),
                "",
                "direccion"
            )

        # Aviso de temperatura

        if temperatura is not None:

            try:

                if float(temperatura) > 25:

                    st.markdown("""
                    <div class="aviso">
                        ☀️ <b>AVISO:</b>
                        La temperatura supera los 25 °C.
                    </div>
                    """, unsafe_allow_html=True)

            except (ValueError, TypeError):
                pass

        # Fecha de la última observación

        fecha = datos.get("fecha")

        if fecha:

            st.markdown(
                f'<div class="estado">Última observación: {escape(str(fecha))}</div>',
                unsafe_allow_html=True
            )


# =====================================================
# 10. PESTAÑA DE EVOLUCIÓN DEL DÍA ACTUAL
# =====================================================

with pestana_historico:

    historico = obtener_historico()

    if historico is None:

        st.warning(
            "No se ha podido consultar el histórico."
        )

    elif "error" in historico:

        st.warning(historico["error"])

    else:

        registros = historico.get("registros", [])

        if not registros:

            st.info(
                "Todavía no hay registros disponibles para hoy."
            )

        else:

            df = pd.DataFrame(registros)

            if "epoch" not in df.columns:

                st.warning(
                    "Los registros históricos no contienen la hora de observación."
                )

            else:

                # -----------------------------------------
                # FILTRAR DESDE LAS 00:00 HASTA AHORA
                # -----------------------------------------

                ahora = pd.Timestamp.now(
                    tz="Europe/Madrid"
                )

                inicio_dia = ahora.normalize()

                df["epoch"] = pd.to_numeric(
                    df["epoch"],
                    errors="coerce"
                )

                df = df.dropna(subset=["epoch"]).copy()

                df["fecha_hora"] = pd.to_datetime(
                    df["epoch"],
                    unit="s",
                    utc=True
                ).dt.tz_convert("Europe/Madrid")

                # Eliminar registros de otros días
                # y cualquier observación futura.

                df = df[
                    (df["fecha_hora"] >= inicio_dia) &
                    (df["fecha_hora"] <= ahora)
                ].copy()

                df = df.sort_values("fecha_hora")

                if df.empty:

                    st.info(
                        "Todavía no hay observaciones para mostrar."
                    )

                else:

                    # -----------------------------------------
                    # ENCABEZADO
                    # -----------------------------------------

                    st.markdown("""
                    <div class="grafica-titulo">
                        📅 Evolución meteorológica de hoy
                    </div>
                    <div class="grafica-subtitulo">
                        Registros desde las 00:00 hasta la hora actual
                    </div>
                    """, unsafe_allow_html=True)

                    st.caption(
                        f"Registros disponibles: {len(df)} · "
                        f"Consulta realizada a las {ahora.strftime('%H:%M')}"
                    )

                    # -----------------------------------------
                    # GRÁFICA DE TEMPERATURA
                    # -----------------------------------------

                    st.markdown("""
                    <div class="grafica-titulo">
                        🌡️ Temperatura
                    </div>
                    <div class="grafica-subtitulo">
                        Evolución de la temperatura durante el día
                    </div>
                    """, unsafe_allow_html=True)

                    if "temperatura_C" in df.columns:

                        df_temp = df[
                            ["fecha_hora", "temperatura_C"]
                        ].copy()

                        df_temp["temperatura_C"] = pd.to_numeric(
                            df_temp["temperatura_C"],
                            errors="coerce"
                        )

                        df_temp = df_temp.dropna()

                        if not df_temp.empty:

                            st.line_chart(
                                df_temp.set_index("fecha_hora"),
                                y="temperatura_C",
                                color="#FF6B6B",
                                height=300
                            )

                        else:

                            st.info(
                                "No hay datos de temperatura disponibles."
                            )

                    # -----------------------------------------
                    # GRÁFICA DE LLUVIA
                    # -----------------------------------------

                    st.markdown("""
                    <div class="grafica-titulo">
                        🌧️ Precipitación
                    </div>
                    <div class="grafica-subtitulo">
                        Lluvia registrada durante el día
                    </div>
                    """, unsafe_allow_html=True)

                    if "lluvia_mm" in df.columns:

                        df_lluvia = df[
                            ["fecha_hora", "lluvia_mm"]
                        ].copy()

                        df_lluvia["lluvia_mm"] = pd.to_numeric(
                            df_lluvia["lluvia_mm"],
                            errors="coerce"
                        )

                        df_lluvia = df_lluvia.dropna()

                        if not df_lluvia.empty:

                            st.bar_chart(
                                df_lluvia.set_index("fecha_hora"),
                                y="lluvia_mm",
                                color="#35C6FF",
                                height=250
                            )

                        else:

                            st.info(
                                "No hay datos de lluvia disponibles."
                            )

                    # -----------------------------------------
                    # RESUMEN DEL DÍA
                    # -----------------------------------------

                    st.markdown("""
                    <div class="grafica-titulo">
                        📊 Resumen meteorológico de hoy
                    </div>
                    <div class="grafica-subtitulo">
                        Valores registrados desde medianoche
                    </div>
                    """, unsafe_allow_html=True)

                    if "temperatura_C" in df.columns:

                        temperaturas = pd.to_numeric(
                            df["temperatura_C"],
                            errors="coerce"
                        ).dropna()

                    else:

                        temperaturas = pd.Series(dtype=float)

                    if "lluvia_mm" in df.columns:

                        lluvias = pd.to_numeric(
                            df["lluvia_mm"],
                            errors="coerce"
                        ).dropna()

                    else:

                        lluvias = pd.Series(dtype=float)

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "🌡️ Temperatura máxima",
                            f"{temperaturas.max():.1f} °C"
                            if not temperaturas.empty else "--"
                        )

                    with col2:

                        st.metric(
                            "❄️ Temperatura mínima",
                            f"{temperaturas.min():.1f} °C"
                            if not temperaturas.empty else "--"
                        )

                    with col3:

                        st.metric(
                            "🌧️ Lluvia registrada",
                            f"{lluvias.sum():.1f} mm"
                            if not lluvias.empty else "--"
                        )


# =====================================================
# 11. PIE DE PÁGINA
# =====================================================

st.markdown("""
<div class="pie">
    Proyecto educativo de Tecnología e Ingeniería
    · IES Virgen de Gracia
</div>
""", unsafe_allow_html=True)
