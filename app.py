import streamlit as st
import pandas as pd
from recommender import recomendar

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
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.25rem;
  padding: 0.75rem 1.5rem;
  box-shadow: 0 0 0.25rem rgba(0,0,0,.2);
  transition: transform 0.1s ease-in-out;
}
div.stButton > button:first-child:hover {
  transform: scale(1.05);
  cursor: pointer;
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
        "horas": answers["horas"],
        "modalidad": answers["modalidad"],
        "idioma": answers["idiomas"][0] if answers["idiomas"] else "Español",
        "exp": answers["experiencia"]          # <- ya la tienes del slider 0-100
    }
    recomendaciones = recomendar(rutas, cursos, **filtros)

    if recomendaciones.empty:
        st.warning("⚠️ No hay coincidencias, prueba otros filtros.")
    else:
        st.success("✨ ¡Listo! Estas son tus rutas recomendadas:")
        for idx, row in recomendaciones.iterrows():
            top_tag = "⭐ Mejor coincidencia" if idx == 0 else f"Opción {idx+1}"
            with st.container():
                st.markdown(f"<div class='card'><h3>{top_tag}: {row['nombre']}</h3>", unsafe_allow_html=True)
                st.write(f"**Institución:** {row['ies']}")
                st.write(f"**Descripción:** {row['descripcion']}")
                st.write(f"**Duración:** {int(row['duracion_meses'])} meses · **Precio:** USD {int(row['precio_usd']):,}")

                # Lista de cursos
                cursos_ruta = cursos[cursos['ruta_id'] == row['ruta_id']]
                if not cursos_ruta.empty:
                    with st.expander("▶ Ver micro‑cursos"):
                        for _, c in cursos_ruta.iterrows():
                            st.markdown(f"- **{c['curso_nombre']}** ({c['duracion_horas']} h) — _{c['microcredencial_nombre']}_")
                st.markdown("</div>", unsafe_allow_html=True)
