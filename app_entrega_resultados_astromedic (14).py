# Streamlit app: Entrega de resultados de laboratorio - Multi análisis

import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import base64

st.set_page_config(page_title="Resultados de Laboratorio ASTROMEDIC", layout="centered")

st.title("RESULTADO DE LABORATORIO CLÍNICO - ASTROMEDIC")

# Datos del paciente
col1, col2, col3 = st.columns(3)
nombre = col1.text_input("Paciente")
dni = col2.text_input("DNI")
edad = col3.number_input("Edad", 0, 120)
sexo = col1.selectbox("Sexo", ["Masculino", "Femenino"])
medico = col2.text_input("Médico")
fecha = col3.date_input("Fecha de entrega", value=date.today())

# Base de datos de análisis
analisis_db = {
    "Hemograma": [
        ("GLOB. BLANCOS", "mm3", "4000", "10000"),
        ("ABASTONADOS", "%", "0", "4"),
        ("SEGMENTADOS", "%", "45", "65"),
        ("EOSINOFILOS", "%", "0", "4"),
        ("BASOFILOS", "%", "0", "1"),
        ("LINFOCITOS", "%", "20", "45"),
        ("MONOCITOS", "%", "0", "4"),
        ("MCV", "fL", "80", "99"),
        ("MCH", "pg", "26", "32"),
        ("MCHC", "g/dL", "32", "36"),
        ("RDW – SD", "fL", "37", "54"),
        ("RDW – CV", "%", "11.5", "14.5"),
        ("PLAQUETAS", "mm3", "150000", "450000")
    ],
    "Glucosa": [
        ("Glucosa en ayunas", "mg/dL", "70", "110"),
        ("Glucosa postprandial", "mg/dL", "<140", "")
    ]
}

# Selección del análisis
opcion = st.selectbox("Selecciona el tipo de análisis", list(analisis_db.keys()))
entradas = []
st.subheader(f"Resultados - {opcion}")

for nombre, unidad, ref_min, ref_max in analisis_db[opcion]:
    c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
    c1.markdown(f"**{nombre}**")
    valor = c2.text_input("", key=nombre)
    c3.markdown(unidad)
    rango = f"{ref_min} - {ref_max}" if ref_max else f"< {ref_min}"
    c4.markdown(rango)
    try:
        v = float(valor)
        if ref_max and float(ref_min) <= v <= float(ref_max):
            estado = "✅"
        elif not ref_max and v < float(ref_min):
            estado = "✅"
        else:
            estado = "🔶"
    except:
        estado = ""
    entradas.append((nombre, valor, unidad, rango, estado))

# Vista previa completa para imprimir
if st.button("🖨️ Vista previa para imprimir"):
    st.markdown("## Resultado de Laboratorio Clínico - ASTROMEDIC")
    st.markdown(f"**Paciente:** {nombre}")
    st.markdown(f"**DNI:** {dni} | **Edad:** {edad} | **Sexo:** {sexo}")
    st.markdown(f"**Médico:** {medico} | **Fecha de entrega:** {fecha}")
    st.markdown("---")
    df = pd.DataFrame(entradas, columns=["Análisis", "Resultado", "Unidad", "Rango", "✔"])
    st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Ubicación:** Av. Siempre Viva 123, Lima  ")
    st.markdown("**Contacto:** contacto@astromedic.pe | Tel: 987-654-321  ")
    st.markdown("**Redes:** Facebook / Instagram / TikTok  ")
    st.info("Presione Ctrl+P o clic derecho → Imprimir para generar PDF")

# Función para generar PDF
def generar_pdf(nombre, dni, edad, sexo, medico, fecha, resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ASTROMEDIC - Resultados de Laboratorio", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Paciente: {nombre}", ln=True)
    pdf.cell(0, 10, f"DNI: {dni}  Edad: {edad}  Sexo: {sexo}", ln=True)
    pdf.cell(0, 10, f"Médico: {medico}", ln=True)
    pdf.cell(0, 10, f"Fecha: {fecha}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Análisis", 1)
    pdf.cell(30, 10, "Resultado", 1)
    pdf.cell(25, 10, "Unidad", 1)
    pdf.cell(50, 10, "Rango", 1)
    pdf.cell(15, 10, "", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 11)
    for r in resultados:
        pdf.cell(60, 10, r[0], 1)
        pdf.cell(30, 10, str(r[1]), 1)
        pdf.cell(25, 10, r[2], 1)
        pdf.cell(50, 10, r[3], 1)
        pdf.cell(15, 10, r[4], 1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Ubicación: Av. Siempre Viva 123, Lima", ln=True)
    pdf.cell(0, 10, "Contacto: contacto@astromedic.pe | Tel: 987-654-321", ln=True)
    pdf.cell(0, 10, "Redes: Facebook / Instagram / TikTok", ln=True)

    return pdf.output(dest="S").encode("utf-8", errors="replace")

# Botón para descargar PDF
if st.button("📥 Descargar PDF"):
    pdf_bytes = generar_pdf(nombre, dni, edad, sexo, medico, fecha, entradas)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="resultado_{nombre}.pdf">Haz clic aquí para descargar el PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
