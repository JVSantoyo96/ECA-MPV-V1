import streamlit as st
from recommender import Recommender

st.set_page_config(page_title="ECA Recommender", layout="centered")

st.title("🧭 Tu Ruta de Aprendizaje Ideal")



st.write("Responde este cuestionario corto para descubrir tu ruta formativa ideal.")

# Barra de progreso
progress = st.progress(0)

# Pregunta 1
objetivo = st.radio(
    "🚀 ¿Cuál es tu meta final?",
    ["Primer empleo", "Reskilling", "Upskilling", "Emprender"]
)
progress.progress(8)

# Pregunta 2
intereses = st.multiselect(
    "🎯 Elige hasta 2 reinos de conocimiento donde quieras brillar:",
    ["Multidisciplinar", "Data/AI", "Ciberseguridad", "Innovación Social", "Diseño", "Negocios"],
    max_selections=2
)
progress.progress(16)

# Pregunta 3
experiencia = st.slider(
    "🏆 ¿Qué tan lejos has viajado en esos reinos? (0 km = novato, 100 km = experto)",
    0, 100, 20
)
progress.progress(24)

# Pregunta 4
horas_semana = st.slider(
    "⏰ ¿Cuántas horas semanales puedes dedicar?",
    0, 20, 5
)
progress.progress(32)

# Pregunta 5
horizonte_meses = st.radio(
    "📅 Marca tu ritmo preferido de misiones:",
    ["Sprint intensivo (≤ 3 meses)", "Constante (3-6 meses)", "Tranquilo (6-12 meses)"]
)
progress.progress(40)

# Pregunta 6
modalidad = st.multiselect(
    "🏠 ¿En qué modalidad te sientes más cómodo para aprender?",
    ["Virtual", "Presencial", "Híbrido"]
)
progress.progress(48)

# Pregunta 7
presupuesto = st.number_input(
    "💰 Tu bolsa de oro para esta campaña (USD máximo):",
    min_value=0, max_value=20000, value=1000
)
progress.progress(56)

# Pregunta 8
ubicacion = st.radio(
    "📍 ¿Tienes restricción geográfica?",
    ["Sin límite", "Quiero estudiar en mi ciudad"]
)
progress.progress(64)

# Pregunta 9
idiomas = st.multiselect(
    "🗣️ Idiomas en los que te gustaría aprender:",
    ["Español", "Inglés", "Francés", "Portugués"]
)
progress.progress(72)

# Pregunta 10
estilo_aprendizaje = st.multiselect(
    "🎮 Elige tu estilo de juego de aprendizaje:",
    ["Videos y podcasts", "Lecturas y proyectos escritos", "Talleres colaborativos"]
)
progress.progress(80)

# Pregunta 11
docs = st.file_uploader("📄 ¿Te gustaría subir tu CV o notas?", type=["pdf","doc","docx"])
progress.progress(88)

# Pregunta 12
habito = st.text_input("🌟 ¿Cuál super-hábito te gustaría cultivar?")
progress.progress(100)

# Botón para enviar
if st.button("🔍 Mostrar mi ruta recomendada"):
    st.success("✅ ¡Respuestas registradas!")
    st.write("**Vista previa de tus respuestas:**")

    respuestas = {
        "objetivo": objetivo,
        "intereses": intereses,
        "experiencia": experiencia,
        "horas_semana": horas_semana,
        "horizonte_meses": horizonte_meses,
        "modalidad": modalidad,
        "presupuesto": presupuesto,
        "ubicacion": ubicacion,
        "idiomas": idiomas,
        "estilo_aprendizaje": estilo_aprendizaje,
        "habito": habito
    }

    rec = Recommender("rutas.csv", "cursos.csv")
    top3 = rec.recomendar(respuestas)

    if top3:
        for idx, ruta in enumerate(top3):
            if idx == 0:
                st.subheader(f"⭐ Mejor Ruta Recomendada: {ruta['ruta']}")
            else:
                st.subheader(f"Opción {idx+1}: {ruta['ruta']}")
            st.write(f"**Institución:** {ruta['ies']}")
            st.write(f"**Descripción:** {ruta['descripcion']}")
            st.write(f"**Duración:** {ruta['duracion_meses']} meses" if ruta['duracion_meses'] > 0 else "Duración: Sin dato")
            st.write(f"**Precio estimado:** USD {ruta['precio']:.2f}" if ruta['precio'] > 0 else "Precio estimado: Sin dato")
            st.write(f"**Puntaje:** {ruta['puntaje']:.2f}")
           


            
            if ruta["ruta_formativa"]:
                st.subheader("Ruta Formativa Detallada:")
                for curso in ruta["ruta_formativa"]:
                    st.markdown(
                        f"""
                        - **{curso['curso_nombre']}** ({curso['duracion_horas']} horas)  
                            Microcredencial: *{curso['microcredencial_nombre']}*
                        """
                    )
            else:
                st.warning("⚠️ Esta ruta no tiene cursos asociados aún.")

    else:
        st.warning("No encontramos rutas con esos filtros, ajusta tus criterios.")
