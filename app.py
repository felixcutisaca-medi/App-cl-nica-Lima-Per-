import streamlit as st

# -------- PDF DESCARGA DIRECTA --------
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
st.set_page_config(page_title="App Clínica Lima", page_icon="🩺", layout="wide")

st.title("🩺 Evaluación Clínica Integral - Lima")
st.markdown("Herramienta de apoyo para emergencia")

# -------------------------------
# GLUCOSA
st.header("Glucosa")
glucosa = st.number_input("Glucosa (mg/dL)", min_value=0.0)

if st.button("Evaluar Glucosa"):
    if glucosa < 70:
        st.error("Hipoglucemia")
    elif glucosa <= 100:
        st.success("Normal")
    elif glucosa <= 125:
        st.warning("Prediabetes")
    else:
        st.error("Diabetes Mellitus")

# -------------------------------
# IMC
st.markdown("---")
st.header("IMC")

col1, col2 = st.columns(2)

with col1:
    peso = st.number_input("Peso (kg)", min_value=0.0)

with col2:
    talla = st.number_input("Talla (m)", min_value=0.0)

if st.button("Calcular IMC"):
    if talla > 0:
        imc = peso / (talla ** 2)
        st.metric("IMC", f"{imc:.2f}")
    else:
        st.error("Ingrese talla válida")

# -------------------------------
# ACIDO BASE
st.markdown("---")
st.header("🧠 Ácido-Base")

col3, col4, col5, col6, col7, col8 = st.columns(6)

with col3:
    ph = st.number_input("pH", value=7.4)

with col4:
    hco3 = st.number_input("HCO3-", value=24.0)

with col5:
    pco2 = st.number_input("PCO2", value=40.0)

with col6:
    na = st.number_input("Na+", value=140.0)

with col7:
    cl = st.number_input("Cl-", value=100.0)

with col8:
    alb = st.number_input("Albúmina (g/dL)", value=4.0)

# -------- BOTÓN PRINCIPAL --------
if st.button("Analizar ácido-base completo"):

    # Cálculos
    ag = na - (cl + hco3)
    ag_corregido = ag + 2.5 * (4 - alb)

    st.metric("Anión Gap", f"{ag:.2f}")
    st.metric("AG corregido", f"{ag_corregido:.2f}")

    # Estado
    if ph < 7.35:
        estado = "Acidemia"
    elif ph > 7.45:
        estado = "Alcalemia"
    else:
        estado = "pH normal"

    # Trastorno
    if hco3 < 22:
        trastorno = "Acidosis metabólica"
    elif hco3 > 26:
        trastorno = "Alcalosis metabólica"
    else:
        trastorno = "No claro"

    st.write(f"Estado: {estado}")
    st.write(f"Trastorno: {trastorno}")

    # -------- REPORTE --------
    reporte = f"""
Paciente con pH {ph}, HCO3- {hco3} mEq/L, PCO2 {pco2} mmHg.
Na {na}, Cl {cl}, Albúmina {alb} g/dL.

Anión Gap: {ag:.2f}
AG corregido: {ag_corregido:.2f}

Estado: {estado}
Trastorno: {trastorno}
"""

    st.text_area("Reporte clínico", reporte, height=250)

    # -------- PDF DESCARGA --------
    pdf_buffer = generar_pdf_buffer(reporte)

    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_buffer,
        file_name="reporte_clinico.pdf",
        mime="application/pdf"
    )

# -------------------------------
st.markdown("---")
st.caption("Uso académico")