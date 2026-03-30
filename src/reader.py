import pandas as pd

def load_signal(file_source):

    try:
        df = pd.read_csv(file_source, sep='\t', header=5)
        
        # Limpieza de columnas vacías y espacios
        df = df.dropna(axis=1, how='all')
        df.columns = df.columns.str.strip()
        
        return df
    
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None