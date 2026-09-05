import streamlit as st
from datetime import datetime
from database import init_db, get_overall_kpis, save_logs_batch
from importer import parse_attendance_file, get_sample_attendance_text
from styles import apply_custom_styles
from views.student_view import render_student_view
from views.admin_view import render_admin_view

# Configuración inicial de Streamlit con identidad Medicina UdeA
st.set_page_config(
    page_title="Asistencia - Facultad de Medicina UdeA",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Base de Datos y sembrar datos de muestra si está vacía
init_db()
kpis = get_overall_kpis()
if kpis['total_students'] == 0:
    try:
        sample_df = parse_attendance_file(get_sample_attendance_text(), "inicial_medicina_udea.txt")
        save_logs_batch(sample_df, "inicial_medicina_udea.txt")
    except Exception:
        pass

# Aplicar estilos CSS personalizados (Verde y esmeralda UdeA)
apply_custom_styles()

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) - NAVEGACIÓN INSTITUCIONAL
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0 1.2rem 0;">
        <div style="font-size: 2.8rem; margin-bottom: 0.2rem;">🩺</div>
        <div style="font-size: 0.75rem; font-weight: 800; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.08em;">
            Universidad de Antioquia
        </div>
        <h3 style="color: #ffffff; margin: 0.2rem 0 0 0; font-weight: 800; font-size: 1.2rem;">Facultad de Medicina</h3>
        <p style="color: #34d399; font-size: 0.8rem; font-weight: 600; margin-top: 0.2rem;">
            Control de Asistencia Biométrico
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Selector de Rol / Modo
    st.markdown("### 🧭 Modo de Acceso")
    mode = st.radio(
        "Seleccione vista",
        options=["🎓 Consulta Estudiantes (Público)", "🔐 Panel Administrativo"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Monitor de Tiempo Real
    st.markdown("### ⚡ Monitor en Vivo")
    now_str = datetime.now().strftime("%H:%M:%S")
    st.caption(f"🕒 Última sincronización: **{now_str}**")
    
    # Botón de refresco manual
    if st.button("🔄 Sincronizar Ahora", use_container_width=True):
        st.rerun()
        
    # Auto-refresco opcional
    auto_refresh = st.checkbox("Monitoreo continuo (cada 15s)", value=False)
    if auto_refresh:
        st.markdown(
            """
            <script>
            setTimeout(function(){
                window.parent.location.reload();
            }, 15000);
            </script>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.78rem; color: #94a3b8; text-align: center; line-height: 1.4; padding-top: 0.5rem;">
        <b>Medellín, Colombia</b><br>
        Facultad de Medicina • UdeA<br>
        Sistema de Registro y Reporte Semanal
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# ENRUTAMIENTO PRINCIPAL
# -------------------------------------------------------------
if "Consulta Estudiantes" in mode:
    render_student_view()
else:
    render_admin_view()
