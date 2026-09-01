CONDUCTA = {
    1: {
        "resumen": "No se requiere tratamiento antirrabico",
        "pasos": [
            "Lavar la zona de contacto con agua y jabon abundante",
            "No se requiere esquema de vacunacion ni suero antirrabico",
            "Vigilar la zona por signos de infeccion"
        ]
    },
    2: {
        "resumen": "Lavado de la herida + observacion del animal y/o vacunacion",
        "pasos": [
            "Lavar la herida de inmediato con agua y jabon abundante 10-15 minutos",
            "Si el animal es observable: mantenerlo en observacion 10 dias",
            "Si permanece sano, no es necesario continuar el esquema de vacunacion",
            "Si no es observable o desarrolla signos, iniciar/completar vacunacion",
            "Acudir a un centro de salud para valoracion de la herida"
        ]
    },
    3: {
        "resumen": "Lavado + suero antirrabico + esquema completo de vacunacion",
        "pasos": [
            "Lavar la herida de inmediato con agua y jabon abundante 10-15 minutos",
            "Acudir de forma inmediata a un centro de salud",
            "Aplicar suero (inmunoglobulina) antirrabico segun indicacion medica",
            "Iniciar el esquema completo de vacunacion antirrabica",
            "Valorar refuerzo de toxoide tetanico y manejo de la herida"
        ]
    }
}


def obtener_tratamiento(resultado):
    codigo = resultado["codigo"]
    conducta = CONDUCTA[codigo]
    return {
        "clasificacion": resultado["clasificacion"],
        "resumen": conducta["resumen"],
        "pasos": conducta["pasos"],
        "motivos": resultado.get("motivos", [])
    }


def mostrar_tratamiento(resultado):
    info = obtener_tratamiento(resultado)
    print(f"\nClasificacion: {info['clasificacion']}")
    if info["motivos"]:
        print("Motivos:")
        for motivo in info["motivos"]:
            print(f"  - {motivo}")
    print(f"\nConducta recomendada: {info['resumen']}")
    print("Pasos a seguir:")
    for i, paso in enumerate(info["pasos"], start=1):
        print(f"  {i}. {paso}")
