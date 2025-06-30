import pandas as pd

class Recommender:
    def __init__(self, rutas_file, cursos_file):
        # primero cargar el CSV
        self.rutas = pd.read_csv(rutas_file)

        # convertir precios a numérico, asegurando no NaN
        self.rutas["precio_usd"] = pd.to_numeric(
            self.rutas["precio_usd"], errors="coerce"
        ).fillna(0)

        # asegúrate de tener la columna puntaje inicializada
        if "puntaje" not in self.rutas.columns:
            self.rutas["puntaje"] = 0

        self.cursos = pd.read_csv(cursos_file)
        self.cursos.columns = self.cursos.columns.str.strip()

        print("✅ Columnas rutas:", self.rutas.columns)
        print("✅ Primeras rutas:", self.rutas.head())
        print("✅ Columnas cursos:", self.cursos.columns)
        print("✅ Primeros cursos:", self.cursos.head())


def recomendar(self, respuestas):
    puntaje = []

    for _, fila in self.rutas.iterrows():
        score = 0

        # presupuesto
        if fila["precio_usd"] <= respuestas["presupuesto"]:
            score += 1

        # modalidad (acepta lista)
        if any(mod in fila["modalidad"] for mod in respuestas["modalidad"]):
            score += 1

        # idioma (acepta lista)
        if any(idioma in fila["idioma"] for idioma in respuestas["idiomas"]):
            score += 1

        # dificultad aproximada
        if respuestas["experiencia"] >= 50 and fila["dificultad"] in ["Intermedia", "Avanzada"]:
            score += 1
        elif respuestas["experiencia"] < 50 and fila["dificultad"] == "Básica":
            score += 1

        puntaje.append(score)

    self.rutas["puntaje"] = puntaje
    recomendadas = self.rutas.sort_values("puntaje", ascending=False).head(3)

    resultado = []
    for _, fila in recomendadas.iterrows():
        cursos_ruta = self.cursos[self.cursos["ruta_id"] == fila["ruta_id"]]
        ruta_formativa = []
        for _, c in cursos_ruta.iterrows():
            ruta_formativa.append({
                "curso_id": c["curso_id"],
                "curso_nombre": c["curso_nombre"],
                "duracion_horas": c["duracion_horas"],
                "microcredencial_id": c["microcredencial_id"],
                "microcredencial_nombre": c["microcredencial_nombre"]
            })

        resultado.append({
            "ruta": fila["nombre"],
            "ies": fila["ies"],
            "descripcion": fila["descripcion"],
            "duracion_meses": fila["duracion_meses"],
            "precio": fila["precio_usd"],
            "puntaje": fila["puntaje"],
            "ruta_formativa": ruta_formativa
        })

    return resultado
