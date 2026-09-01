import random
import string

import streamlit as st

from flujo import siguiente_paso, ORDEN_MAXIMO
from tratamiento import obtener_tratamiento

st.set_page_config(page_title="RABI · Clasificación de exposición rábica", page_icon="🐾", layout="centered")

TOTAL_ESTIMADO = 10

BADGE_POR_NIVEL = {
    1: {"bg": "#E1F5EE", "color": "#0F6E56", "icono": "✓"},
    2: {"bg": "#FAEEDA", "color": "#633806", "icono": "⚠"},
    3: {"bg": "#FCEBEB", "color": "#791F1F", "icono": "⛔"},
}

LOGO_SVG = """
<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="#E1F5EE"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6z"/>
  <path d="M9 12l2 2 4-4"/>
</svg>
"""

# ---------- CSS: tarjeta, botones estilo "opcion", tipografia ----------
st.markdown(
    """
    <style>
    .block-container{ max-width: 460px; padding-top: 2.5rem; }

    div[data-testid="stButton"] button[kind="secondary"]{
        width: 100%;
        border: 1.5px solid #0F6E56;
        color: #0F6E56;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 15px;
        background: #FFFFFF;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover{
        background: #E1F5EE;
        color: #0F6E56;
        border-color: #0F6E56;
    }
    div[data-testid="stButton"] button[kind="primary"]{
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 15px;
    }

    .rabi-cabecera{ display:flex; align-items:center; gap:10px; margin-bottom: 6px; }
    .rabi-logo{
        width:34px; height:34px; border-radius:10px; background:#0F6E56;
        display:flex; align-items:center; justify-content:center; flex:none;
    }
    .rabi-titulo{ margin:0; font-size:15px; font-weight:600; color:#1B2B27; }
    .rabi-subtitulo{ margin:0; font-size:11px; color:#6B7A76; }

    .rabi-eyebrow{ font-size:11px; color:#94A29D; margin: 0 0 14px; }
    .rabi-pregunta{ font-size:17px; font-weight:600; color:#1B2B27; margin:0 0 14px; }

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


def reiniciar_caso():
    st.session_state.respuestas = {}
    st.session_state.historial = []
    st.session_state.codigo_caso = nuevo_codigo_caso()


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

# ---------- Cabecera ----------
st.markdown(
    f"""
    <div class="rabi-cabecera">
        <div class="rabi-logo">{LOGO_SVG}</div>
        <div>
            <p class="rabi-titulo">RABI</p>
            <p class="rabi-subtitulo">Clasificación de exposición rábica</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Paso actual ----------
paso = siguiente_paso(st.session_state.respuestas)

if paso["tipo"] == "pregunta":
    progreso = min(1.0, len(st.session_state.respuestas) / (TOTAL_ESTIMADO + 1))
    st.progress(progreso)
    st.markdown(
        f'<p class="rabi-eyebrow">Pregunta {paso["paso"]} de ~{paso["total_estimado"]}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="rabi-pregunta">{paso["texto"]}</p>', unsafe_allow_html=True)

    for opcion in paso["opciones"]:
        if st.button(opcion["texto"], key=f"{paso['id']}_{opcion['valor']}"):
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

    st.progress(1.0)

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
