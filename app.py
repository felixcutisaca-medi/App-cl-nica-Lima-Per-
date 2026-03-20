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
st.set_page_config(page_title="Sistema Ácido-Base", page_icon="🩺", layout="wide")

# -------- ESTILO --------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #0b3c5d;
}
</style>
""", unsafe_allow_html=True)

# -------- TITULO --------
st.title("EVALUACIÓN ÁCIDO-BASE")
st.caption("Herramienta clínica para apoyo en emergencia")

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
# ÁCIDO BASE
st.markdown("---")
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

    # -------- CÁLCULOS --------
    ag = na - (cl + hco3)
    ag_corregido = ag + 2.5 * (4 - alb)

    # -------- ESTADO --------
    if ph < 7.35:
        estado = "Acidemia"
    elif ph > 7.45:
        estado = "Alcalemia"
    else:
        estado = "pH normal"

    # -------- TRASTORNO --------
    if hco3 < 22:
        trastorno = "Acidosis metabólica"
    elif hco3 > 26:
        trastorno = "Alcalosis metabólica"
    else:
        trastorno = "No claro"

    # -------- RESULTADOS --------
    st.markdown("### 📊 Resultados")

    colR1, colR2 = st.columns(2)

    with colR1:
        st.metric("Anión Gap", f"{ag:.2f}")

    with colR2:
        st.metric("AG corregido", f"{ag_corregido:.2f}")

    st.success(f"Estado: {estado}")
    st.info(f"Trastorno principal: {trastorno}")

    # -------- DIAGNÓSTICO --------
    diagnostico = ""

    if estado == "Acidemia" and "Acidosis metabólica" in trastorno:
        if ag_corregido > 12:
            diagnostico = "Acidosis metabólica con anión gap elevado, probable cetoacidosis diabética o acidosis láctica."
        else:
            diagnostico = "Acidosis metabólica hiperclorémica, probable diarrea o acidosis tubular renal."

    elif estado == "Alcalemia":
        diagnostico = "Alcalosis metabólica, considerar vómitos o diuréticos."

    elif estado == "pH normal":
        diagnostico = "pH normal con posible trastorno mixto."

    st.warning(f"🧠 {diagnostico}")

    # -------- ALERTAS --------
    st.markdown("### 🚨 Alertas clínicas")

    if ph < 7.2:
        st.error("Acidemia severa → riesgo vital")
    elif ph > 7.55:
        st.error("Alcalemia severa → riesgo de arritmias")
    elif ag_corregido > 20:
        st.warning("Anión gap muy elevado → considerar UCI")

    # -------- TRASTORNOS MIXTOS --------
    st.markdown("### 🔬 Trastornos mixtos")

    if hco3 < 22:
        pco2_esperado = 1.5 * hco3 + 8

        if abs(pco2 - pco2_esperado) > 2:
            st.warning("Posible trastorno mixto (compensación inadecuada)")
        else:
            st.success("Compensación adecuada")

    # -------- INTERPRETACIÓN --------
    st.markdown("### 📘 Interpretación clínica")

    interpretacion = ""

    if ag_corregido > 12 and hco3 < 22:
        interpretacion = "Acidosis metabólica con anión gap elevado: pensar en cetoacidosis, acidosis láctica, insuficiencia renal o tóxicos."
    elif ag_corregido <= 12 and hco3 < 22:
        interpretacion = "Acidosis metabólica hiperclorémica: probable diarrea o acidosis tubular renal."
    elif hco3 > 26:
        interpretacion = "Alcalosis metabólica: considerar vómitos, diuréticos o hiperaldosteronismo."

    st.info(interpretacion)

    # -------- REPORTE --------
    st.markdown("### 📄 Reporte clínico")

    reporte = f"""
Paciente: {nombre}
Edad: {edad} años
Fecha: {fecha}

pH: {ph}
HCO3-: {hco3}
PCO2: {pco2}
Na: {na}
Cl: {cl}
Albúmina: {alb}

Anión Gap: {ag:.2f}
AG corregido: {ag_corregido:.2f}

Estado ácido-base: {estado}
Trastorno principal: {trastorno}

Diagnóstico probable:
{diagnostico}

Interpretación:
{interpretacion}
"""

    st.text_area("Reporte listo para copiar", reporte, height=300)

    # -------- PDF --------
    pdf_buffer = generar_pdf_buffer(reporte)

    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_buffer,
        file_name="reporte_clinico.pdf",
        mime="application/pdf"
    )

# -------------------------------
st.markdown("---")
st.caption("⚠️ Uso clínico orientativo")
