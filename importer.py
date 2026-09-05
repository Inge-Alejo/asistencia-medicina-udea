import io
import re
import pandas as pd
from datetime import datetime

def parse_attendance_file(file_content: bytes | str, filename: str = "upload.txt") -> pd.DataFrame:
    """
    Parsea de forma robusta archivos generados por dispositivos biométricos / control de acceso.
    Soporta .txt, .csv, .tsv, .dat, .xlsx, con separadores por tabulador, comas, punto y coma o espacios múltiples.
    """
    df = None
    
    # 1. Si es archivo Excel
    if filename.lower().endswith(('.xlsx', '.xls')):
        if isinstance(file_content, bytes):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            df = pd.read_excel(file_content)
    else:
        # Decodificar texto si viene en bytes
        if isinstance(file_content, bytes):
            # Intentar utf-8 primero, luego latin1 / cp1252 común en Windows
            for encoding in ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']:
                try:
                    text = file_content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                text = file_content.decode('latin1', errors='replace')
        else:
            text = str(file_content)
            
        # Detectar el separador analizando las primeras líneas
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            return pd.DataFrame()
            
        first_line = lines[0]
        sep = None
        if '\t' in first_line:
            sep = '\t'
        elif ';' in first_line:
            sep = ';'
        elif ',' in first_line:
            sep = ','
        else:
            # Separador de espacios múltiples o tabulaciones mixtas
            sep = r'\s{2,}|\t'
            
        try:
            if sep in ['\t', ';', ',']:
                df = pd.read_csv(io.StringIO(text), sep=sep, engine='python', skipinitialspace=True)
            else:
                df = pd.read_csv(io.StringIO(text), sep=sep, engine='python')
        except Exception:
            # Fallback con regex flexible
            df = pd.read_csv(io.StringIO(text), sep=r'\s{2,}|\t', engine='python')

    if df is None or df.empty:
        return pd.DataFrame()
        
    # 2. Limpiar nombres de columnas
    df.columns = [str(c).strip() for c in df.columns]
    
    # Eliminar columnas sin nombre o vacías generadas por tabuladores finales
    df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
    df = df.loc[:, df.columns != '']

    # Mapeo de columnas esperadas
    col_mapping = {}
    used_targets = set()
    for col in df.columns:
        col_lower = col.lower().replace('.', '').strip()
        target = None
        if col_lower in ['id', 'id usuario', 'user id', 'codigo', 'matricula', 'no']:
            target = 'student_id'
        elif 'nombre' in col_lower or 'name' in col_lower or 'estudiante' in col_lower or 'alumno' in col_lower:
            target = 'name'
        elif 'depart' in col_lower or 'dept' in col_lower or 'grupo' in col_lower or 'grado' in col_lower or 'curso' in col_lower:
            target = 'department'
        elif 'tiempo' in col_lower or 'time' in col_lower or 'fecha' in col_lower or 'datetime' in col_lower:
            target = 'timestamp'
        elif 'dispositivo' in col_lower or 'device' in col_lower:
            target = 'device_id'

        if target and target not in used_targets:
            col_mapping[col] = target
            used_targets.add(target)

    df = df.rename(columns=col_mapping)
    
    # Validar que tengamos las columnas mínimas indispensables
    required_cols = ['student_id', 'timestamp']
    for req in required_cols:
        if req not in df.columns:
            raise ValueError(f"No se pudo identificar la columna '{req}' en el archivo. Columnas detectadas: {list(df.columns)}")
            
    # Asegurar que cada columna mapeada sea una Serie y no un DataFrame
    for c in ['student_id', 'name', 'department', 'timestamp', 'device_id']:
        if c in df.columns and isinstance(df[c], pd.DataFrame):
            df[c] = df[c].iloc[:, 0]

    # Si no vienen nombre, departamento o dispositivo, rellenar valores por defecto
    if 'name' not in df.columns:
        df['name'] = "Estudiante " + df['student_id'].astype(str)
    if 'department' not in df.columns:
        df['department'] = "General"
    if 'device_id' not in df.columns:
        df['device_id'] = "1"
        
    # 3. Limpiar y normalizar los datos
    # Limpiar student_id
    df['student_id'] = df['student_id'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    df = df[df['student_id'] != '']
    df = df[df['student_id'].str.lower() != 'nan']
    
    # Limpiar nombre
    df['name'] = df['name'].fillna("").astype(str).str.strip()
    df.loc[df['name'] == '', 'name'] = "Estudiante " + df['student_id']
    df.loc[df['name'] == '', 'name'] = "Estudiante " + df['student_id']
    # Capitalización limpia
    df['name'] = df['name'].apply(lambda n: n.title() if n.islower() else n)
    
    # Limpiar departamento
    df['department'] = df['department'].fillna("Sin Asignar").astype(str).str.strip()
    df['department'] = df['department'].replace({'Not Set1': 'General', 'Not Set': 'General', '': 'General'})
    
    # Limpiar timestamps: ej. " 2026-09-02     11:27:44"
    def clean_and_parse_datetime(val):
        if pd.isna(val):
            return None
        val_str = str(val).strip()
        # Reducir múltiples espacios internos a uno solo
        val_str = re.sub(r'\s+', ' ', val_str)
        try:
            # Intento automático de parseo de pandas
            return pd.to_datetime(val_str)
        except Exception:
            for fmt in [
                "%Y-%m-%d %H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%d-%m-%Y %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%d/%m/%Y %H:%M"
            ]:
                try:
                    return pd.to_datetime(datetime.strptime(val_str, fmt))
                except Exception:
                    continue
        return None

    df['timestamp'] = df['timestamp'].apply(clean_and_parse_datetime)
    # Descartar filas con fechas no válidas
    df = df.dropna(subset=['timestamp'])
    
    # 4. Extraer fecha (YYYY-MM-DD) y hora (HH:MM:SS)
    df['date'] = df['timestamp'].dt.strftime('%Y-%m-%d')
    df['time'] = df['timestamp'].dt.strftime('%H:%M:%S')
    df['device_id'] = df['device_id'].astype(str).str.strip()
    
    # 5. Ordenar cronológicamente
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    return df[['student_id', 'name', 'department', 'timestamp', 'date', 'time', 'device_id']]

def get_sample_attendance_text() -> str:
    """Devuelve datos de ejemplo con el formato exacto del usuario y alumnos adicionales."""
    return """ID.\tNombre\tDepart.\tTiempo\tID del dispositivo\t
264\talejo pb\tNot Set1\t 2026-09-02     11:27:44\t1
265\tJAVI G\tNot Set1\t 2026-09-02     11:27:53\t1
267\tMARIO V\tNot Set1\t 2026-09-02     11:29:24\t1
264\talejo pb\tNot Set1\t 2026-09-03     11:25:10\t1
265\tJAVI G\tNot Set1\t 2026-09-03     11:26:05\t1
267\tMARIO V\tNot Set1\t 2026-09-03     11:30:12\t1
268\tSofia Morales\tInformatica\t 2026-09-03     11:22:15\t1
269\tCarlos Ruiz\tDiseno\t 2026-09-03     11:28:40\t1
264\talejo pb\tNot Set1\t 2026-09-04     11:24:50\t1
265\tJAVI G\tNot Set1\t 2026-09-04     11:27:10\t1
267\tMARIO V\tNot Set1\t 2026-09-04     11:31:00\t1
268\tSofia Morales\tInformatica\t 2026-09-04     11:20:00\t1
269\tCarlos Ruiz\tDiseno\t 2026-09-04     11:25:30\t1
270\tValentina Gomez\tInformatica\t 2026-09-04     11:26:18\t1
"""
