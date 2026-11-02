import requests
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Mi Estación Meteorológica", page_icon="⛅", layout="centered"
)

st.title("⛅ Estación Meteorológica Escolar")
st.write(
    "Bienvenido a mi aplicación del tiempo conectada a la API central de la"
    " clase."
)
st.markdown("---")

# ==========================================
# 2. CONEXIÓN CON LA API DEL PROFESOR
# ==========================================
# Esta es la dirección web de nuestro servidor central en Render
URL_API = "https://estacion-meteorologica.onrender.com/api/estado"


def obtener_datos_meteorologicos():
  """Función que realiza una petición HTTP al servidor para obtener el JSON con los datos."""
  try:
    respuesta = requests.get(URL_API, timeout=5)
    # Si la conexión es exitosa (código 200)
    if respuesta.status_code == 200:
      return respuesta.json()
  except Exception as e:
    st.error(f"Error de conexión: {e}")
  return None


# Guardamos los datos obtenidos en una variable
datos = obtener_datos_meteorologicos()

# ==========================================
# 3. INTERFAZ VISUAL DE LA APP
# ==========================================
if datos:
  # Mostramos la fecha y hora de la última actualización de la estación
  st.caption(f"📅 Última actualización: {datos.get('fecha', 'N/D')}")

  # Dividimos la pantalla en 2 columnas para organizar la información
  col1, col2 = st.columns(2)

  with col1:
    # st.metric crea una tarjeta visual automática muy limpia
    st.metric(
        label="🌡️ Temperatura", value=f"{datos.get('temperatura_C', '--')} °C"
    )
    st.metric(label="💨 Viento", value=f"{datos.get('viento_kmh', '--')} km/h")

  with col2:
    st.metric(label="💧 Humedad", value=f"{datos.get('humedad_pct', '--')} %")
    st.metric(
        label="🌧️ Lluvia",
        value=f"{datos.get('lluvia_acumulada_mm', '--')} mm",
    )

  # ==========================================
  # 4. LÓGICA Y ALERTAS PERSONALIZADAS (PARA ALUMNOS)
  # ==========================================
  # Los alumnos pueden modificar esto para crear sus propias alertas
  temperatura_actual = datos.get("temperatura_C", 0)

  if temperatura_actual > 25:
    st.warning("⚠️ ¡Aviso: Hace calor! Temperatura superior a 25 °C.")
  elif temperatura_actual < 10:
    st.info("❄️ ¡Aviso: Hace frío! Temperatura inferior a 10 °C.")
  else:
    st.success("👍 El tiempo está agradable.")

else:
  # Mensaje si el servidor no responde
  st.error("⚠️ No se ha podido conectar con el servidor central de la estación.")


