import pandas as pd
import pytest
from recommender import Recommender

def test_recommender_top3_distintos():
    # Cargar datos de rutas y cursos
    rutas = pd.read_csv("rutas.csv")
    cursos = pd.DataFrame({
        "ruta_id": [],
        "curso_nombre": [],
        "duracion_horas": [],
        "microcredencial_nombre": []
    })  # No se usan los cursos para este test

    user = {
        "intereses": ["Data/AI"],
        "experiencia": 10,
        "modalidad": ["Virtual"],
        "presupuesto": 500,
        "idiomas": ["Español"]
    }

    rec = Recommender(rutas, cursos)
    resultado = rec.recomendar(user)

    # 1) Debe retornar una lista de longitud 3
    assert isinstance(resultado, list)
    assert len(resultado) == 3

    # 2) Los nombres de las rutas deben ser distintos
    nombres = [r["ruta"] for r in resultado]
    assert len(set(nombres)) == 3
