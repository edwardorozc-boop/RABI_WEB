# clasificacion.py
# Motor de decisión de RABI
# Basado en el "Algoritmo para la clasificación de agresiones por animal
# potencialmente transmisor de rabia" del Instituto Nacional de Salud (INS)
#
# Todas las preguntas se responden con números (1, 2, 3...)


# ============================================================
#  PREGUNTAS Y OPCIONES
# ============================================================
# 1. especie:            1 = Perro | 2 = Gato | 3 = Otro mamífero
# 2. signos_rabia:       1 = Con signos de rabia | 2 = Sin signos | 3 = Desconocido
# 3. es_observable:      1 = Sí | 2 = No | 3 = Desconocido
# 4. tipo_agresion:      1 = Única | 2 = Múltiple
# 5. extension:          1 = Superficial | 2 = Profunda
# 6. localizacion:       1 = Cabeza, cara, cuello
#                        2 = Manos o dedos
#                        3 = Tronco
#                        4 = Miembros superiores
#                        5 = Miembros inferiores
#                        6 = Pies, dedos
#                        7 = Genitales
# 7. vacunado:           1 = Sí | 2 = No | 3 = Desconocido
# 8. tiene_dueno:        1 = Sí | 2 = No
# 9. estado_animal:      1 = Vivo | 2 = Muerto | 3 = Desconocido
# 10. ubicacion_animal:  1 = Observable | 2 = Perdido
#
# Resultado (tipo_exposicion):
#   1 = No exposición | 2 = Exposición leve | 3 = Exposición grave

# Localizaciones consideradas de alto riesgo
ZONAS_ALTO_RIESGO = [1, 2, 6, 7]  # cabeza/cara/cuello, manos/dedos, pies/dedos, genitales

TEXTO_CLASIFICACION = {
    1: "No exposición",
    2: "Exposición leve",
    3: "Exposición grave"
}


def clasificar_exposicion(
    especie,
    signos_rabia=None,
    es_observable=None,
    tipo_agresion=None,
    extension=None,
    localizacion=None,
    vacunado=None,
    tiene_dueno=None,
    estado_animal=None,
    ubicacion_animal=None
):
    """
    Clasifica el nivel de exposición rábica siguiendo el algoritmo del INS.

    Retorna:
        dict: {
            "codigo": 1 | 2 | 3,
            "clasificacion": "No exposición" | "Exposición leve" | "Exposición grave",
            "motivos": [lista de razones que explican el resultado]
        }
    """
    motivos = []

    # --- Paso 1: especie agresora ---
    # Perro (1) y gato (2) pueden observarse; cualquier otro mamífero (3) no.
    if especie == 3:
        motivos.append("El agresor es un mamífero distinto de perro/gato: no es posible mantenerlo en observación")
        return _resultado(3, motivos)

    # --- Paso 2: estado del animal / signos de rabia ---
    if estado_animal == 2:
        motivos.append("El animal murió")
        return _resultado(3, motivos)

    if signos_rabia == 1:
        motivos.append("El animal presenta signos compatibles con rabia")
        return _resultado(3, motivos)

    # --- Paso 3: ¿es observable? ---
    # Se considera observable solo si la respuesta es "Sí" y el animal
    # tiene dueño y está ubicado (no perdido). Si algo es desconocido,
    # se asume "no observable" por precaución.
    es_realmente_observable = (
        es_observable == 1
        and tiene_dueno == 1
        and ubicacion_animal == 1
    )

    if not es_realmente_observable:
        motivos.append("El animal no puede mantenerse en observación (sin dueño, perdido o de procedencia desconocida)")

        if tipo_agresion == 2:
            motivos.append("Lesión múltiple")
            return _resultado(3, motivos)

        if extension == 2:
            motivos.append("Herida profunda")
            return _resultado(3, motivos)

        if localizacion in ZONAS_ALTO_RIESGO:
            motivos.append("Localización en zona de alto riesgo")
            return _resultado(3, motivos)

        motivos.append("Herida superficial en zona de bajo riesgo, pero sin posibilidad de observar al animal")
        return _resultado(2, motivos)

    # --- Paso 4: animal observable y con dueño ---
    # Si el animal tiene dueño y puede mantenerse en observación 10 días,
    # se clasifica directo como No exposición, sin importar si está
    # vacunado, el tipo de agresión (mordedura/rasguño) o la localización.
    motivos.append("El animal tiene dueño y puede mantenerse en observación durante 10 días")
    return _resultado(1, motivos)


def _resultado(codigo, motivos):
    """Empaqueta el resultado final en el formato esperado."""
    return {
        "codigo": codigo,
        "clasificacion": TEXTO_CLASIFICACION[codigo],
        "motivos": motivos
    }
