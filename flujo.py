# flujo.py
# Maquina de estados: dado un diccionario de respuestas ya recolectadas,
# calcula cual es la siguiente pregunta o, si ya hay suficiente
# informacion, el resultado final.
#
# Orden FIJO de las 10 preguntas (siempre se hacen en este orden, sin
# saltarse ninguna), salvo dos casos que dan resultado inmediato porque
# no hay nada mas que evaluar:
#   - Contacto de mucosa con saliva infectada (tipo_agresion == 3)
#   - Agresor es un mamifero distinto de perro/gato (especie == 3)

from clasificacion import clasificar_exposicion

PREGUNTAS = {
    "tipo_agresion": {
        "texto": "Que tipo de agresion o exposicion ocurrio?",
        "opciones": [
            {"valor": 1, "texto": "Mordedura"},
            {"valor": 2, "texto": "Arañazo o rasguño"},
            {"valor": 3, "texto": "Contacto de mucosa con saliva infectada"},
        ],
    },
    "especie": {
        "texto": "Que animal agredio?",
        "opciones": [
            {"valor": 1, "texto": "Perro"},
            {"valor": 2, "texto": "Gato"},
            {"valor": 3, "texto": "Otro mamifero"},
        ],
    },
    "localizacion": {
        "texto": "Donde fue la mordedura, arañazo o lesion?",
        "opciones": [
            {"valor": 1, "texto": "Cabeza, cara o cuello"},
            {"valor": 2, "texto": "Manos o dedos"},
            {"valor": 3, "texto": "Tronco"},
            {"valor": 4, "texto": "Miembros superiores"},
            {"valor": 5, "texto": "Miembros inferiores"},
            {"valor": 6, "texto": "Pies o dedos"},
            {"valor": 7, "texto": "Genitales"},
        ],
    },
    "agresion": {
        "texto": "La agresion fue unica o multiple?",
        "opciones": [
            {"valor": 1, "texto": "Unica"},
            {"valor": 2, "texto": "Multiple"},
        ],
    },
    "extension": {
        "texto": "Que tan profunda fue la lesion?",
        "opciones": [
            {"valor": 1, "texto": "Superficial"},
            {"valor": 2, "texto": "Profunda"},
        ],
    },
    "estado_animal": {
        "texto": "Cual es el estado actual del animal?",
        "opciones": [
            {"valor": 1, "texto": "Vivo"},
            {"valor": 2, "texto": "Muerto"},
            {"valor": 3, "texto": "Desconocido"},
        ],
    },
    "signos_rabia": {
        "texto": "El animal presenta signos de rabia?",
        "opciones": [
            {"valor": 1, "texto": "Con signos"},
            {"valor": 2, "texto": "Sin signos"},
            {"valor": 3, "texto": "Desconocido"},
        ],
    },
    "vacunado": {
        "texto": "El animal esta vacunado contra la rabia?",
        "opciones": [
            {"valor": 1, "texto": "Si"},
            {"valor": 2, "texto": "No"},
            {"valor": 3, "texto": "Desconocido"},
        ],
    },
    "tiene_dueno": {
        "texto": "El animal tiene dueno?",
        "opciones": [
            {"valor": 1, "texto": "Si"},
            {"valor": 2, "texto": "No"},
            {"valor": 3, "texto": "Desconocido"},
        ],
    },
    "ubicacion_animal": {
        "texto": "Ubicacion del animal agresor",
        "opciones": [
            {"valor": 1, "texto": "Observable"},
            {"valor": 2, "texto": "Perdido"},
        ],
    },
}

# Orden fijo en el que siempre se hacen las preguntas.
ORDEN_MAXIMO = [
    "tipo_agresion", "especie", "localizacion", "agresion", "extension",
    "estado_animal", "signos_rabia", "vacunado", "tiene_dueno", "ubicacion_animal",
]


def _pregunta(id_pregunta, respuestas):
    total_respondidas = len(respuestas)
    return {
        "tipo": "pregunta",
        "id": id_pregunta,
        "texto": PREGUNTAS[id_pregunta]["texto"],
        "opciones": PREGUNTAS[id_pregunta]["opciones"],
        "paso": total_respondidas + 1,
        "total_estimado": len(ORDEN_MAXIMO),
    }


def _resultado(resultado, respuestas):
    return {
        "tipo": "resultado",
        "resultado": resultado,
        "respuestas": respuestas,
    }


def siguiente_paso(respuestas):
    # 1. Tipo de agresion o exposicion
    tipo_agresion = respuestas.get("tipo_agresion")
    if tipo_agresion is None:
        return _pregunta("tipo_agresion", respuestas)

    if tipo_agresion == 3:
        motivos_extra = clasificar_exposicion(tipo_agresion=3)
        return _resultado(motivos_extra, respuestas)

    # 2. Especie del animal
    especie = respuestas.get("especie")
    if especie is None:
        return _pregunta("especie", respuestas)

    if especie == 3:
        return _resultado(
            clasificar_exposicion(especie=3, tipo_agresion=tipo_agresion),
            respuestas,
        )

    # 3. Localizacion de la lesion
    localizacion = respuestas.get("localizacion")
    if localizacion is None:
        return _pregunta("localizacion", respuestas)

    # 4. Numero de agresiones (unica/multiple)
    agresion = respuestas.get("agresion")
    if agresion is None:
        return _pregunta("agresion", respuestas)

    # 5. Profundidad de la lesion
    extension = respuestas.get("extension")
    if extension is None:
        return _pregunta("extension", respuestas)

    # 6. Estado actual del animal
    estado_animal = respuestas.get("estado_animal")
    if estado_animal is None:
        return _pregunta("estado_animal", respuestas)

    # 7. Signos de rabia
    signos_rabia = respuestas.get("signos_rabia")
    if signos_rabia is None:
        return _pregunta("signos_rabia", respuestas)

    # 8. Vacunacion del animal
    vacunado = respuestas.get("vacunado")
    if vacunado is None:
        return _pregunta("vacunado", respuestas)

    # 9. Propietario del animal
    tiene_dueno = respuestas.get("tiene_dueno")
    if tiene_dueno is None:
        return _pregunta("tiene_dueno", respuestas)

    # 10. Ubicacion actual del animal
    ubicacion_animal = respuestas.get("ubicacion_animal")
    if ubicacion_animal is None:
        return _pregunta("ubicacion_animal", respuestas)

    # Ya se tienen las 10 respuestas: se calcula el resultado final.
    resultado = clasificar_exposicion(
        especie=especie,
        estado_animal=estado_animal,
        signos_rabia=signos_rabia,
        tiene_dueno=tiene_dueno,
        ubicacion_animal=ubicacion_animal,
        localizacion=localizacion,
        agresion=agresion,
        extension=extension,
        vacunado=vacunado,
        tipo_agresion=tipo_agresion,
    )
    return _resultado(resultado, respuestas)
