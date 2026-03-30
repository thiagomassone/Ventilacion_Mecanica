# 🫁 Monitor de Ventilación Mecánica - Mini TP 1

Este proyecto es un visualizador interactivo de señales de ventilación mecánica desarrollado para la cátedra de **Ventilación Mecánica**. Permite analizar archivos de señales reales (.txt) y simular el monitoreo en tiempo real tal como se vería en un equipo de terapia intensiva.

## 🧪 Señales Analizadas
Las señales procesadas incluyen:

- Flow [L/min]: Ciclos inspiratorios (positivos) y espiratorios (negativos).
- Paw [cmH2O]: Presión medida en la vía aérea.
- Pes [cmH2O]: Presión esofágica (reflejo del esfuerzo del paciente).

## 🚀 Características

* **Carga de Archivos:** Interfaz para subir señales extraídas de equipos de medición (frecuencia de muestreo 256 Hz).
* **Visualización Interactiva:** Gráficos sincronizados de Flujo (Flow), Presión de Vía Aérea (Paw) y Presión Esofágica (Pes) mediante **Plotly**.
* **Modo Simulación:** Visualización dinámica con ventana temporal deslizable y velocidad ajustable.
* **Umbralización Automática:** El modo simulación detecta automáticamente el inicio de la actividad respiratoria (Paw > 2 cmH2O) para evitar periodos de silencio inicial.
* **Diseño Médico:** Interfaz oscura optimizada para la visualización de curvas fisiológicas.

## 🛠️ Instalación y Uso

1. **Clonar el repositorio:**
    ```zsh
    git clone [https://github.com/thiagomassone/Ventilacion_Mecanica.git](https://github.com/thiagomassone/Ventilacion_Mecanica.git)
    cd MiniTP1

2. **Crear y activar el entorno virtual:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate

3. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt

4. **Correr la aplicación:**
    ```bash
    streamlit run app/main.py

Desarrollado por Thiago Massone - 2026.