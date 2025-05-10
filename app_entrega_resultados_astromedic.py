# Streamlit app: Formulario de entrega de resultados - ASTROMEDIC

import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image

# Cargar logo
top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
with top_col2:
    logo = Image.open("Mesa de trabajo - logo astromedic laboratorio 1.png")
    st.image(logo, width=200)
    st.markdown("""<h3 style='text-align: center; color: #004080;'>RESULTADO DE LABORATORIO CLÍNICO</h3>""", unsafe_allow_html=True)

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

# Datos del hemograma
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

# Sello del licenciado y laboratorio en una línea
st.markdown("
**____________________**                     **____________________**")
st.markdown("Sello del Licenciado                           Sello del Laboratorio")

# Pie de página en una sola línea
st.markdown("---")
st.markdown("Ubicación: Av. Siempre Viva 123, Lima | Tel: 987-654-321 | contacto@astromedic.pe | Redes: Facebook / Instagram / TikTok")

# Botón final (placeholder)
st.success("Formulario listo. Puedes generar el PDF desde la app.")
