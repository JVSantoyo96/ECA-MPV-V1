import streamlit as st
import pandas as pd
from recommender import recomendar

st.set_page_config(page_title="MVP ECA", layout="centered")
st.title("🧭 Tu ruta ideal")
st.write("→ Ajusta filtros y presiona *Recomendar*")

progress = st.progress(0)

# --- formulario completo ---
horas = st.slider("Horas disponibles /sem", 1, 20, 5)
progress.progress(8)

modalidad = st.multiselect(
    "Modalidad",
    ["Virtual", "Presencial", "Híbrido"],
    ["Virtual"]
)
progress.progress(16)

idioma = st.selectbox("Idioma", ["Español", "Inglés"])
progress.progress(24)

objetivo = st.radio(
    "Objetivo",
    ["Primer empleo", "Reskilling", "Upskilling", "Emprender"]
)
progress.progress(32)

intereses = st.multiselect(
    "Reinos de conocimiento (máx 2)",
    ["Multidisciplinar", "Data/AI", "Ciberseguridad",
     "Innovación Social", "Diseño", "Negocios"], max_selections=2)
progress.progress(40)

experiencia = st.slider("Experiencia previa (0–100)", 0, 100, 20)
progress.progress(48)

presupuesto = st.number_input("Presupuesto máx (USD)", 0, 20_000, 1_000)
progress.progress(56)

ubicacion = st.radio("Restricción geográfica",
                     ["Sin límite", "Quiero estudiar en mi ciudad"])
progress.progress(64)

estilo = st.multiselect(
    "Estilo de aprendizaje",
    ["Videos y podcasts", "Lecturas y proyectos escritos",
     "Talleres colaborativos"]
)
progress.progress(72)

horizonte = st.radio(
    "Ritmo preferido",
    ["Sprint intensivo (≤ 3 m)",
     "Constante (3–6 m)",
     "Tranquilo (6–12 m)"]
)
progress.progress(80)

docs = st.file_uploader("Subir CV / notas (opcional)", type=["pdf", "docx"])
progress.progress(88)

habito = st.text_input("Super-hábito a cultivar")
progress.progress(100)

# --- acción ---
if st.button("🎯 Recomendar"):
    rutas  = pd.read_csv("rutas.csv")
    cursos = pd.read_csv("cursos.csv")

    filtros = dict(
        horas      = horas,
        modalidad  = modalidad,
        idioma     = idioma,
        objetivo   = objetivo,
        intereses  = intereses,
        experiencia= experiencia,
        presupuesto= presupuesto,
        ubicacion  = ubicacion,
        estilo     = estilo,
        horizonte  = horizonte
    )

    top3 = recomendar(rutas, cursos, **filtros)

    if not top3.empty:
        for i, r in top3.iterrows():
            st.subheader(f"{'⭐' if i==0 else f'Opción {i+1}'}: {r['nombre']}")
            st.write(f"**Institución:** {r['ies']}")
            st.write(f"**Descripción:** {r['descripcion']}")
            st.write(f"**Duración:** {r['duracion_meses']} meses")
            st.write(f"**Precio:** USD {r['precio_usd']:.0f}")
            st.write(f"**Puntaje:** {r['puntaje']:.2f}")
    else:
        st.warning("No hay coincidencias, prueba otros filtros")
