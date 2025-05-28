# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:06:25 2025

@author: jahop
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Título principal
st.title("Sistema Inteligente para Gestión de Quejas Hospitalarias")
st.subheader("Portafolio de Javier Horacio Pérez Ricárdez")

# Sidebar con filtros y descarga de CV
st.sidebar.title("Filtros")
area_filtro = st.sidebar.selectbox("Selecciona el área", options=['Todas', 'Urgencias', 'Consulta Externa', 'Laboratorio', 'Farmacia', 'Imagenología'])
gravedad_filtro = st.sidebar.selectbox("Nivel de gravedad", options=['Todas', 'Alta', 'Media', 'Baja'])

with open("CV_Javier_Perez.pdf", "rb") as file:
    st.sidebar.download_button(
        label="Descargar CV",
        data=file,
        file_name="CV_Javier HPR.pdf",
        mime="application/pdf"
    )

# Generar datos simulados de quejas
np.random.seed(42)
areas = ['Urgencias', 'Consulta Externa', 'Laboratorio', 'Farmacia', 'Imagenología']
tipos = ['Trato inadecuado', 'Tiempos de espera', 'Falta de insumos', 'Errores administrativos']
fechas = pd.date_range(start='2024-01-01', periods=100, freq='D')

data = {
    'Fecha': np.random.choice(fechas, 100),
    'Área': np.random.choice(areas, 100),
    'Tipo de Queja': np.random.choice(tipos, 100),
    'Nivel de Gravedad': np.random.choice(['Alta', 'Media', 'Baja'], 100)
}
df_quejas = pd.DataFrame(data)

# Filtro
filtro = df_quejas.copy()
if area_filtro != 'Todas':
    filtro = filtro[filtro['Área'] == area_filtro]
if gravedad_filtro != 'Todas':
    filtro = filtro[filtro['Nivel de Gravedad'] == gravedad_filtro]

# Indicadores Clave
st.markdown("### Indicadores Clave de Desempeño (KPIs)")
st.metric("Total de Quejas", len(filtro))
st.metric("% Quejas Críticas (Alta)", f"{(filtro['Nivel de Gravedad'] == 'Alta').mean()*100:.1f}%")
st.metric("Área con más quejas", filtro['Área'].mode()[0] if not filtro.empty else "N/A")

# Mostrar tabla
st.markdown("### Tabla de Quejas Registradas")
st.dataframe(filtro)

# Análisis gráfico
st.markdown("### Análisis de Tendencias")
grafico = filtro.groupby([filtro['Fecha'].dt.to_period('M').astype(str), 'Área']).size().reset_index(name='Cantidad')
fig = px.bar(grafico, x='Fecha', y='Cantidad', color='Área', barmode='group', title='Tendencia mensual de quejas por área')
st.plotly_chart(fig)

# Recomendaciones dinámicas (simples)
st.markdown("### Recomendaciones Estratégicas")
recomendaciones = []
if 'Urgencias' in filtro['Área'].values:
    recomendaciones.append("Implementar un sistema de triaje más eficiente en Urgencias debido al volumen de quejas.")
if 'Trato inadecuado' in filtro['Tipo de Queja'].values:
    recomendaciones.append("Capacitar al personal en trato digno y comunicación con pacientes.")
if 'Falta de insumos' in filtro['Tipo de Queja'].values:
    recomendaciones.append("Revisar los protocolos de suministro en farmacia y laboratorio.")

if recomendaciones:
    for r in recomendaciones:
        st.write("- ", r)
else:
    st.write("No se encontraron recomendaciones relevantes con los filtros seleccionados.")

# Simulador de solución de quejas
st.markdown("### Simulador de Solución de Quejas")
quejas_resueltas = st.slider("Simula cuántas quejas se han resuelto", 0, len(filtro), step=1)
if quejas_resueltas > 0:
    nuevo_total = len(filtro) - quejas_resueltas
    st.success(f"Al resolver {quejas_resueltas} quejas, el total restante sería: {nuevo_total}")
else:
    st.info("Desliza para simular la solución de quejas.")

# Sección de contacto
st.markdown("### Contacto")
st.markdown("Si desea conocer más sobre esta propuesta o ponerse en contacto, puede escribirme a:")
st.markdown("**Correo:** jahoperi@gmail.com")
st.markdown("**Teléfono:** +52 56 1056 4095")
