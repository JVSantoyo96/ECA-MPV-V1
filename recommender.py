import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

class Recommender:
    def __init__(self, rutas, cursos):
        self.rutas = rutas
        self.cursos = cursos

    def recomendar(self, respuestas):

        # 1. FILTROS DUROS con fallback
        rutas = self.rutas.copy()
        filtradas = rutas[
            (rutas["precio_usd"] <= respuestas["presupuesto"]) &
            (rutas["modalidad"].apply(lambda m: any(mod in m for mod in respuestas["modalidad"]))) &
            (rutas["idioma"].apply(lambda i: any(idi in i for idi in respuestas["idiomas"])))
        ]
        # Si hay al menos 3 rutas que cumplen filtros, úsalas;
        # de lo contrario, volvemos al catálogo completo
        if len(filtradas) >= 3:
            rutas = filtradas.copy()
        else:
            rutas = self.rutas.copy()
        # 2. VECTORIZACIÓN DE SEÑALES
        temas = ["Multidisciplinar","Data/AI","Ciberseguridad","Innovación Social","Diseño","Negocios"]
        user_tematica = np.array([[1 if t in respuestas["intereses"] else 0 for t in temas]])
        ruta_tematica = np.array(
            rutas["tematica"].astype(str)
             .apply(lambda txt: [1 if t in txt else 0 for t in temas])
             .to_list()
        )

        scaler = MinMaxScaler()
        ruta_diff_norm   = scaler.fit_transform(rutas[["dificultad_num"]])
        user_exp_norm    = scaler.transform([[respuestas["experiencia"]]])
        ruta_precio_norm = scaler.fit_transform(rutas[["precio_usd"]])
        user_prec_norm   = scaler.transform([[respuestas["presupuesto"]]])
        ruta_dur_norm    = scaler.fit_transform(rutas[["duracion_meses"]])
        user_horas_norm  = scaler.transform([[respuestas["horas"]]])

        # 3. CÁLCULO DE PUNTAJE COMPUESTO
        sim          = cosine_similarity(user_tematica, ruta_tematica).flatten()
        score_diff   = 1 - np.abs(user_exp_norm - ruta_diff_norm).flatten()
        score_price  = 1 - np.abs(user_prec_norm - ruta_precio_norm).flatten()
        score_horas  = 1 - np.abs(user_horas_norm - ruta_dur_norm).flatten()

        rutas["score"] = (
            0.5 * sim +
            0.2 * score_diff +
            0.2 * score_price +
            0.1 * score_horas
        )

        # 4. DESEMPATE ALEATORIO
        rng = np.random.default_rng()
        rutas["score"] += rng.random(len(rutas)) * 1e-4

        # 5. ORDENAR TODAS LAS RUTAS Y DEVOLVER
        resultado = []
        for _, fila in rutas.sort_values("score", ascending=False).iterrows():
            cursos_ruta = self.cursos[self.cursos["ruta_id"] == fila["ruta_id"]]
            resultado.append({
                "ruta":            fila["nombre"],
                "ies":             fila["ies"],
                "descripcion":     fila["descripcion"],
                "duracion_meses":  fila["duracion_meses"],
                "precio":          fila["precio_usd"],
                "puntaje":         round(fila["score"], 3),
                "ruta_formativa":  cursos_ruta.to_dict("records")
            })
        return resultado
