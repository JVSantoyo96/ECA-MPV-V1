import pandas as pd

def recomendar(
        rutas: pd.DataFrame,
        cursos: pd.DataFrame,
        *,
        horas: int,
        modalidad: list[str],
        idioma: str,
) -> pd.DataFrame:
    """
    Filtra y puntúa rutas, devuelve TOP-3 DataFrame.

    • horas: disponibles por semana
    • modalidad: lista de strings (puede venir vacía)
    • idioma: string único
    """
    df = rutas.copy()

    # --- FILTROS DUROS ----------------------------------------------------
    # 1. duración (regla simplona: 4h/sem = 1 mes de estudio)
    df = df[df["duracion_meses"] <= max(horas, 1) * 4]

    # 2. modalidad
    if modalidad:                                              # <- evita vacío
        df = df[df["modalidad"].str.lower().isin(
            [m.lower() for m in modalidad]
        )]

    # 3. idioma
    if idioma:
        df = df[df["idioma"].str.lower() == idioma.lower()]

    # Si tras los filtros no queda nada, salimos ya:
    if df.empty:
        return pd.DataFrame()                                  # <- señal vacío

    # --- PUNTAJE ----------------------------------------------------------
    # Normalizamos para que “más pequeño = mejor”
    df["score_precio"]     = df["precio_usd"].rank(method="min")
    df["score_dificultad"] = df["dificultad"].rank(method="min")

    # Ponderación simple (50 % precio, 50 % dificultad)
    df["puntaje"] = df["score_precio"] * 0.5 + df["score_dificultad"] * 0.5

    # --- TOP-3 ------------------------------------------------------------
    top3 = df.nsmallest(3, "puntaje")

    # (Opcional) añadimos cursos dentro de la misma función
    out = []
    for _, fila in top3.iterrows():
        cursos_ruta = cursos[cursos["ruta_id"] == fila["ruta_id"]]

        ruta_formativa = cursos_ruta.to_dict("records") if not cursos_ruta.empty else []

        out.append({
            "nombre"          : fila["nombre"],
            "descripcion"     : fila["descripcion"],
            "duracion_meses"  : int(fila["duracion_meses"]),
            "precio_usd"      : int(fila["precio_usd"]),
            "ies"             : fila["ies"],
            "puntaje"         : float(fila["puntaje"]),
            "ruta_formativa"  : ruta_formativa,
        })

    return pd.DataFrame(out)
