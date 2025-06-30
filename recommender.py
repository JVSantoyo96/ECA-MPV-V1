import pandas as pd

def recomendar(rutas, cursos, horas, modalidad, idioma):
    df = rutas.copy()
    df = df[df["duracion_meses"] <= horas * 4]          # filtro simple horas → meses
    df = df[df["modalidad"].isin(modalidad)]
    df = df[df["idioma"] == idioma]

    df["puntaje"] = (
        (df["precio_usd"].rank(ascending=True)) +      # más barato → mejor
        (df["dificultad"].rank())                      # menor dificultad → mejor
    )
    return df.nsmallest(3, "puntaje")
