
import requests
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Estación Meteorológica - IES Virgen de Gracia",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

URL_API = "https://servidor-estacion-meteorologica.onrender.com/api/estado"
URL_HISTORICO = "https://servidor-estacion-meteorologica.onrender.com/api/historico"

# ==========================================
# 2. ACTUALIZACIÓN AUTOMÁTICA CADA 60 SEGUNDOS
# ==========================================

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

# ==========================================
# 3. DISEÑO VISUAL
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #030607;
    color: white;
}

header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
    padding-left: 3% !important;
    padding-right: 3% !important;
    max-width: 1600px;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Cabecera */

.titulo {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    color: #f4f8ff;
    margin-bottom: 0px;
    letter-spacing: 1px;
}

.subtitulo {
    text-align: center;
    color: #00ff80;
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 5px;
}

.linea {
    height: 3px;
    background: linear-gradient(
        90deg, transparent, #00ff80, transparent
    );
    margin: 8px 0;
}

.actualizacion {
    text-align: center;
    color: #b9d4e9;
    font-size: 0.9rem;
    margin: 8px 0 12px 0;
}

/* Pestañas */

button[data-baseweb="tab"] {
    color: #b9c8df;
    font-size: 1rem;
    font-weight: 700;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #00ff80;
}

div[data-baseweb="tab-highlight"] {
    background-color: #00ff80;
}

/* Tarjetas */

.weather-card {
    height: 125px;
    border-radius: 19px;
    background: linear-gradient(
        145deg,
        rgba(27,32,42,0.96),
        rgba(3,8,12,0.98)
    );
    border: 1px solid #35404d;
    padding: 12px 8px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 5px 12px rgba(0,0,0,0.5);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.weather-card:hover {
    transform: translateY(-4px);
    filter: brightness(1.3);
}

.weather-icon {
    font-size: 1.9rem;
    margin-bottom: 2px;
}

.weather-label {
    color: #b9c8df;
    font-size: 0.85rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.weather-value {
    color: #ffffff;
    font-size: 2.25rem;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 3px;
}

.weather-unit {
    font-size: 1rem;
    font-weight: 500;
}

/* Colores de las tarjetas */

.red {
    border-bottom: 4px solid #ff303b;
    box-shadow: 0 4px 15px rgba(255,48,59,0.15);
}

.blue {
    border-bottom: 4px solid #00aaff;
    box-shadow: 0 4px 15px rgba(0,170,255,0.15);
}

.cyan {
    border-bottom: 4px solid #00d9e8;
    box-shadow: 0 4px 15px rgba(0,217,232,0.15);
}

.purple {
    border-bottom: 4px solid #b34cff;
    box-shadow: 0 4px 15px rgba(179,76,255,0.15);
}

.yellow {
    border-bottom: 4px solid #ffd000;
    box-shadow: 0 4px 15px rgba(255,208,0,0.15);
}

.green {
    border-bottom: 4px solid #61ff36;
    box-shadow: 0 4px 15px rgba(97,255,54,0.15);
}

.turquoise {
    border-bottom: 4px solid #00e5c5;
    box-shadow: 0 4px 15px rgba(0,229,197,0.15);
}

/* Avisos */

.aviso {
    background: rgba(255,190,0,0.10);
    border: 1px solid #d6a900;
    border-radius: 12px;
    color: #ffd000;
    padding: 9px;
    text-align: center;
    font-weight: bold;
    margin-top: 2px;
    font-size: 0.95rem;
}

/* Gráficas */

.grafica-titulo {
    color: #f4f8ff;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 12px 0 5px 0;
}

.pie {
    text-align: center;
    color: #667777;
    font-size: 0.72rem;
    margin-top: 5px;
}

@media (max-height: 800px) {

    .weather-card {
        height: 105px;
        padding: 6px;
        margin-bottom: 7px;
    }

    .weather-value {
        font-size: 1.9rem;
    }

    .weather-icon {
        font-size: 1.5rem;
    }

    .titulo {
        font-size: 1.65rem;
    }

    .actualizacion {
        margin: 4px 0 7px 0;
    }
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. CABECERA
# ==========================================

st.markdown("""
<div class="titulo">
    ⛅ ESTACIÓN METEOROLÓGICA
</div>

<div class="subtitulo">
    IES VIRGEN DE GRACIA · OLIVA DE LA FRONTERA
</div>

<div class="linea"></div>
""", unsafe_allow_html=True)

# ==========================================
# 5. CONEXIÓN CON EL SERVIDOR
# ==========================================

def obtener_datos():

    try:
        respuesta = requests.get(
            URL_API,
            timeout=15
        )

        respuesta.raise_for_status()
        return respuesta.json()

    except (requests.RequestException, ValueError):
        return None


def obtener_historico():

    try:
        respuesta = requests.get(
            URL_HISTORICO,
            timeout=20
        )

        respuesta.raise_for_status()
        return respuesta.json()

    except (requests.RequestException, ValueError):
        return None


datos = obtener_datos()
historico = obtener_historico()

# ==========================================
# 6. FUNCIÓN PARA CREAR TARJETAS
# ==========================================

def tarjeta(columna, icono, titulo, valor, unidad, color):

    if valor is None:
        valor = "--"

    columna.markdown(f"""
    <div class="weather-card {color}">
        <div class="weather-icon">{icono}</div>
        <div class="weather-label">{titulo}</div>
        <div class="weather-value">
            {valor} <span class="weather-unit">{unidad}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 7. CREACIÓN DE LAS DOS PESTAÑAS
# ==========================================

pestana_actual, pestana_historico = st.tabs([
    "🌤️ DATOS ACTUALES",
    "📈 EVOLUCIÓN 24 HORAS"
])


# ==========================================
# PESTAÑA 1. DATOS ACTUALES
# ==========================================

with pestana_actual:

    if datos and "error" not in datos:

        fecha_actualizacion = datos.get("fecha", "N/D")

        st.markdown(
            f'<div class="actualizacion">'
            f'🕒 Últimos datos registrados: {fecha_actualizacion}'
            f'</div>',
            unsafe_allow_html=True
        )

        # FILA 1

        c1, c2, c3 = st.columns(3)

        tarjeta(
            c1, "🌡️", "Temperatura",
            datos.get("temperatura_C"), "°C", "red"
        )

        tarjeta(
            c2, "💧", "Humedad",
            datos.get("humedad_pct"), "%", "blue"
        )

        tarjeta(
            c3, "💨", "Viento",
            datos.get("viento_kmh"), "km/h", "cyan"
        )

        # FILA 2

        c4, c5, c6 = st.columns(3)

        tarjeta(
            c4, "🌪️", "Ráfaga",
            datos.get("rafaga_kmh"), "km/h", "purple"
        )

        tarjeta(
            c5, "🌧️", "Lluvia",
            datos.get("lluvia_acumulada_mm"), "mm", "blue"
        )

        tarjeta(
            c6, "☀️", "Índice UV",
            datos.get("indice_uv"), "", "yellow"
        )

        # FILA 3

        c7, c8 = st.columns(2)

        tarjeta(
            c7, "🔆", "Radiación solar",
            datos.get("radiacion_solar_W_m2"), "W/m²", "green"
        )

        tarjeta(
            c8, "🧭", "Dirección del viento",
            datos.get("direccion_viento_grados"), "°", "turquoise"
        )

        # AVISOS

        try:
            temperatura = float(datos.get("temperatura_C"))

            if temperatura > 25:
                st.markdown("""
                <div class="aviso">
                    ⚠️ ¡Aviso educativo: Temperatura superior a 25 °C!
                </div>
                """, unsafe_allow_html=True)

        except (ValueError, TypeError):
            pass

    else:

        st.error(
            "⚠️ No se pudo conectar con el servidor meteorológico."
        )


# ==========================================
# PESTAÑA 2. EVOLUCIÓN DE LAS ÚLTIMAS 24 HORAS
# ==========================================

with pestana_historico:

    st.markdown(
        '<div class="actualizacion">'
        '📊 Evolución meteorológica de las últimas 24 horas'
        '</div>',
        unsafe_allow_html=True
    )

    if historico and "error" not in historico:

        registros = historico.get("registros", [])

        if registros:

            df = pd.DataFrame(registros)

            # Preparar las fechas para las gráficas.

            if "fecha" in df.columns:
                df["fecha_grafica"] = pd.to_datetime(
                    df["fecha"],
                    errors="coerce"
                )

            if "epoch" in df.columns:

                fechas_epoch = pd.to_datetime(
                    df["epoch"],
                    unit="s",
                    utc=True
                ).dt.tz_convert("Europe/Madrid").dt.tz_localize(None)

                if "fecha_grafica" not in df.columns:
                    df["fecha_grafica"] = fechas_epoch
                else:
                    df["fecha_grafica"] = (
                        df["fecha_grafica"].fillna(fechas_epoch)
                    )

            # Convertir los valores a números.

            df["temperatura_C"] = pd.to_numeric(
                df["temperatura_C"],
                errors="coerce"
            )

            df["lluvia_mm"] = pd.to_numeric(
                df["lluvia_mm"],
                errors="coerce"
            )

            df = df.dropna(subset=["fecha_grafica"])
            df = df.sort_values("fecha_grafica")

            # RESUMEN DE LAS ÚLTIMAS 24 HORAS

            temperaturas = df["temperatura_C"].dropna()
            lluvias = df["lluvia_mm"].dropna()

            r1, r2, r3 = st.columns(3)

            if not temperaturas.empty:

                r1.metric(
                    "🌡️ Temperatura máxima",
                    f"{temperaturas.max():.1f} °C"
                )

                r2.metric(
                    "❄️ Temperatura mínima",
                    f"{temperaturas.min():.1f} °C"
                )

            else:
                r1.metric("🌡️ Temperatura máxima", "--")
                r2.metric("❄️ Temperatura mínima", "--")

            lluvia_total = lluvias.sum() if not lluvias.empty else 0

            r3.metric(
                "🌧️ Lluvia total",
                f"{lluvia_total:.1f} mm"
            )

            # GRÁFICA DE TEMPERATURA

            st.markdown(
                '<div class="grafica-titulo">'
                '🌡️ Evolución de la temperatura'
                '</div>',
                unsafe_allow_html=True
            )

            df_temperatura = df.dropna(
                subset=["temperatura_C"]
            ).set_index("fecha_grafica")

            if not df_temperatura.empty:

                st.line_chart(
                    df_temperatura[["temperatura_C"]],
                    color="#ff303b",
                    y_label="Temperatura (°C)",
                    x_label="Hora",
                    height=300
                )

            else:
                st.info(
                    "No hay datos de temperatura para representar."
                )

            # GRÁFICA DE PRECIPITACIONES

            st.markdown(
                '<div class="grafica-titulo">'
                '🌧️ Precipitaciones por hora'
                '</div>',
                unsafe_allow_html=True
            )

            df_lluvia = df.dropna(
                subset=["lluvia_mm"]
            ).set_index("fecha_grafica")

            if not df_lluvia.empty:

                st.bar_chart(
                    df_lluvia[["lluvia_mm"]],
                    color="#00aaff",
                    y_label="Lluvia (mm)",
                    x_label="Hora",
                    height=300
                )

            else:
                st.info(
                    "No hay datos de lluvia para representar."
                )

            st.caption(
                f"Registros recibidos: {len(df)}. "
                "Los valores corresponden a las observaciones "
                "horarias disponibles."
            )

        else:

            st.warning(
                "Todavía no hay registros históricos disponibles."
            )

    else:

        st.error(
            "No se ha podido consultar el histórico meteorológico."
        )


# ==========================================
# 8. PIE DE PÁGINA
# ==========================================

st.markdown("""
<div class="pie">
    Proyecto educativo de Tecnología e Ingeniería · IES Virgen de Gracia
</div>
""", unsafe_allow_html=True)
