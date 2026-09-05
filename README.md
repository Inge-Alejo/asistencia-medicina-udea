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
