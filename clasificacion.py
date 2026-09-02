ZONAS_ALTO_RIESGO = [1, 2, 6, 7]

TEXTO_CLASIFICACION = {
    1: "No exposicion",
    2: "Exposicion leve",
    3: "Exposicion grave"
}


def clasificar_exposicion(
    especie=None,
    signos_rabia=None,
    tipo_agresion=None,
    agresion=None,
    extension=None,
    localizacion=None,
    vacunado=None,
    tiene_dueno=None,
    estado_animal=None,
    ubicacion_animal=None,
):
    motivos = []

    if tipo_agresion == 3:
        motivos.append("Contacto de mucosa con saliva potencialmente infectada")
        return _resultado(3, motivos)

    if especie == 3:
        motivos.append("El agresor es un mamifero distinto de perro/gato: no es posible mantenerlo en observacion")
        return _resultado(3, motivos)

    if estado_animal == 2:
        motivos.append("El animal murio")
        return _resultado(3, motivos)

    if signos_rabia == 1:
        motivos.append("El animal presenta signos compatibles con rabia")
        return _resultado(3, motivos)

    es_realmente_observable = (
        tiene_dueno == 1
        and ubicacion_animal == 1
    )

    if not es_realmente_observable:
        motivos.append("El animal no puede mantenerse en observacion (sin dueno, perdido o desconocido)")

        if agresion == 2:
            motivos.append("Lesion multiple")
            return _resultado(3, motivos)

        if extension == 2:
            motivos.append("Herida profunda")
            return _resultado(3, motivos)

        if localizacion in ZONAS_ALTO_RIESGO:
            motivos.append("Localizacion en zona de alto riesgo")
            return _resultado(3, motivos)

        motivos.append("Herida superficial en zona de bajo riesgo, pero sin posibilidad de observar al animal")
        return _resultado(2, motivos)

    motivos.append("El animal puede mantenerse en observacion durante 10 dias")

    if vacunado == 1:
        motivos.append("El animal esta vacunado contra la rabia")
    elif vacunado == 3:
        motivos.append("Se desconoce el estado de vacunacion del animal")
    else:
        motivos.append("El animal no esta vacunado")

    if agresion == 2:
        motivos.append("Lesion multiple")
        return _resultado(3, motivos)

    if extension == 2:
        motivos.append("Herida profunda")
        return _resultado(3, motivos)

    if localizacion in ZONAS_ALTO_RIESGO:
        motivos.append("Localizacion en zona de alto riesgo")
        return _resultado(3, motivos)

    if agresion == 1 and extension == 1:
        motivos.append("Agresion unica y herida superficial en zona de bajo riesgo")
        return _resultado(2, motivos)

    motivos.append("No se identificaron criterios de gravedad; se recomienda seguimiento")
    return _resultado(1, motivos)


def _resultado(codigo, motivos):
    return {
        "codigo": codigo,
        "clasificacion": TEXTO_CLASIFICACION[codigo],
        "motivos": motivos
    }
