# Streamlit app: Entrega de resultados de laboratorio - Multi análisis

import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Resultados de Laboratorio ASTROMEDIC", layout="centered")

st.title("RESULTADO DE LABORATORIO CLÍNICO - ASTROMEDIC")

# Datos del paciente
with st.expander("🧾 Datos del paciente"):
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

# Botón Streamlit nativo para impresión por navegador manual
if st.button("🖨️ Vista previa para imprimir"):
    st.markdown("""
    <script>
    window.addEventListener('afterprint', function(){alert('Impresión completada');});
    window.print();
    </script>
    """, unsafe_allow_html=True)
    st.markdown("## Resultado de Laboratorio Clínico - ASTROMEDIC")
    st.markdown(f"**Paciente:** {nombre} | **DNI:** {dni} | **Edad:** {edad} | **Sexo:** {sexo} | **Fecha:** {fecha} | **Médico:** {medico}")
    df = pd.DataFrame(entradas, columns=["Análisis", "Resultado", "Unidad", "Rango", "✔"])
    st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

# Pie de página
st.markdown("---")
st.markdown("Ubicación: Av. Siempre Viva 123, Lima | Tel: 987-654-321 | contacto@astromedic.pe | Redes: Facebook / Instagram / TikTok")
