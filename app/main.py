import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import time
import numpy as np

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from src.reader import load_signal

st.set_page_config(page_title="MiniTP 1", layout="wide")
st.title("🫁 Monitor de Ventilación Mecánica")

uploaded_file = st.sidebar.file_uploader("Cargar archivo de señales (.txt)", type=["txt"])
st.sidebar.divider()
st.sidebar.subheader("🎥 Modo Simulación")
modo_vivo = st.sidebar.checkbox("Activar vista en tiempo real")
velocidad = st.sidebar.slider("Velocidad de barrido", 0.1, 2.0, 0.3)
ventana_tiempo = st.sidebar.slider("Ventana de tiempo visible (seg)", 10, 60, 20)


if uploaded_file is not None:

    df = load_signal(uploaded_file)
    st.toast(f"Archivo '{uploaded_file.name}' cargado", icon='✅')

    if df is not None:
        if not modo_vivo:
    
            fig = make_subplots(
                rows=3, cols=1, 
                shared_xaxes=True, 
                vertical_spacing=0.07,
                subplot_titles=("Flujo [L/min]", "Paw [cmH2O]", "Pes [cmH2O]")
            )

            fig.add_trace(go.Scatter(x=df['Time'], y=df['Flow'], name="Flujo", line=dict(color='#00d1ff')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Time'], y=df['Paw'], name="Paw", line=dict(color='#ffea00')), row=2, col=1)
            fig.add_trace(go.Scatter(x=df['Time'], y=df['Pes'], name="Pes", line=dict(color='#ff00ff')), row=3, col=1)

            fig.update_layout(height=800, template="plotly_dark", showlegend=False)
            fig.update_xaxes(showticklabels=True, row=1, col=1)
            fig.update_xaxes(showticklabels=True, row=2, col=1)
            fig.update_xaxes(showticklabels=True, row=3, col=1)

            fig.update_xaxes(title_text="Tiempo [s]", row=3, col=1)

            st.plotly_chart(fig, use_container_width=True)
        
        else:
            # --- MODO SIMULACIÓN EN VIVO ---
            umbral_paw = 2.0
            umbral_flow = 5.0
            
            # Buscamos dónde hay señal significativa
            actividad = df[(df['Paw'].abs() > umbral_paw) | (df['Flow'].abs() > umbral_flow)]
            
            if not actividad.empty:
                # Empezamos 2 segundos antes del primer signo de vida para dar contexto
                tiempo_inicio_real = max(df['Time'].min(), actividad['Time'].iloc[0] - 2)
            else:
                tiempo_inicio_real = df['Time'].min()

            placeholder_gráfico = st.empty() 
            
            tiempo_max = int(df['Time'].max())
            pasos_tiempo = np.arange(tiempo_inicio_real, tiempo_max, 0.2)
            
            for t_actual in pasos_tiempo:
                t_inicio = max(tiempo_inicio_real, t_actual - ventana_tiempo)
                mask = (df['Time'] >= t_inicio) & (df['Time'] <= t_actual)
                df_ventana = df[mask]
                
                fig_vivo = make_subplots(
                    rows=3, cols=1, 
                    shared_xaxes=True,
                    vertical_spacing=0.07,
                    subplot_titles=("Flujo [L/min]", "Paw [cmH2O]", "Pes [cmH2O]")
                )

                fig_vivo.add_trace(go.Scatter(x=df_ventana['Time'], y=df_ventana['Flow'], name="Flow", line=dict(color='#00d1ff')), row=1, col=1)
                fig_vivo.add_trace(go.Scatter(x=df_ventana['Time'], y=df_ventana['Paw'], name="Paw", line=dict(color='#ffea00')), row=2, col=1)
                fig_vivo.add_trace(go.Scatter(x=df_ventana['Time'], y=df_ventana['Pes'], name="Pes", line=dict(color='#ff00ff')), row=3, col=1)
                
                fig_vivo.update_xaxes(showticklabels=True, row=1, col=1)
                fig_vivo.update_xaxes(showticklabels=True, row=2, col=1)
                fig_vivo.update_xaxes(showticklabels=True, row=3, col=1)
                
                fig_vivo.update_xaxes(range=[t_inicio, t_actual], title_text="Tiempo [s]", row=3, col=1)
                
                fig_vivo.update_yaxes(range=[df['Flow'].min()*1.1, df['Flow'].max()*1.1], row=1, col=1)
                fig_vivo.update_yaxes(range=[0, df['Paw'].max()*1.1], row=2, col=1)

                # Mantenemos el estilo oscuro y el título general
                fig_vivo.update_layout(
                    height=800, 
                    template="plotly_dark", 
                    showlegend=False, 
                    # Aquí inyectamos el tiempo actual en el título
                    title=f"⏱️ Tiempo de Simulación: {t_actual} s | Archivo: {uploaded_file.name}",
                    title_font_size=20,
                    title_x=0.5
                    )       
                
                placeholder_gráfico.plotly_chart(fig_vivo, use_container_width=True)
                
                time.sleep(velocidad / 5)