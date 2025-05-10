
# Streamlit app: Formulario de entrega de resultados - ASTROMEDIC

import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image
from fpdf import FPDF
import base64
from io import BytesIO

# Cargar logo
top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
with top_col2:
    logo = Image.open("Mesa de trabajo - logo astromedic laboratorio 1.png")
    st.image(logo, width=200)
    st.markdown("<h3 style='text-align: center; color: #004080;'>RESULTADO DE LABORATORIO CLÍNICO</h3>", unsafe_allow_html=True)

# Datos del paciente
st.subheader("Datos del paciente")
col1, col2, col3 = st.columns(3)
nombre = col1.text_input("Nombres y Apellidos")
dni = col2.text_input("DNI")
edad = col3.number_input("Edad", min_value=0, max_value=120, step=1)
sexo = col1.selectbox("Sexo", ["Masculino", "Femenino"])
medico = col2.text_input("Médico tratante")
fecha = col3.date_input("Fecha", value=date.today())

# Valores referenciales según edad y sexo
def get_referencia(nombre, edad, sexo):
    ref_map = {
        "Glóbulos blancos": ("mm³", 4000, 10000),
        "Abastonados": ("%", 0, 4),
        "Segmentados": ("%", 45, 65),
        "Eosinófilos": ("%", 0, 4),
        "Basófilos": ("%", 0, 1),
        "Linfocitos": ("%", 20, 45),
        "Monocitos": ("%", 0, 4),
        "Eritrocitos": {
            "Masculino": ("mill/mm³", 4000000, 5500000),
            "Femenino": ("mill/mm³", 3500000, 5000000),
            "Niño": ("mill/mm³", 4100000, 5100000),
            "RN": ("mill/mm³", 5000000, 6000000)
        },
        "Hemoglobina": {
            "Masculino": ("g/dL", 14, 17),
            "Femenino": ("g/dL", 12, 16),
            "Niño": ("g/dL", 11.2, 16),
            "RN": ("g/dL", 16, 23),
            "2-11m": ("g/dL", 9, 14)
        },
        "Hematocrito": {
            "Masculino": ("%", 42, 52),
            "Femenino": ("%", 36, 46),
            "Niño": ("%", 35, 49),
            "RN": ("%", 50, 62)
        },
        "MCV": ("fL", 80, 99),
        "MCH": ("pg", 26, 32),
        "MCHC": ("g/dL", 32, 36),
        "RDW – SD": ("fL", 37, 54),
        "RDW – CV": ("%", 11.5, 14.5),
        "Plaquetas": ("mil/mm³", 150000, 450000)
    }

    if nombre in ["Eritrocitos", "Hemoglobina", "Hematocrito"]:
        if edad < 1:
            key = "RN"
        elif edad < 2:
            key = "2-11m"
        elif edad <= 12:
            key = "Niño"
        else:
            key = sexo
        unidad, min_val, max_val = ref_map[nombre][key]
    else:
        unidad, min_val, max_val = ref_map[nombre]
    return unidad, min_val, max_val

# Hemograma
st.subheader("Hemograma")
analitos = [
    "Glóbulos blancos", "Abastonados", "Segmentados", "Eosinófilos", "Basófilos",
    "Linfocitos", "Monocitos", "Eritrocitos", "Hemoglobina", "Hematocrito",
    "MCV", "MCH", "MCHC", "RDW – SD", "RDW – CV", "Plaquetas"
]

resultados = []
for analito in analitos:
    unidad, ref_min, ref_max = get_referencia(analito, edad, sexo)
    col1, col2, col3, col4 = st.columns([2, 2, 1, 3])
    col1.markdown(f"**{analito}**")
    resultado = col2.text_input("", key=analito)
    col3.markdown(unidad)
    col4.markdown(f"{ref_min} - {ref_max}")
    resultados.append((analito, resultado, unidad, f"{ref_min} - {ref_max}"))

# Exportar PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, "RESULTADO DE LABORATORIO CLÍNICO - ASTROMEDIC", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", size=8)
        self.multi_cell(0, 5, "Ubicación: Av. Siempre Viva 123, Lima | Tel: 987-654-321 | contacto@astromedic.pe | Redes: Facebook / Instagram / TikTok", align="C")

    def add_info(self):
        self.set_font("Arial", size=10)
        self.cell(0, 10, f"Paciente: {nombre}    DNI: {dni}    Edad: {edad}    Sexo: {sexo}", ln=True)
        self.cell(0, 10, f"Médico: {medico}    Fecha: {fecha}", ln=True)
        self.ln(5)

    def add_table(self):
        self.set_font("Arial", 'B', 10)
        self.cell(50, 8, "Análisis", 1)
        self.cell(30, 8, "Resultado", 1)
        self.cell(30, 8, "Unidad", 1)
        self.cell(60, 8, "Valores Normales", 1, ln=True)
        self.set_font("Arial", size=10)
        for a, r, u, v in resultados:
            self.cell(50, 8, a, 1)
            self.cell(30, 8, r, 1)
            self.cell(30, 8, u, 1)
            self.cell(60, 8, v, 1, ln=True)
        self.ln(10)
        self.cell(0, 10, "____________________                        ____________________", ln=True)
        self.cell(0, 5, "Sello del Licenciado                                 Sello del Laboratorio", ln=True)

if st.button("Generar PDF"):
    pdf = PDF()
    pdf.add_page()
    pdf.add_info()
    pdf.add_table()
    buffer = BytesIO()
    pdf.output(buffer)
    st.download_button(
        label="Descargar PDF",
        data=buffer.getvalue(),
        file_name="resultado_astromedic.pdf",
        mime="application/pdf"
    )
