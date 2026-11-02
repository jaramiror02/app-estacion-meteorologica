
import requests
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Estación Meteorológica - IES Virgen de Gracia",
    page_icon="⛅",
    layout="wide",
)

# ==========================================
# 2. ESTILOS VISUALES (CSS)
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #050505;
    color: #ffffff;
}

.weather-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 18px;
    min-height: 155px;
}

.weather-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(0, 255, 128, 0.25);
    border-color: #00ff80;
}

.weather-icon {
    font-size: 2.5rem;
    margin-bottom: 8px;
}

.weather-card h3 {
    margin: 0;
    font-size: 0.95rem;
    color: #a0b0c0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.weather-card h2 {
    margin-top: 12px;
    font-size: 2rem;
    color: #ffffff;
}

.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #00ff80;
    font-size: 1.25rem;
    margin-bottom: 20px;
}

.update {
    text-align: center;
    color: #b0c0d0;
    font-size: 1rem;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. TÍTULO DEL CENTRO
# ==========================================

st.markdown("""
<div class="main-title">
    ⛅ Estación Meteorológica
</div>
<div class="subtitle">
    IES Virgen de Gracia · Oliva de la Frontera
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 4. CONEXIÓN CON EL SERVIDOR DE RENDER
# ==========================================

URL_API = "https://estacion-meteorologica-profe.onrender.com/api/estado"


def obtener_datos():
    try:
        response = requests.get(URL_API, timeout=15)

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        pass

    return None


# ==========================================
# 5. FUNCIÓN PARA CREAR TARJETAS
# ==========================================

def tarjeta(columna, icono, titulo, valor, unidad=""):
    columna.markdown(f"""
    <div class="weather-card">
        <div class="weather-icon">{icono}</div>
        <h3>{titulo}</h3>
        <h2>{valor} {unidad}</h2>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 6. OBTENER Y MOSTRAR LOS DATOS
# ==========================================

datos = obtener_datos()

if datos:

    st.markdown(
        f"""
        <div class="update">
        📅 Última actualización: {datos.get('fecha', 'N/D')}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primera fila: temperatura, humedad y viento

    col1, col2, col3 = st.columns(3)

    tarjeta(
        col1, "🌡️", "Temperatura",
        datos.get("temperatura_C", "--"), "°C"
    )

    tarjeta(
        col2, "💧", "Humedad",
        datos.get("humedad_pct", "--"), "%"
    )

    tarjeta(
        col3, "💨", "Viento",
        datos.get("viento_kmh", "--"), "km/h"
    )

    # Segunda fila: ráfaga, lluvia e índice UV

    col4, col5, col6 = st.columns(3)

    tarjeta(
        col4, "🌪️", "Ráfaga",
        datos.get("rafaga_kmh", "--"), "km/h"
    )

    tarjeta(
        col5, "🌧️", "Lluvia",
        datos.get("lluvia_acumulada_mm", "--"), "mm"
    )

    tarjeta(
        col6, "☀️", "Índice UV",
        datos.get("indice_uv", "--")
    )

    # Tercera fila: radiación solar y dirección del viento

    col7, col8 = st.columns(2)

    tarjeta(
        col7, "🔆", "Radiación solar",
        datos.get("radiacion_solar_W_m2", "--"), "W/m²"
    )

    tarjeta(
        col8, "🧭", "Dirección del viento",
        datos.get("direccion_viento_grados", "--"), "°"
    )

    # ==========================================
    # 7. AVISOS METEOROLÓGICOS
    # ==========================================

    temperatura = datos.get("temperatura_C")

    try:
        if temperatura is not None and float(temperatura) > 25:
            st.warning(
                "⚠️ ¡Aviso educativo: Temperatura superior a 25 °C!"
            )
    except (ValueError, TypeError):
        pass

else:

    st.error(
        "⚠️ No se pudo conectar con el servidor meteorológico."
    )

    st.info(
        "Comprueba que el servidor de Render está funcionando."
    )

# ==========================================
# 8. PIE DE PÁGINA
# ==========================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; color:#777; padding:10px;">
    IES Virgen de Gracia · Oliva de la Frontera<br>
    Proyecto educativo de Tecnología e Ingeniería
</div>
""", unsafe_allow_html=True)
