# Streamlit app: Formulario de entrega de resultados - ASTROMEDIC

import streamlit as st
import pandas as pd
from datetime import date
import json

st.set_page_config(page_title="Entrega de Hemograma", layout="centered")

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
    input_val = col2.text_input("", key=analito)

    # Validación de rangos numéricos y sombreado
    try:
        val_float = float(input_val)
        if val_float < ref_min or val_float > ref_max:
            col2.markdown(f"<div style='background-color:#ffcc33;padding:4px'>{input_val}</div>", unsafe_allow_html=True)
        else:
            col2.markdown(f"<div style='background-color:#d6f7d6;padding:4px'>{input_val}</div>", unsafe_allow_html=True)
    except:
        pass

    col3.markdown(unidad)
    col4.markdown(f"{ref_min} - {ref_max}")
    resultados.append((analito, input_val, unidad, f"{ref_min} - {ref_max}"))

# Generar sección imprimible en una sola hoja
st.subheader("Generar vista lista para impresión")
if st.button("🖨️ Vista para imprimir o guardar"):
    st.markdown("""
        <script>
            window.print()
        </script>
    """, unsafe_allow_html=True)

    st.markdown("## Resultado de Laboratorio Clínico - ASTROMEDIC")
    st.write(f"**Paciente:** {nombre} | **DNI:** {dni} | **Edad:** {edad} | **Sexo:** {sexo} | **Fecha:** {fecha} | **Médico:** {medico}")
    df_result = pd.DataFrame(resultados, columns=["Análisis", "Resultado", "Unidad", "Rango"])
    df_result["Resultado"] = df_result.apply(lambda row: f"🔶 {row['Resultado']}" if (row['Resultado'].replace('.','',1).isdigit() and (float(row['Resultado']) < float(row['Rango'].split(' - ')[0]) or float(row['Resultado']) > float(row['Rango'].split(' - ')[1]))) else row['Resultado'], axis=1)
    st.markdown(df_result.to_html(index=False, escape=False), unsafe_allow_html=True)

# Guardar historial (local JSON)
historial = st.session_state.get("historial", [])
if st.button("💾 Guardar historial del paciente"):
    entrada = {
        "nombre": nombre,
        "dni": dni,
        "edad": edad,
        "sexo": sexo,
        "medico": medico,
        "fecha": str(fecha),
        "resultados": resultados
    }
    historial.append(entrada)
    st.session_state["historial"] = historial
    st.success("Historial guardado en sesión")

# Mostrar historial si hay
if "historial" in st.session_state:
    st.subheader("Historial del paciente")
    for i, item in enumerate(st.session_state["historial"]):
        with st.expander(f"{item['fecha']} - {item['nombre']}"):
            st.write(f"DNI: {item['dni']} | Edad: {item['edad']} | Sexo: {item['sexo']} | Médico: {item['medico']}")
            df = pd.DataFrame(item["resultados"], columns=["Análisis", "Resultado", "Unidad", "Rango"])
            st.dataframe(df)

# Pie de página
st.markdown("---")
st.markdown("Ubicación: Av. Siempre Viva 123, Lima | Tel: 987-654-321 | contacto@astromedic.pe | Redes: Facebook / Instagram / TikTok")
