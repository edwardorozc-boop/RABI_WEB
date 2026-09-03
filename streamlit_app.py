import random
import string

import streamlit as st

from flujo import siguiente_paso, ORDEN_MAXIMO
from tratamiento import obtener_tratamiento

st.set_page_config(page_title="RABI · Clasificación de exposición rábica", page_icon="🐾", layout="centered")

TOTAL_PREGUNTAS = len(ORDEN_MAXIMO)

BADGE_POR_NIVEL = {
    1: {"bg": "#E1F5EE", "color": "#0F6E56", "icono": "✓"},
    2: {"bg": "#FAEEDA", "color": "#633806", "icono": "⚠"},
    3: {"bg": "#FCEBEB", "color": "#791F1F", "icono": "⛔"},
}

CATEGORIA_POR_PREGUNTA = {
    "tipo_agresion": "Tipo de exposición",
    "especie": "Animal agresor",
    "estado_animal": "Animal agresor",
    "signos_rabia": "Animal agresor",
    "vacunado": "Seguimiento del animal",
    "tiene_dueno": "Seguimiento del animal",
    "ubicacion_animal": "Seguimiento del animal",
    "localizacion": "Características de la lesión",
    "agresion": "Características de la lesión",
    "extension": "Características de la lesión",
}

LOGO_SVG = """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#E1F5EE"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6z"/>
  <path d="M9 12l2 2 4-4"/>
</svg>
"""

ICONO_CATEGORIA = """
<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#0F6E56"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/>
</svg>
"""

# ---------- CSS: la app entera queda dentro de una tarjeta con sombra ----------
st.markdown(
    """
    <style>
    .block-container{
        max-width: 460px;
        padding: 30px 32px 34px;
        margin-top: 2.5rem;
        background: #FFFFFF;
        border: 1px solid #E4E1D8;
        border-radius: 18px;
        box-shadow: 0 1px 2px rgba(27,43,39,.04), 0 12px 28px -16px rgba(27,43,39,.18);
    }

    div[data-testid="stButton"] button[kind="secondary"]{
        width: 100%;
        text-align: left;
        border: 1.5px solid #E4E1D8;
        color: #1B2B27;
        border-radius: 11px;
        padding: 13px 16px;
        font-size: 14.5px;
        background: #FCFBF8;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover{
        background: #E1F5EE;
        color: #0F6E56;
        border-color: #0F6E56;
    }
    div[data-testid="stButton"] button[kind="primary"]{
        border-radius: 11px;
        padding: 12px 40px;
        font-size: 15px;
        display: block;
        margin: 0 auto;
        width: auto;
    }

    .rabi-cabecera{ display:flex; align-items:center; gap:10px; margin-bottom: 22px; }
    .rabi-cabecera--centrada{ flex-direction:column; justify-content:center; text-align:center; margin-bottom: 24px; }
    .rabi-logo{
        width:36px; height:36px; border-radius:10px; background:#0F6E56;
        display:flex; align-items:center; justify-content:center; flex:none;
    }
    .rabi-titulo{ margin:0; font-size:15px; font-weight:600; color:#1B2B27; }
    .rabi-subtitulo{ margin:0; font-size:11px; color:#6B7A76; }

    .rabi-progreso{ display:flex; align-items:center; gap:10px; margin-bottom:20px; }
    .rabi-progreso .pista{ height:6px; flex:1; background:#EFEEE7; border-radius:3px; overflow:hidden; }
    .rabi-progreso .relleno{ height:100%; background:#0F6E56; border-radius:3px; }
    .rabi-progreso .contador{ font-size:11px; color:#94A29D; white-space:nowrap; }

    .rabi-categoria-fila{ display:flex; align-items:center; gap:8px; margin-bottom:10px; }
    .rabi-categoria{
        font-size:11px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:#0F6E56;
    }
    .rabi-pregunta{ font-size:18px; font-weight:600; color:#1B2B27; margin:0 0 16px; line-height:1.35; }

    .rabi-eyebrow{
        font-size:11px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:#0F6E56;
        margin:0 0 10px; text-align:center;
    }
    .rabi-bienvenida-titulo{ font-size:20px; font-weight:600; color:#1B2B27; margin:0 0 16px; text-align:center; }
    .rabi-bienvenida-texto{ font-size:14.5px; line-height:1.6; color:#6B7A76; margin:0 0 26px; text-align:center; }

    .rabi-badge{
        display:inline-flex; align-items:center; gap:7px;
        padding:6px 14px; border-radius:999px;
        font-size:11px; font-weight:600; letter-spacing:.03em; text-transform:uppercase;
        margin-bottom:16px;
    }
    .rabi-resumen{ font-size:16px; font-weight:600; color:#1B2B27; margin:0 0 20px; line-height:1.4; }
    .rabi-seccion-titulo{
        font-size:11.5px; font-weight:600; text-transform:uppercase; letter-spacing:.03em;
        color:#6B7A76; margin:0 0 10px;
    }
    .rabi-paso{ display:flex; gap:9px; margin-bottom:8px; }
    .rabi-paso .num{
        width:20px; height:20px; border-radius:50%; background:#E1F5EE; color:#0F6E56;
        font-size:10.5px; display:flex; align-items:center; justify-content:center; flex:none;
    }
    .rabi-paso p{ margin:0; font-size:13.5px; color:#1B2B27; line-height:1.5; }
    .rabi-aviso{ font-size:12px; color:#94A29D; line-height:1.5; margin-top:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def nuevo_codigo_caso():
    sufijo = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"RABI-{sufijo}"


def iniciar_estado():
    if "respuestas" not in st.session_state:
        st.session_state.respuestas = {}
    if "historial" not in st.session_state:
        st.session_state.historial = []
    if "codigo_caso" not in st.session_state:
        st.session_state.codigo_caso = nuevo_codigo_caso()
    if "iniciado" not in st.session_state:
        st.session_state.iniciado = False


def reiniciar_caso():
    st.session_state.respuestas = {}
    st.session_state.historial = []
    st.session_state.codigo_caso = nuevo_codigo_caso()
    st.session_state.iniciado = False


def barra_progreso(actual, total):
    pct = min(100, round((actual - 1) / total * 100)) if total else 0
    st.markdown(
        f"""
        <div class="rabi-progreso">
            <div class="pista"><div class="relleno" style="width:{pct}%;"></div></div>
            <span class="contador">{actual} / {total}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


CABECERA_HTML = f"""
<div class="rabi-logo">{LOGO_SVG}</div>
<div>
    <p class="rabi-titulo">RABI</p>
    <p class="rabi-subtitulo">Clasificación de exposición rábica</p>
</div>
"""

iniciar_estado()

# ---------- Barra lateral: caso e historial ----------
with st.sidebar:
    st.markdown(f"**Caso:** `{st.session_state.codigo_caso}`")
    st.markdown("---")
    if st.session_state.historial:
        st.markdown("**Respuestas registradas**")
        for item in st.session_state.historial:
            st.markdown(f"- *{item['etiqueta']}*: **{item['texto']}**")
    else:
        st.caption("Aún no hay respuestas registradas.")

# ---------- Pantalla de bienvenida ----------
if not st.session_state.iniciado:
    st.markdown(f'<div class="rabi-cabecera rabi-cabecera--centrada">{CABECERA_HTML}</div>', unsafe_allow_html=True)
    st.markdown('<p class="rabi-eyebrow">Bienvenido</p>', unsafe_allow_html=True)
    st.markdown('<p class="rabi-bienvenida-titulo">¡Hola! Soy RABI</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="rabi-bienvenida-texto">'
        "Fui creado para ser un apoyo a la hora de clasificar correctamente "
        "el tipo de exposición rábica, siguiendo el algoritmo del Instituto "
        "Nacional de Salud (Colombia). Te voy a hacer 10 preguntas, paso a paso."
        "</p>",
        unsafe_allow_html=True,
    )
    if st.button("Comenzar", type="primary"):
        st.session_state.iniciado = True
        st.rerun()
    st.stop()

# ---------- Cabecera (preguntas y resultado) ----------
st.markdown(f'<div class="rabi-cabecera">{CABECERA_HTML}</div>', unsafe_allow_html=True)

# ---------- Paso actual ----------
paso = siguiente_paso(st.session_state.respuestas)

if paso["tipo"] == "pregunta":
    barra_progreso(paso["paso"], TOTAL_PREGUNTAS)

    categoria = CATEGORIA_POR_PREGUNTA.get(paso["id"], "Pregunta")
    st.markdown(
        f'<div class="rabi-categoria-fila">{ICONO_CATEGORIA}'
        f'<span class="rabi-categoria">{categoria}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="rabi-pregunta">{paso["texto"]}</p>', unsafe_allow_html=True)

    for opcion in paso["opciones"]:
        if st.button(f"○   {opcion['texto']}", key=f"{paso['id']}_{opcion['valor']}"):
            st.session_state.respuestas[paso["id"]] = opcion["valor"]
            st.session_state.historial.append({"etiqueta": paso["texto"], "texto": opcion["texto"]})
            st.rerun()

    if st.session_state.historial:
        if st.button("← Corregir respuesta anterior", key="btn_atras"):
            st.session_state.historial.pop()
            respondidas = [clave for clave in ORDEN_MAXIMO if clave in st.session_state.respuestas]
            if respondidas:
                del st.session_state.respuestas[respondidas[-1]]
            st.rerun()

else:
    resultado = paso["resultado"]
    tratamiento = obtener_tratamiento(resultado)
    nivel = resultado["codigo"]
    estilo = BADGE_POR_NIVEL[nivel]

    barra_progreso(TOTAL_PREGUNTAS + 1, TOTAL_PREGUNTAS)

    st.markdown(
        f'<span class="rabi-badge" style="background:{estilo["bg"]};color:{estilo["color"]};">'
        f'{estilo["icono"]} {resultado["clasificacion"]}</span>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="rabi-resumen">{tratamiento["resumen"]}</p>', unsafe_allow_html=True)

    st.markdown('<p class="rabi-seccion-titulo">Pasos a seguir</p>', unsafe_allow_html=True)
    pasos_html = "".join(
        f'<div class="rabi-paso"><span class="num">{i}</span><p>{p}</p></div>'
        for i, p in enumerate(tratamiento["pasos"], start=1)
    )
    st.markdown(pasos_html, unsafe_allow_html=True)

    if resultado.get("motivos"):
        with st.expander("Motivos de la clasificación"):
            for motivo in resultado["motivos"]:
                st.markdown(f"- {motivo}")

    st.markdown(
        '<p class="rabi-aviso">RABI es una guía de apoyo basada en el algoritmo del INS '
        "y no reemplaza la valoración de un profesional de la salud.</p>",
        unsafe_allow_html=True,
    )

    if st.button("Nuevo caso", type="primary"):
        reiniciar_caso()
        st.rerun()
