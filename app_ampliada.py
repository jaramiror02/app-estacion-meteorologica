import requests
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
# Definimos el título de la pestaña del navegador, el icono y el diseño centrado
st.set_page_config(
    page_title="Estación Meteorológica - IES Oliva de la Frontera",
    page_icon="⛅",
    layout="centered",
)

# ==========================================
# 2. ESTILOS VISUALES PERSONALIZADOS (CSS)
# ==========================================
# Inyectamos CSS para lograr el diseño deseado:
# - Fondo de la app casi negro (#050505)
# - Tarjetas con transparencia de cristal (rgba)
# - Efecto hover dinámico (la tarjeta se eleva 8px y se ilumina en verde #00ff80)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #050505;
        color: #ffffff;
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        margin-bottom: 15px;
    }
    .weather-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(0, 255, 128, 0.25);
        border-color: #00ff80;
    }
    .weather-icon {
        font-size: 2.8rem;
        margin-bottom: 8px;
    }
    .weather-card h3 {
        margin: 0;
        font-size: 0.9rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .weather-card h2 {
        margin: 8px 0 0 0;
        font-size: 1.6rem;
        color: #ffffff;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Título principal de la aplicación en pantalla
st.title("⛅ Estación Meteorológia IES OLIVA DE LA FRONTERA")
st.markdown("---")

# ==========================================
# 3. CONEXIÓN CON LA API CENTRAL (BACKEND)
# ==========================================
# Dirección web oficial del servidor Flask desplegado en Render
URL_API = "https://servidor-estacion-meteorologica.onrender.com/api/estado"


def obtener_datos():
  """Función que realiza una petición HTTP GET al servidor para obtener

  el diccionario JSON con los datos meteorológicos actualizados.
  """
  try:
    response = requests.get(URL_API, timeout=5)
    # Si la respuesta es exitosa (código 200)
    if response.status_code == 200:
      return response.json()
  except Exception:
    pass
  return None


# Obtenemos los datos ejecutando la función
datos = obtener_datos()

# ==========================================
# 4. RENDERIZADO DE DATOS E INTERFAZ
# ==========================================
if datos:
  # Mostramos la fecha de la última lectura de la estación
  st.caption(f"📅 Última actualización: {datos.get('fecha', 'N/D')}")

  # Distribuimos los datos principales en 3 columnas simétricas
  col1, col2, col3 = st.columns(3)

  with col1:
    # Tarjeta de Temperatura
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">🌡️</div>
            <h3>Temperatura</h3>
            <h2>{datos.get('temperatura_C', '--')} °C</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Tarjeta de Viento
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">💨</div>
            <h3>Viento</h3>
            <h2>{datos.get('viento_kmh', '--')} km/h</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    # Tarjeta de Humedad
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">💧</div>
            <h3>Humedad</h3>
            <h2>{datos.get('humedad_pct', '--')} %</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Tarjeta de Ráfaga de Viento
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">🌪️</div>
            <h3>Ráfaga</h3>
            <h2>{datos.get('rafaga_kmh', '--')} km/h</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
    # Tarjeta de Lluvia
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">🌧️</div>
            <h3>Lluvia</h3>
            <h2>{datos.get('lluvia_acumulada_mm', '--')} mm</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Tarjeta de Índice UV
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">☀️</div>
            <h3>Índice UV</h3>
            <h2>{datos.get('indice_uv', '--')}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

  # Fila inferior en 2 columnas para los parámetros complementarios
  col_a, col_b = st.columns(2)
  with col_a:
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">🔆</div>
            <h3>Radiación Solar</h3>
            <h2>{datos.get('radiacion_solar_W_m2', '--')} W/m²</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_b:
    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-icon">🧭</div>
            <h3>Dir. Viento</h3>
            <h2>{datos.get('direccion_viento_grados', '--')} °</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

  # ==========================================
  # 5. LÓGICA EDUCATIVA Y CONDICIONALES
  # ==========================================
  # Ejemplo de lógica para mostrar avisos personalizados según los valores medidos
  temp = datos.get("temperatura_C", 0)
  if temp and temp > 25:
    st.warning("⚠️ ¡Aviso educativo: Temperatura superior a 25 °C!")

else:
  # Mensaje de error si la API central no responde o hay problemas de red
  st.error("⚠️ No se pudo conectar con el servidor central de Render.")
