# flujo.py
# Convierte el arbol de decision de preguntas.py (que usaba input()) en una
# maquina de estados sin bloqueo: dado un diccionario de respuestas ya
# recolectadas, calcula cual es la siguiente pregunta o, si ya hay
# suficiente informacion, el resultado final.
#
# Esto permite que cada "paso" sea una peticion HTTP independiente desde
# el navegador (la interfaz web), en vez de una llamada a input() en consola.

from clasificacion import clasificar_exposicion

PREGUNTAS = {
    "especie": {
        "texto": "Que animal agredio?",
        "opciones": [
            {"valor": 1, "texto": "Perro"},
            {"valor": 2, "texto": "Gato"},
            {"valor": 3, "texto": "Otro mamifero"},
        ],
    },
    "estado_animal": {
        "texto": "Estado del animal?",
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
        ],
    },
    "ubicacion_animal": {
        "texto": "Donde esta el animal?",
        "opciones": [
            {"valor": 1, "texto": "Observable"},
            {"valor": 2, "texto": "Perdido"},
        ],
    },
    "es_observable": {
        "texto": "Es posible mantener al animal en observacion 10 dias?",
        "opciones": [
            {"valor": 1, "texto": "Si"},
            {"valor": 2, "texto": "No"},
            {"valor": 3, "texto": "Desconocido"},
        ],
    },
    "localizacion": {
        "texto": "Donde fue la mordedura o lesion?",
        "opciones": [
            {"valor": 1, "texto": "Cabeza, cara o cuello"},
            {"valor": 2, "texto": "Manos o dedos"},
            {"valor": 3, "texto": "Tronco"},
            {"valor": 4, "texto": "Miembros superiores"},
            {"valor": 5, "texto": "Miembros inferiores"},
            {"valor": 6, "texto": "Pies, dedos"},
            {"valor": 7, "texto": "Genitales"},
        ],
    },
    "tipo_agresion": {
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
}

# Orden maximo posible, usado solo para calcular el progreso aproximado.
ORDEN_MAXIMO = [
    "especie", "estado_animal", "signos_rabia", "vacunado", "tiene_dueno",
    "ubicacion_animal", "es_observable", "localizacion", "tipo_agresion",
    "extension",
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
    """Dado el dict de respuestas acumuladas hasta ahora, decide cual es
    el siguiente paso: otra pregunta, o ya el resultado final.
    Replica exactamente la logica secuencial que antes vivia en
    preguntas.py / hacer_preguntas()."""

    especie = respuestas.get("especie")
    if especie is None:
        return _pregunta("especie", respuestas)

    if especie == 3:
        return _resultado(clasificar_exposicion(especie=3), respuestas)

    estado_animal = respuestas.get("estado_animal")
    if estado_animal is None:
        return _pregunta("estado_animal", respuestas)

    signos_rabia = respuestas.get("signos_rabia")
    if signos_rabia is None:
        return _pregunta("signos_rabia", respuestas)

    if estado_animal == 2 or signos_rabia == 1:
        return _resultado(
            clasificar_exposicion(
                especie=especie,
                estado_animal=estado_animal,
                signos_rabia=signos_rabia,
            ),
            respuestas,
        )

    vacunado = respuestas.get("vacunado")
    if vacunado is None:
        return _pregunta("vacunado", respuestas)

    tiene_dueno = respuestas.get("tiene_dueno")
    if tiene_dueno is None:
        return _pregunta("tiene_dueno", respuestas)

    ubicacion_animal = respuestas.get("ubicacion_animal")
    if ubicacion_animal is None:
        return _pregunta("ubicacion_animal", respuestas)

    es_observable = respuestas.get("es_observable")
    if es_observable is None:
        return _pregunta("es_observable", respuestas)

    observable_confirmado = (
        es_observable == 1 and tiene_dueno == 1 and ubicacion_animal == 1
    )

    if observable_confirmado:
        return _resultado(
            clasificar_exposicion(
                especie=especie,
                estado_animal=estado_animal,
                signos_rabia=signos_rabia,
                es_observable=es_observable,
                tiene_dueno=tiene_dueno,
                ubicacion_animal=ubicacion_animal,
                vacunado=vacunado,
            ),
            respuestas,
        )

    localizacion = respuestas.get("localizacion")
    if localizacion is None:
        return _pregunta("localizacion", respuestas)

    if localizacion in [1, 2, 6, 7]:
        return _resultado(
            clasificar_exposicion(
                especie=especie,
                estado_animal=estado_animal,
                signos_rabia=signos_rabia,
                es_observable=es_observable,
                tiene_dueno=tiene_dueno,
                ubicacion_animal=ubicacion_animal,
                localizacion=localizacion,
                vacunado=vacunado,
            ),
            respuestas,
        )

    tipo_agresion = respuestas.get("tipo_agresion")
    if tipo_agresion is None:
        return _pregunta("tipo_agresion", respuestas)

    if tipo_agresion == 2:
        return _resultado(
            clasificar_exposicion(
                especie=especie,
                estado_animal=estado_animal,
                signos_rabia=signos_rabia,
                es_observable=es_observable,
                tiene_dueno=tiene_dueno,
                ubicacion_animal=ubicacion_animal,
                localizacion=localizacion,
                tipo_agresion=tipo_agresion,
                vacunado=vacunado,
            ),
            respuestas,
        )

    extension = respuestas.get("extension")
    if extension is None:
        return _pregunta("extension", respuestas)

    resultado = clasificar_exposicion(
        especie=especie,
        estado_animal=estado_animal,
        signos_rabia=signos_rabia,
        es_observable=es_observable,
        tiene_dueno=tiene_dueno,
        ubicacion_animal=ubicacion_animal,
        localizacion=localizacion,
        tipo_agresion=tipo_agresion,
        extension=extension,
        vacunado=vacunado,
    )
    return _resultado(resultado, respuestas)
