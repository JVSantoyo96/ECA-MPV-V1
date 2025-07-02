import streamlit as st
import pandas as pd
from recommender import Recommender

st.set_page_config(page_title="MVP ECA", page_icon="🧭", layout="centered")

# ────────────────────────────────────────────────────────────────────────────────
# 🎨 — Estilos globales (paleta neutra + rojo acento) y tamaño de fuente
# ────────────────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* Fuentes + sliders rojos */
:root {
  --primary-color: #E63946;   /* rojo acento */
  --text-color: #1d3557;      /* azul oscuro */
}
html, body, [class*="css"]  {
  font-family: 'Inter', sans-serif;
  color: var(--text-color);
}
[data-testid="stSlider"] span[data-baseweb="slider"] {
  color: var(--primary-color) !important;
}
/* Botón principal */
div.stButton > button:first-child {
  background‑color: white;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  border-radius: 8px;
  font-weight: 600;
    font-size: 1.2rem;
  padding: 0.6rem 1.4rem;
  box-shadow: 0 0 0 3px rgba(230,57,70,0.15);
  transition: background-color 0.2s, color 0.2s;
}
div.stButton > button:first-child:hover {
  background-color: var(--primary-color);
  color: white;
}
/* Tarjeta recomendación */
.card {
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# 🧭 Cabecera
# ────────────────────────────────────────────────────────────────────────────────
st.title("🧭 Tu ruta ideal")
st.markdown("→ **Ajusta filtros y presiona _Recomendar_**")

# Contenedor para barra de progreso
progress_bar = st.progress(0)
step = 100 // 12  # 12 preguntas

answers = {}

# ────────────────────────────────────────────────────────────────────────────────
# Preguntas gamificadas (12)
# ────────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    answers["objetivo"] = st.radio(
        "🚀 Imagina tu meta final… ¿qué emblema te gustaría desbloquear?",
        ["Primer empleo", "Reskilling", "Upskilling", "Emprender"])
progress_bar.progress(step)

answers["intereses"] = st.multiselect(
    "🎯 Elige hasta **2** reinos de conocimiento donde quieras brillar:",
    ["Multidisciplinar", "Data/AI", "Ciberseguridad", "Innovación Social", "Diseño", "Negocios"],
    max_selections=2)
progress_bar.progress(step*2)

answers["experiencia"] = st.slider("🏆 ¿Qué tan lejos has viajado en esos reinos? (0 km = novato, 100 km = experto)", 0, 100, 50)
progress_bar.progress(step*3)

answers["horas"] = st.slider("⏰ ¿Cuántas horas semanales puedes dedicar?", 1, 20, 5)
progress_bar.progress(step*4)

answers["ritmo"] = st.radio(
    "📅 Marca tu ritmo preferido de misiones:",
    ["Sprint intensivo (≤ 3 meses)", "Constante (3‑6 meses)", "Tranquilo (6‑12 meses)"])
progress_bar.progress(step*5)

answers["modalidad"] = st.multiselect("🏠 ¿En qué modalidad te sientes más cómodo para aprender?", ["Virtual", "Presencial", "Híbrido"], ["Virtual"])
progress_bar.progress(step*6)

answers["presupuesto"] = st.number_input("💰 Tu bolsa de oro para esta campaña (USD máx):", 0, 20000, 1000, step=100)
progress_bar.progress(step*7)

answers["geo"] = st.radio("📍 ¿Tienes limitación geográfica?", ["Sin límite", "Quiero estudiar en mi ciudad"])
progress_bar.progress(step*8)

answers["idiomas"] = st.multiselect("🗣️ Idiomas en los que disfrutas aprender:", ["Español", "Inglés", "Francés", "Portugués"], ["Español"])
progress_bar.progress(step*9)

answers["estilo"] = st.multiselect("🎮 Elige tu estilo de juego de aprendizaje:", ["Videos y podcasts", "Lecturas y proyectos escritos", "Talleres colaborativos"])
progress_bar.progress(step*10)

answers["docs"] = st.file_uploader("📄 ¿Te gustaría subir tu CV o notas?", type=["pdf", "doc", "docx"], accept_multiple_files=False)
progress_bar.progress(step*11)

answers["habito"] = st.text_input("🌟 ¿Cuál super‑hábito te gustaría cultivar?")
progress_bar.progress(100)

# ────────────────────────────────────────────────────────────────────────────────
# Acción principal – Recomendar
# ────────────────────────────────────────────────────────────────────────────────
if st.button("🎯 Recomendar"):
    # Carga datasets
    rutas = pd.read_csv("rutas.csv")
    cursos = pd.read_csv("cursos.csv")

    # Llamada al core (solo las variables que entiende la función v0)
   
    filtros = {
        "intereses":   answers["intereses"],
        "experiencia": answers["experiencia"],
        "presupuesto": answers["presupuesto"],
        "modalidad":   answers["modalidad"] or ["Virtual","Presencial","Híbrido"],
        "idiomas":     answers["idiomas"]  or ["Español"],
        "horas":       answers["horas"],        # horas semanales disponibles
        "estilo":      answers["estilo"] or ["Videos y podcasts", "Lecturas y proyectos escritos", "Talleres colaborativos"],
        "docs":        answers["docs"],
        "habito":      answers["habito"]
      }

    
        # 🛠️ Instanciamos y obtenemos la lista de resultados

    rec         = Recommender(rutas, cursos)
    all_results = rec.recomendar(filtros)     # lista completa ordenada por afinidad
    resultado   = all_results[:3]             # nos quedamos sólo con las 3 mejores


    # Si no hay resultados (lista vacía), mostramos un warning
    if not resultado:
        st.warning("No se encontraron rutas que cumplan tu perfil.")
    else:
        # Aquí va tu código de renderizado original,
        # pero usando la lista `resultado`
        for ruta in resultado:
            st.subheader(ruta["ruta"])
            st.write(f"**IES:** {ruta['ies']}")
            st.write(f"**Precio:** {ruta['precio']} USD")
            st.write(f"**Duración:** {ruta['duracion_meses']} meses")
            st.write(f"**Puntaje:** {ruta['puntaje']}") 
             
            # — Aquí abrimos un expander para listar los cursos —
            cursos_ruta = ruta["ruta_formativa"]
            if cursos_ruta:
                with st.expander("👉 Ver cursos de esta ruta"):
                    for curso in cursos_ruta:
                        st.write(
                            f"- **{curso['curso_nombre']}** "
                            f"({curso['duracion_horas']} h) – "
                            f"{curso['microcredencial_nombre']}"
                        )                                            

