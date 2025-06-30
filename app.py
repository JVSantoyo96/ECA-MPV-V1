import streamlit as st
import pandas as pd
from recommender import recommend

st.set_page_config(page_title="MVP ECA", layout="centered")
st.title("🧭 Tu ruta ideal")

st.write("→ Ajusta filtros y presiona *Recomendar*")

horas = st.slider("Horas disponibles /sem", 1, 20, 5)
modalidad = st.multiselect("Modalidad", ["Virtual","Presencial","Híbrido"], ["Virtual"])
idioma = st.selectbox("Idioma", ["Español","Inglés"])

if st.button("🎯 Recomendar"):
    rutas = pd.read_csv("rutas.csv")
    cursos = pd.read_csv("cursos.csv")
    top3 = recommend(rutas, cursos, horas, modalidad, idioma)
    if top3.empty:
        st.warning("No hay coincidencias, prueba otros filtros")
    else:
        for _, r in top3.iterrows():
            st.subheader(f"⭐ {r['nombre']}")
            st.write(r['descripcion'])
            st.write(f"Dura {r['duracion_meses']} meses • ${r['precio_usd']}")

