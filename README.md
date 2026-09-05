# 🩺 Sistema de Control de Asistencia - Facultad de Medicina UdeA

Dashboard interactivo en tiempo real desarrollado en **Streamlit** para el registro, seguimiento y analítica de asistencia de estudiantes y rotaciones clínicas de la **Facultad de Medicina de la Universidad de Antioquia (Medellín, Colombia)** a partir de reportes biométricos.

---

## 🏛️ Identidad y Características

- **Paleta Institucional UdeA**: Diseñado con el verde oficial de la Universidad de Antioquia (`#006837`), tonos esmeralda profundos y detalles dorados.
- **Enfoque de Balance Mensual**:
  - Métricas centradas en el **mes completo en curso** (días asistidos en el mes, marcaciones totales del mes y porcentaje de asistencia).
  - Histórico acumulado sin límite temporal.
- **Portal Estudiantil Confidencial**:
  - Búsqueda privada por **Nombre** o **ID** (evita la exposición pública de las listas de estudiantes).
  - Estado del día en tiempo real (🟢 *Presente hoy* con hora exacta o 🟡 *Sin registro hoy*).
  - Ficha médica del estudiante con gráficos interactivos y descarga de certificado en CSV.
- **Panel Administrativo Protegido**:
  - Acceso seguro mediante clave (`admin123` por defecto, modificable).
  - **Carga Semanal de Archivos**: Compatible con archivos `.txt`, `.tsv`, `.csv` y `.xlsx` del reloj biométrico. Omite duplicados automáticamente.
  - **Dashboard Global**: KPIs mensuales e históricos, horas pico de llegada a clases/rotaciones, asistencias por departamento y tendencia diaria.
  - **Explorador Maestro**: Visualización de absolutamente todos los estudiantes, filtros por rotación/fecha y exportación directa a **Excel (.xlsx)** y **CSV**.

---

## 🚀 Despliegue en Streamlit Community Cloud

Para desplegar esta aplicación de forma gratuita en la nube de Streamlit:

### Paso 1: Crear un nuevo repositorio en GitHub
1. Ingresa a tu cuenta de [GitHub](https://github.com/new).
2. Crea un nuevo repositorio (por ejemplo: `asistencia-medicina-udea`).
3. Elige la visibilidad (*Público* o *Privado*). **No** marques la opción de agregar README ni .gitignore (ya están incluidos en este proyecto).

### Paso 2: Vincular y subir tu código local
Abre una terminal PowerShell en la carpeta del proyecto y ejecuta:

```powershell
cd "C:\Users\WinterOS\.gemini\antigravity-ide\scratch\student-attendance-dashboard"

# Reemplaza TU-USUARIO y TU-REPOSITORIO con tus datos de GitHub:
git remote add origin https://github.com/TU-USUARIO/asistencia-medicina-udea.git
git push -u origin main
```

### Paso 3: Desplegar en Streamlit Cloud
1. Entra a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New app"**.
3. Selecciona tu repositorio recién subido: `TU-USUARIO/asistencia-medicina-udea`.
4. En **Main file path**, ingresa: `app.py`.
5. Haz clic en **"Deploy!"**.

¡Tu aplicación quedará en línea con enlace público seguro (HTTPS) para que docentes, coordinadores y estudiantes puedan consultarla desde cualquier dispositivo!

---

## 💻 Ejecución Local

Si deseas correr la aplicación en tu computador:

```powershell
cd "C:\Users\WinterOS\.gemini\antigravity-ide\scratch\student-attendance-dashboard"
& "C:\Users\WinterOS\.local\bin\uv.exe" run streamlit run app.py
```

Acceso local: `http://localhost:8501`
- **Clave administrativa inicial:** `admin123`
- **IDs de prueba incluidos:** `264` (Alejo Pb), `265` (JAVI G), `267` (MARIO V), etc.
