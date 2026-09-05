# 🎓 Sistema de Control de Asistencia Estudiantil en Tiempo Real

Dashboard interactivo desarrollado en **Streamlit** para la gestión, análisis y consulta confidencial de asistencia de estudiantes a partir de las exportaciones de relojes biométricos o dispositivos de control de acceso.

---

## 🌟 Características Principales

### 1. 🔍 Portal de Consulta Individual para Estudiantes (Público)
- **Privacidad Total**: No expone la lista general de estudiantes ni datos confidenciales a otros alumnos.
- **Búsqueda Instantánea**: Consulta por **Nombre** (ej. *Alejo Pb*) o **ID / Matrícula** (ej. *264*).
- **Ficha Personal del Estudiante**:
  - Avatar dinámico, nombre, ID y departamento.
  - Indicador de estado del día: 🟢 *Presente hoy* o 🟡 *Sin registro hoy*.
  - KPIs personales: Total marcaciones, días asistidos, hora promedio habitual de llegada.
- **Gráficos Interactivos con Plotly**: Historial de marcaciones por fecha y dispersión de horarios de entrada.
- **Historial Completo**: Tabla detallada con opción de descargar comprobante/reporte individual en CSV.

### 2. 🔐 Panel Administrativo Completo
- **Acceso Protegido**: Clave de administrador (`admin123` por defecto, configurable en la pestaña de ajustes).
- **Carga Semanal de Archivos**:
  - Compatible con archivos `.txt`, `.tsv`, `.csv`, `.dat` y `.xlsx` exportados por el reloj biométrico.
  - Motor inteligente de limpieza que normaliza columnas (`ID.`, `Nombre`, `Depart.`, `Tiempo`, `ID del dispositivo`).
  - Previsualización en tiempo real antes de guardar.
  - **Sin sobreescritura ni duplicados**: Utiliza restricciones únicas en SQLite para que subir archivos solapados de varias semanas no duplique registros.
  - Auditoría de lotes importados con fecha, nombre de archivo y opción de reversión.
- **Dashboard Global con Analítica Ejecutiva**:
  - Métricas acumuladas: Total de estudiantes, asistencias totales, asistieron hoy, última fecha registrada.
  - Horas pico de llegada (distribución por hora).
  - Porcentaje y distribución por departamento / carrera / grado.
  - Tendencia diaria de afluencia de alumnos únicos.
- **Explorador Maestro con Filtros Avanzados**:
  - Visualización completa de **absolutamente todos los involucrados**.
  - Filtros en vivo por rango de fechas (Desde - Hasta), departamento y buscador por texto.
  - Exportación directa a **Excel (.xlsx)** y **CSV**.
- **Directorio de Estudiantes y Configuración**:
  - Directorio maestro con totales de asistencia y última marcación registrada.
  - Cambio de clave de administrador y nombre de la institución.

---

## 🚀 Cómo Iniciar la Aplicación

Para ejecutar la aplicación localmente en tu máquina:

```powershell
# 1. Abre PowerShell en la carpeta del proyecto:
cd "C:\Users\WinterOS\.gemini\antigravity-ide\scratch\student-attendance-dashboard"

# 2. Ejecuta Streamlit con uv o con el entorno virtual:
& "C:\Users\WinterOS\.local\bin\uv.exe" run streamlit run app.py
```

O si prefieres usar el ejecutable directo del entorno virtual:
```powershell
.venv\Scripts\streamlit.exe run app.py
```

La aplicación se abrirá automáticamente en tu navegador web en:
👉 `http://localhost:8501`

---

## 🔑 Credenciales por Defecto
- **Contraseña de Administrador:** `admin123` *(puedes cambiarla en el panel administrativo)*
- **IDs de Prueba:** `264` (Alejo Pb), `265` (JAVI G), `267` (MARIO V), etc.
