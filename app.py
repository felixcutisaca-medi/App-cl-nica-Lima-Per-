import streamlit as st
from datetime import date

# -------- PDF --------
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generar_pdf_buffer(texto):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    contenido = []

    for linea in texto.split("\n"):
        contenido.append(Paragraph(linea, styles["Normal"]))

    doc.build(contenido)
    buffer.seek(0)
    return buffer

# -------- CONFIG --------
st.set_page_config(
    page_title="Evaluación Ácido-Base",
    page_icon="",
    layout="wide"
)

# -------- SIDEBAR --------
with st.sidebar:
    st.markdown("## Parámetros normales")
    st.write("pH: 7.35 – 7.45")
    st.write("HCO3-: 22 – 26")
    st.write("PCO2: 35 – 45")
    st.write("AG: 8 – 12")

# -------- ESTILO DARK --------
st.markdown("""
<style>

body {
    background-color: #0e1117;
    color: #e6edf3;
}

.block-container {
    padding-top: 1.5rem;
}

h1 {
    color: #58a6ff;
    font-weight: 700;
}

h2, h3 {
    color: #8b949e;
}

.stNumberInput input, .stTextInput input {
    background-color: #161b22 !important;
    color: white !important;
    border-radius: 8px;
}

.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

[data-testid="metric-container"] {
    background-color: #161b22;
    border-radius: 12px;
    padding: 10px;
}

.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown("""
<h1>MONITOR ÁCIDO-BASE</h1>
<p style='color:#8b949e;'>Sistema clínico de interpretación en tiempo real</p>
""", unsafe_allow_html=True)

# -------------------------------
# DATOS DEL PACIENTE
st.markdown("## Datos del paciente")

colA, colB, colC = st.columns(3)

with colA:
    nombre = st.text_input("Nombre")

with colB:
    edad = st.number_input("Edad", min_value=0)

with colC:
    fecha = st.date_input("Fecha", value=date.today())

# -------------------------------
st.divider()
st.markdown("## Análisis Ácido-Base")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    ph = st.number_input("pH", value=7.4)

with col2:
    hco3 = st.number_input("HCO3-", value=24.0)

with col3:
    pco2 = st.number_input("PCO2", value=40.0)

with col4:
    na = st.number_input("Na+", value=140.0)

with col5:
    cl = st.number_input("Cl-", value=100.0)

with col6:
    alb = st.number_input("Albúmina", value=4.0)

# -------------------------------
if st.button("🔍 Analizar paciente"):

    ag = na - (cl + hco3)
    ag_corregido = ag + 2.5 * (4 - alb)

    if ph < 7.35:
        estado = "Acidemia"
    elif ph > 7.45:
        estado = "Alcalemia"
    else:
        estado = "pH normal"

    if estado == "Acidemia":
        if hco3 < 22:
            trastorno = "Acidosis metabólica"
        elif pco2 > 45:
            trastorno = "Acidosis respiratoria"
        else:
            trastorno = "Mixto o indeterminado"

    elif estado == "Alcalemia":
        if hco3 > 26:
            trastorno = "Alcalosis metabólica"
        elif pco2 < 35:
            trastorno = "Alcalosis respiratoria"
        else:
            trastorno = "Mixto o indeterminado"
    else:
        trastorno = "Posible trastorno mixto"

    # -------- MÉTRICAS --------
    st.markdown("### Resultados")

    colR1, colR2, colR3 = st.columns(3)

    with colR1:
        st.metric("pH", f"{ph:.2f}")

    with colR2:
        st.metric("Anión Gap", f"{ag:.2f}")

    with colR3:
        st.metric("AG corregido", f"{ag_corregido:.2f}")

    st.success(f"Estado: {estado}")
    st.info(f"Trastorno principal: {trastorno}")

    # -------- ESTADO CRÍTICO --------
    st.markdown("### Estado crítico")

    if ph < 7.2:
        st.error("🔴 ACIDEMIA SEVERA")
    elif ph > 7.55:
        st.error("🔴 ALCALOSIS SEVERA")
    else:
        st.success("🟢 Estable")

    # -------- WINTER --------
    st.markdown("### Compensación (Winter)")

    if "Acidosis metabólica" in trastorno:
        pco2_esperado = 1.5 * hco3 + 8
        st.write(f"PCO2 esperado: {pco2_esperado:.2f} ±2")

        if abs(pco2 - pco2_esperado) <= 2:
            st.success("Compensación adecuada")
        else:
            st.warning("Trastorno mixto")

    # -------- DELTA GAP --------
    st.markdown("### Delta Gap")

    if ag_corregido > 12:
        delta_ag = ag_corregido - 12
        delta_hco3 = 24 - hco3
        relacion = delta_ag / delta_hco3 if delta_hco3 != 0 else 0

        st.write(f"Relación Δ/Δ: {relacion:.2f}")

        if relacion < 0.8:
            st.warning("Acidosis mixta")
        elif 0.8 <= relacion <= 2:
            st.success("Acidosis pura")
        else:
            st.warning("Alcalosis asociada")

    # -------- DIAGNÓSTICO --------
    if "Acidosis metabólica" in trastorno:
        if ag_corregido > 12:
            diagnostico = "Acidosis metabólica con anión gap elevado"
        else:
            diagnostico = "Acidosis metabólica hiperclorémica"

    elif "Alcalosis metabólica" in trastorno:
        diagnostico = "Alcalosis metabólica"

    elif "respiratoria" in trastorno:
        diagnostico = "Trastorno respiratorio"

    else:
        diagnostico = "Trastorno mixto"

    st.warning(diagnostico)

    # -------- REPORTE --------
    reporte = f"""
Paciente: {nombre}
Edad: {edad}
Fecha: {fecha}

pH: {ph}
HCO3: {hco3}
PCO2: {pco2}

AG: {ag:.2f}
AG corregido: {ag_corregido:.2f}

Estado: {estado}
Trastorno: {trastorno}

Diagnóstico: {diagnostico}
"""

    st.text_area("Reporte", reporte, height=250)

    pdf_buffer = generar_pdf_buffer(reporte)

    st.download_button(
        label="Descargar PDF",
        data=pdf_buffer,
        file_name="reporte.pdf",
        mime="application/pdf"
    )

# -------------------------------
st.caption("Uso clínico orientativo")
