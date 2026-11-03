
import requests
import streamlit as st
import streamlit.components.v1 as components
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

URL_ESTADO = "https://servidor-estacion-meteorologica.onrender.com/api/estado"
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

    h1, h2, h3, p {
        color: white;
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

    .pie {
        text-align: center;
        color: #718087;
        font-size: 12px;
        padding: 15px 0 5px 0;
    }

    div[data-testid="stMetric"] {
        background: #111c21;
        border: 1px solid #26383e;
        padding: 12px;
        border-radius: 12px;
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

    .estado {
        text-align: center;
        color: #9eabb0;
        font-size: 12px;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. FUNCIONES PARA CONSULTAR LOS DATOS
# =====================================================

def obtener_datos_actuales():

    try:
        respuesta = requests.get(
            URL_ESTADO,
            timeout=20
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except (requests.RequestException, ValueError):
        return None


# El histórico queda guardado en caché durante 5 minutos.
# Las excepciones no se guardan en caché: se podrá reintentar
# la consulta en la siguiente actualización.

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
# 4. FUNCIONES AUXILIARES
# =====================================================

def formato(valor, decimales=1):

    if valor is None or valor == "":
        return "--"

    try:
        return f"{float(valor):.{decimales}f}"
    except (ValueError, TypeError):
        return "--"


def tarjeta(titulo, valor, unidad, clase):

    st.markdown(
        f"""
        <div class="tarjeta">
            <div class="tarjeta-titulo">{escape(titulo)}</div>
            <div class="tarjeta-valor {clase}">
                {escape(str(valor))}
                <span class="tarjeta-unidad">{escape(unidad)}</span>
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
# 5. CABECERA
# =====================================================

st.markdown("""
<div class="cabecera">
    <div class="titulo">⛅ ESTACIÓN METEOROLÓGICA</div>
    <div class="subtitulo">
        IES VIRGEN DE GRACIA · OLIVA DE LA FRONTERA
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 6. CONSULTA DE LOS DATOS
# =====================================================

datos = obtener_datos_actuales()


# =====================================================
# 7. PESTAÑAS
# =====================================================

pestana_actual, pestana_historico = st.tabs([
    "🌤️ DATOS ACTUALES",
    "📈 EVOLUCIÓN 24 HORAS"
])


# =====================================================
# 8. PESTAÑA DE DATOS ACTUALES
# =====================================================

with pestana_actual:

    if datos is None:

        st.error(
            "No se puede conectar con el servidor de la estación meteorológica."
        )

        st.info(
            "Comprueba que el servidor está funcionando e inténtalo de nuevo."
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

        # Aviso educativo

        if temperatura is not None:

            try:
                if float(temperatura) > 25:

                    st.markdown("""
                    <div class="aviso">
                        ☀️ <b>AVISO:</b> La temperatura supera los 25 °C.
                    </div>
                    """, unsafe_allow_html=True)

            except (ValueError, TypeError):
                pass

        # Fecha de los datos

        fecha = datos.get("fecha")

        if fecha:
            st.markdown(
                f'<div class="estado">Última observación: {escape(str(fecha))}</div>',
                unsafe_allow_html=True
            )



# =====================================================
# 9. PESTAÑA DE EVOLUCIÓN DE LAS ÚLTIMAS 24 HORAS
# =====================================================

with pestana_historico:

    historico = obtener_historico()

    if historico is None:

        st.warning("No se ha podido consultar el histórico.")

    elif "error" in historico:

        st.warning(historico["error"])

    else:

        registros = historico.get("registros", [])

        if not registros:

            st.info("Todavía no hay registros históricos disponibles.")

        else:

            df = pd.DataFrame(registros)

            # Preparar las horas

            if "epoch" in df.columns:

                df["hora"] = (
                    pd.to_datetime(df["epoch"], unit="s", utc=True)
                    .dt.tz_convert("Europe/Madrid")
                    .dt.strftime("%H:%M")
                )

                df = df.sort_values("epoch")

            else:

                df["hora"] = df["fecha"].astype(str)

            # Fondo y estilo de las gráficas

            st.markdown("""
            <style>
                .grafica-titulo {
                    font-size: 20px;
                    font-weight: 750;
                    color: #e8f4ff;
                    margin-top: 20px;
                    margin-bottom: 5px;
                }

                .grafica-subtitulo {
                    font-size: 12px;
                    color: #8299aa;
                    margin-bottom: 15px;
                }

                div[data-testid="stMetric"] {
                    background: linear-gradient(135deg, #132b3b, #091722);
                    border: 1px solid #24465c;
                    border-radius: 14px;
                    padding: 16px;
                }
            </style>
            """, unsafe_allow_html=True)

            # -----------------------------------------
            # TEMPERATURA
            # -----------------------------------------

            st.markdown("""
            <div class="grafica-titulo">🌡️ Temperatura</div>
            <div class="grafica-subtitulo">
                Evolución de la temperatura durante las últimas 24 horas
            </div>
            """, unsafe_allow_html=True)

            if "temperatura_C" in df.columns:

                df_temp = df[["hora", "temperatura_C"]].copy()

                df_temp["temperatura_C"] = pd.to_numeric(
                    df_temp["temperatura_C"],
                    errors="coerce"
                )

                df_temp = df_temp.dropna()

                if not df_temp.empty:

                    st.line_chart(
                        df_temp.set_index("hora"),
                        color="#FF6B6B",
                        height=300
                    )

                else:
                    st.info("No hay datos de temperatura.")

            # -----------------------------------------
            # LLUVIA
            # -----------------------------------------

            st.markdown("""
            <div class="grafica-titulo">🌧️ Precipitación</div>
            <div class="grafica-subtitulo">
                Cantidad de lluvia registrada en cada observación
            </div>
            """, unsafe_allow_html=True)

            if "lluvia_mm" in df.columns:

                df_lluvia = df[["hora", "lluvia_mm"]].copy()

                df_lluvia["lluvia_mm"] = pd.to_numeric(
                    df_lluvia["lluvia_mm"],
                    errors="coerce"
                )

                df_lluvia = df_lluvia.dropna()

                if not df_lluvia.empty:

                    st.bar_chart(
                        df_lluvia.set_index("hora"),
                        color="#35C6FF",
                        height=250
                    )

                else:
                    st.info("No hay datos de lluvia.")

            # -----------------------------------------
            # RESUMEN
            # -----------------------------------------

            st.markdown("""
            <div class="grafica-titulo">📊 Resumen meteorológico</div>
            <div class="grafica-subtitulo">
                Valores registrados durante las últimas 24 horas
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

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
# 10. PIE DE PÁGINA
# =====================================================

st.markdown("""
<div class="pie">
    Proyecto educativo de Tecnología e Ingeniería
    · IES Virgen de Gracia
</div>
""", unsafe_allow_html=True)


# =====================================================
# 11. ACTUALIZACIÓN AUTOMÁTICA CADA 60 SEGUNDOS
# =====================================================

components.html(
    """
    <script>
        setTimeout(function() {
            window.parent.location.reload();
        }, 60000);
    </script>
    """,
    height=0
)
