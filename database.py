import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
import os

DB_PATH = Path(__file__).parent / "attendance.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Inicializa las tablas necesarias en la base de datos SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla de estudiantes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT DEFAULT 'Sin Asignar',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Tabla de registros de asistencia (con restricción única por estudiante y timestamp)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        device_id TEXT DEFAULT '1',
        batch_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(student_id, timestamp),
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );
    """)
    
    # Tabla de lotes de importación
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS import_batches (
        batch_id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_rows INTEGER,
        new_records INTEGER,
        status TEXT DEFAULT 'OK'
    );
    """)
    
    # Tabla de configuración
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)
    
    # Configuración por defecto de admin si no existe (clave compleja)
    default_secure_pwd = "MedUdeA#2026$Semillero!Salud"
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('admin_password', ?)", (default_secure_pwd,))
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('institution_name', 'Semillero Medicina UdeA - Nivel 1')")
    
    # Índices para consultas de alta velocidad
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_student ON attendance_logs(student_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_date ON attendance_logs(date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON attendance_logs(timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_name ON students(name);")
    
    conn.commit()
    conn.close()

def get_admin_password() -> str:
    """Obtiene la contraseña administrativa desde Streamlit Secrets, variables de entorno o BD."""
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and "ADMIN_PASSWORD" in st.secrets:
            return str(st.secrets["ADMIN_PASSWORD"])
    except Exception:
        pass
        
    env_pwd = os.environ.get("ADMIN_PASSWORD")
    if env_pwd:
        return env_pwd
        
    return get_setting("admin_password", "MedUdeA#2026$Semillero!Salud")

def save_logs_batch(df_clean: pd.DataFrame, filename: str) -> dict:
    """
    Inserta o actualiza estudiantes y guarda las marcaciones sin duplicados.
    Retorna un diccionario con estadísticas de inserción.
    """
    if df_clean.empty:
        return {"total_rows": 0, "new_records": 0, "skipped_duplicates": 0, "batch_id": None}
    
    batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Upsert estudiantes
        unique_students = df_clean[['student_id', 'name', 'department']].drop_duplicates(subset=['student_id'])
        for _, row in unique_students.iterrows():
            cursor.execute("""
            INSERT INTO students (student_id, name, department, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(student_id) DO UPDATE SET
                name = COALESCE(NULLIF(excluded.name, ''), students.name),
                department = CASE 
                    WHEN excluded.department != 'Sin Asignar' AND excluded.department != 'Not Set1' THEN excluded.department 
                    ELSE students.department 
                END,
                updated_at = CURRENT_TIMESTAMP
            """, (str(row['student_id']), str(row['name']), str(row['department'])))
        
        # 2. Insertar registros con INSERT OR IGNORE para no duplicar
        new_records_count = 0
        for _, row in df_clean.iterrows():
            ts_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            date_str = row['date']
            time_str = row['time']
            device_id = str(row.get('device_id', '1'))
            
            cursor.execute("""
            INSERT OR IGNORE INTO attendance_logs (student_id, timestamp, date, time, device_id, batch_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (str(row['student_id']), ts_str, date_str, time_str, device_id, batch_id))
            if cursor.rowcount > 0:
                new_records_count += 1
        
        total_rows = len(df_clean)
        skipped = total_rows - new_records_count
        
        # 3. Registrar el lote
        cursor.execute("""
        INSERT INTO import_batches (batch_id, filename, total_rows, new_records)
        VALUES (?, ?, ?, ?)
        """, (batch_id, filename, total_rows, new_records_count))
        
        conn.commit()
        return {
            "total_rows": total_rows,
            "new_records": new_records_count,
            "skipped_duplicates": skipped,
            "batch_id": batch_id
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def search_students_by_query(query: str, limit: int = 10) -> list:
    """Busca estudiantes que coincidan con ID o Nombre."""
    if not query or not query.strip():
        return []
    
    q = f"%{query.strip().lower()}%"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT student_id, name, department 
    FROM students
    WHERE LOWER(student_id) LIKE ? OR LOWER(name) LIKE ?
    ORDER BY name ASC
    LIMIT ?
    """, (q, q, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"student_id": r[0], "name": r[1], "department": r[2]} for r in rows]

def get_student_by_id(student_id: str) -> dict | None:
    """Obtiene datos de un estudiante por su ID exacto."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, department, created_at FROM students WHERE student_id = ?", (str(student_id),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"student_id": row[0], "name": row[1], "department": row[2], "created_at": row[3]}
    return None

def get_student_attendance(student_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """Devuelve las marcaciones de un estudiante ordenadas de más reciente a más antigua."""
    conn = get_connection()
    sql = "SELECT date, time, timestamp, device_id FROM attendance_logs WHERE student_id = ?"
    params = [str(student_id)]
    
    if start_date:
        sql += " AND date >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND date <= ?"
        params.append(end_date)
        
    sql += " ORDER BY timestamp DESC"
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

def get_overall_kpis() -> dict:
    """Métricas globales del sistema para el panel de administración."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM attendance_logs")
    total_logs = cursor.fetchone()[0]
    
    # Marcaciones del día de hoy (fecha actual)
    today_str = datetime.now().strftime("%Y-%m-%d")
    current_month_prefix = datetime.now().strftime("%Y-%m")
    
    cursor.execute("SELECT COUNT(DISTINCT student_id) FROM attendance_logs WHERE date = ?", (today_str,))
    students_today = cursor.fetchone()[0]
    
    # Marcaciones y estudiantes únicos del mes completo actual
    cursor.execute("SELECT COUNT(DISTINCT student_id), COUNT(*) FROM attendance_logs WHERE strftime('%Y-%m', date) = ?", (current_month_prefix,))
    row_month = cursor.fetchone()
    students_this_month = row_month[0] if row_month else 0
    logs_this_month = row_month[1] if row_month else 0
    
    # Última fecha registrada en la base de datos
    cursor.execute("SELECT MAX(date) FROM attendance_logs")
    last_record_date = cursor.fetchone()[0] or today_str
    
    # Estudiantes presentes en la fecha más reciente con datos
    cursor.execute("SELECT COUNT(DISTINCT student_id) FROM attendance_logs WHERE date = ?", (last_record_date,))
    students_last_day = cursor.fetchone()[0]
    
    # Total de lotes cargados
    cursor.execute("SELECT COUNT(*) FROM import_batches")
    total_batches = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_students": total_students,
        "total_logs": total_logs,
        "students_today": students_today,
        "current_month_prefix": current_month_prefix,
        "students_this_month": students_this_month,
        "logs_this_month": logs_this_month,
        "last_record_date": last_record_date,
        "students_last_day": students_last_day,
        "total_batches": total_batches
    }

def get_all_attendance_filtered(start_date: str = None, end_date: str = None, department: str = None, search: str = None) -> pd.DataFrame:
    """Devuelve tabla maestra completa para el panel administrativo con filtros."""
    conn = get_connection()
    sql = """
    SELECT 
        l.date as Fecha,
        l.time as Hora,
        s.student_id as "ID Estudiante",
        s.name as Nombre,
        s.department as "Departamento / Grado",
        l.device_id as "ID Dispositivo",
        l.timestamp as Timestamp
    FROM attendance_logs l
    JOIN students s ON l.student_id = s.student_id
    WHERE 1=1
    """
    params = []
    
    if start_date:
        sql += " AND l.date >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND l.date <= ?"
        params.append(end_date)
    if department and department != "Todos":
        sql += " AND s.department = ?"
        params.append(department)
    if search and search.strip():
        sql += " AND (LOWER(s.name) LIKE ? OR LOWER(s.student_id) LIKE ?)"
        q = f"%{search.strip().lower()}%"
        params.extend([q, q])
        
    sql += " ORDER BY l.timestamp DESC"
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

def get_all_students_df() -> pd.DataFrame:
    """Devuelve listado de todos los estudiantes con estadísticas resumidas."""
    conn = get_connection()
    sql = """
    SELECT 
        s.student_id as "ID",
        s.name as "Nombre",
        s.department as "Departamento / Grado",
        COUNT(l.id) as "Total Asistencias",
        MAX(l.timestamp) as "Última Marcación"
    FROM students s
    LEFT JOIN attendance_logs l ON s.student_id = l.student_id
    GROUP BY s.student_id
    ORDER BY s.name ASC
    """
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def get_distinct_departments() -> list:
    """Obtiene la lista de departamentos existentes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM students WHERE department IS NOT NULL AND department != '' ORDER BY department ASC")
    rows = cursor.fetchall()
    conn.close()
    deps = [r[0] for r in rows if r[0]]
    return ["Todos"] + deps

def get_hourly_distribution() -> pd.DataFrame:
    """Distribución de marcajes por hora del día."""
    conn = get_connection()
    sql = """
    SELECT 
        CAST(SUBSTR(time, 1, 2) AS INTEGER) as hora,
        COUNT(*) as total
    FROM attendance_logs
    GROUP BY hora
    ORDER BY hora ASC
    """
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def get_daily_trend(days: int = 30) -> pd.DataFrame:
    """Tendencia diaria de asistencia en los últimos N días registrados."""
    conn = get_connection()
    sql = """
    SELECT 
        date as Fecha,
        COUNT(DISTINCT student_id) as "Estudiantes Únicos",
        COUNT(*) as "Total Marcaciones"
    FROM attendance_logs
    GROUP BY date
    ORDER BY date ASC
    LIMIT ?
    """
    df = pd.read_sql_query(sql, conn, params=[days])
    conn.close()
    return df

def get_setting(key: str, default: str = "") -> str:
    """Obtiene un valor de configuración."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key: str, value: str):
    """Guarda un valor de configuración."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_batches_df() -> pd.DataFrame:
    """Devuelve historial de lotes importados."""
    conn = get_connection()
    df = pd.read_sql_query("""
    SELECT 
        batch_id as "ID Lote",
        filename as "Archivo",
        uploaded_at as "Fecha Carga",
        total_rows as "Total Filas",
        new_records as "Nuevos Registros"
    FROM import_batches
    ORDER BY uploaded_at DESC
    """, conn)
    conn.close()
    return df

def delete_batch(batch_id: str):
    """Elimina las marcaciones asociadas a un lote específico."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance_logs WHERE batch_id = ?", (batch_id,))
    cursor.execute("DELETE FROM import_batches WHERE batch_id = ?", (batch_id,))
    conn.commit()
    conn.close()

def mask_name(name: str) -> str:
    """
    Enmascara un nombre completo mostrando solo algunas letras y el resto con asteriscos
    para cumplimiento estricto de protección de datos (Habeas Data).
    Ejemplos:
    - 'Alejandro' -> 'Al******o'
    - 'Pérez' -> 'Pé**z'
    - 'Pb' -> 'P*'
    - 'Ana' -> 'A*a'
    """
    if not name or not isinstance(name, str):
        return ""
    
    masked_words = []
    for word in name.strip().split():
        clean_word = word.strip()
        length = len(clean_word)
        if length <= 1:
            masked_words.append(clean_word)
        elif length == 2:
            masked_words.append(clean_word[0] + "*")
        elif length == 3:
            masked_words.append(clean_word[0] + "*" + clean_word[-1])
        else:
            masked_words.append(clean_word[:2] + "*" * (length - 3) + clean_word[-1])
            
    return " ".join(masked_words)

