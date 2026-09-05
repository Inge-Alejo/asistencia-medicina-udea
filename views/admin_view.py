import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database import (
    get_overall_kpis,
    get_all_attendance_filtered,
    get_all_students_df,
    get_distinct_departments,
    get_hourly_distribution,
    get_daily_trend,
    get_batches_df,
    delete_batch,
    save_logs_batch,
    get_setting,
    set_setting
)
from importer import parse_attendance_file, get_sample_attendance_text

# Paleta oficial UdeA Medicina
UDEA_GREEN_SCALE = ['#006837', '#059669', '#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#fcd34d']

def render_admin_login():
    """Formulario de acceso seguro al panel administrativo con estilo Medicina UdeA."""
    st.markdown("""
    <div class="hero-container" style="max-width: 550px; margin: 2rem auto 1rem auto; text-align: center;">
        <div class="hero-badge-udea">Universidad de Antioquia • Facultad de Medicina</div>
        <div style="font-size: 3rem; margin: 0.5rem 0;">🔐</div>
        <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 0.5rem;">Acceso Administrativo</h2>
        <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1.5rem;">
            Ingresa las credenciales autorizadas de coordinación académica para gestionar cargas semanales y reportes globales.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        with st.form("admin_login_form"):
            password_input = st.text_input("Contraseña de Coordinación", type="password", placeholder="Ingresa tu clave...")
            submitted = st.form_submit_button("Ingresar al Panel de Gestión", type="primary", use_container_width=True)
            
            if submitted:
                expected_pwd = get_setting("admin_password", "admin123")
                if password_input == expected_pwd:
                    st.session_state['admin_authenticated'] = True
                    st.success("¡Autenticación exitosa! Bienvenido.")
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta. (Clave por defecto: admin123)")
                    
        st.caption("🔒 *Clave inicial de fábrica: `admin123` (Puedes modificarla en la pestaña de Ajustes)*")

def render_admin_view():
    """Panel administrativo completo con branding Medicina UdeA."""
    if not st.session_state.get('admin_authenticated', False):
        render_admin_login()
        return

    # Header del Panel con botón de logout
    c_title, c_logout = st.columns([5, 1])
    with c_title:
        st.markdown("""
        <div class="hero-container" style="padding: 1.5rem 2rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div class="hero-badge-udea">Facultad de Medicina • Universidad de Antioquia</div>
                    <h2 class="hero-title" style="font-size: 1.8rem; margin: 0.2rem 0;">Panel de Gestión de Asistencia</h2>
                    <p class="hero-subtitle" style="font-size: 0.92rem;">Monitoreo en tiempo real, balance mensual consolidado y carga de reportes biométricos.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_logout:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state['admin_authenticated'] = False
            st.rerun()

    # Pestañas principales
    tab_dash, tab_upload, tab_master, tab_students = st.tabs([
        "📊 Dashboard Global y Mensual",
        "📁 Carga Semanal de Archivos",
        "📋 Explorador Maestro",
        "👥 Directorio de Estudiantes & Ajustes"
    ])

    # -------------------------------------------------------------
    # PESTAÑA 1: DASHBOARD GLOBAL Y MENSUAL
    # -------------------------------------------------------------
    with tab_dash:
        kpis = get_overall_kpis()
        
        # Tarjetas KPI Globales con énfasis en el Mes Completo
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Estudiantes Registrados</div>
                <div class="kpi-value" style="color: #34d399;">{kpis['total_students']}</div>
                <div class="kpi-subtext">Base de datos de medicina</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Marcaciones del Mes</div>
                <div class="kpi-value" style="color: #6ee7b7;">{kpis.get('logs_this_month', kpis['total_logs'])}</div>
                <div class="kpi-subtext">Mes {kpis.get('current_month_prefix', '')} ({kpis.get('students_this_month', 0)} alumnos)</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Presentes Hoy</div>
                <div class="kpi-value" style="color: #a7f3d0;">{kpis['students_today']}</div>
                <div class="kpi-subtext">Marcaciones del día de hoy</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Histórico</div>
                <div class="kpi-value" style="color: #fcd34d;">{kpis['total_logs']}</div>
                <div class="kpi-subtext">Marcaciones acumuladas totales</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)

        # Gráficos Analíticos
        g_col1, g_col2 = st.columns(2)
        
        with g_col1:
            # Distribución por Hora (Horas Pico de Entrada a Rotaciones/Clases)
            hourly_df = get_hourly_distribution()
            if not hourly_df.empty:
                hourly_df['hora_label'] = hourly_df['hora'].apply(lambda h: f"{h:02d}:00")
                fig_hour = px.bar(
                    hourly_df,
                    x='hora_label',
                    y='total',
                    title="Afluencia por Hora del Día (Horas Pico de Entrada)",
                    labels={'hora_label': 'Hora de Marcaje', 'total': 'Total Marcaciones'},
                    color_discrete_sequence=['#006837']
                )
                fig_hour.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=320,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(16, 185, 129, 0.15)")
                )
                st.plotly_chart(fig_hour, use_container_width=True)
            else:
                st.info("Sin datos suficientes para graficar horarios.")

        with g_col2:
            # Asistencia por Departamento / Rotación Clínica
            students_df = get_all_students_df()
            if not students_df.empty and 'Departamento / Grado' in students_df.columns:
                dep_counts = students_df.groupby('Departamento / Grado')['Total Asistencias'].sum().reset_index()
                fig_dep = px.pie(
                    dep_counts,
                    names='Departamento / Grado',
                    values='Total Asistencias',
                    title="Distribución por Departamento / Rotación Clínica",
                    color_discrete_sequence=UDEA_GREEN_SCALE,
                    hole=0.45
                )
                fig_dep.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=320
                )
                st.plotly_chart(fig_dep, use_container_width=True)
            else:
                st.info("Sin datos suficientes para graficar departamentos.")

        # Tendencia Diaria del Mes Completo
        trend_df = get_daily_trend(days=31)
        if not trend_df.empty:
            fig_trend = px.line(
                trend_df,
                x='Fecha',
                y='Estudiantes Únicos',
                title="Evolución de Asistencia Diaria (Alumnos Únicos por Jornada)",
                markers=True,
                color_discrete_sequence=['#10b981']
            )
            fig_trend.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(16, 185, 129, 0.15)")
            )
            st.plotly_chart(fig_trend, use_container_width=True)

    # -------------------------------------------------------------
    # PESTAÑA 2: CARGA SEMANAL DE ARCHIVOS
    # -------------------------------------------------------------
    with tab_upload:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 1.5rem;">
            <h3 style="color: #ffffff; margin-bottom: 0.5rem; font-weight: 700;">Subir Reporte Biométrico Semanal</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">
                Carga el archivo exportado por el reloj o dispositivo de control de acceso de la Facultad de Medicina. 
                Soporta extensiones <code>.txt</code>, <code>.tsv</code>, <code>.csv</code> o <code>.xlsx</code>.
                El sistema acumula los registros de forma segura y <b>descarta automáticamente duplicados existentes</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_up, col_sample = st.columns([3, 1])
        with col_up:
            uploaded_file = st.file_uploader(
                "Seleccionar archivo del dispositivo",
                type=['txt', 'csv', 'tsv', 'dat', 'xlsx'],
                help="Arrastra o selecciona el archivo descargado de tu dispositivo biométrico."
            )
        with col_sample:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            load_sample_btn = st.button("🧪 Cargar Datos de Prueba", use_container_width=True, help="Inserta los registros de prueba con alejo pb, JAVI G, MARIO V...")

        # Cargar archivo de prueba
        if load_sample_btn:
            try:
                sample_text = get_sample_attendance_text()
                parsed_sample = parse_attendance_file(sample_text, "asistencia_medicina_udea.txt")
                res = save_logs_batch(parsed_sample, "asistencia_medicina_udea.txt")
                st.success(f"¡Lote de prueba importado con éxito! {res['new_records']} registros nuevos guardados ({res['skipped_duplicates']} duplicados ignorados).")
                st.rerun()
            except Exception as e:
                st.error(f"Error al cargar archivo de prueba: {e}")

        # Archivo subido por el usuario
        if uploaded_file is not None:
            try:
                file_bytes = uploaded_file.getvalue()
                df_clean = parse_attendance_file(file_bytes, uploaded_file.name)
                
                if df_clean.empty:
                    st.warning("El archivo no contiene registros válidos de asistencia.")
                else:
                    st.markdown(f"#### 🔎 Vista Previa ({len(df_clean)} filas detectadas)")
                    
                    p1, p2, p3 = st.columns(3)
                    p1.metric("Filas en Archivo", len(df_clean))
                    p2.metric("Estudiantes Distintos", df_clean['student_id'].nunique())
                    p3.metric("Rango de Fechas", f"{df_clean['date'].min()} a {df_clean['date'].max()}")

                    st.dataframe(df_clean.head(10), use_container_width=True, hide_index=True)

                    if st.button("💾 Confirmar e Importar a Base de Datos", type="primary"):
                        result = save_logs_batch(df_clean, uploaded_file.name)
                        st.success(f"""
                        **¡Importación completada exitosamente!**
                        - 📥 Total de registros procesados: **{result['total_rows']}**
                        - ✨ Nuevos registros insertados: **{result['new_records']}**
                        - 🔄 Registros existentes (omitidos sin duplicar): **{result['skipped_duplicates']}**
                        """)
                        st.rerun()
            except Exception as ex:
                st.error(f"Error al procesar el archivo: {ex}")

        # Historial de lotes cargados
        st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
        st.subheader("📜 Historial de Lotes Importados")
        batches_df = get_batches_df()
        if not batches_df.empty:
            st.dataframe(batches_df, use_container_width=True, hide_index=True)
            
            with st.expander("⚠️ Opciones de reversión de lote"):
                batch_to_delete = st.selectbox("Seleccionar lote para eliminar sus marcaciones:", batches_df['ID Lote'].tolist())
                if st.button(f"🗑️ Revertir Lote {batch_to_delete}", type="secondary"):
                    delete_batch(batch_to_delete)
                    st.warning(f"Lote {batch_to_delete} eliminado correctamente.")
                    st.rerun()
        else:
            st.info("Aún no se han registrado lotes de importación.")

    # -------------------------------------------------------------
    # PESTAÑA 3: EXPLORADOR MAESTRO DE ASISTENCIA
    # -------------------------------------------------------------
    with tab_master:
        st.markdown("### 📋 Registro Consolidado de Asistencia (Todos los Estudiantes)")
        st.caption("Visualiza, filtra y descarga el historial completo de todos los estudiantes y rotaciones clínicas.")

        # Filtros
        col_f1, col_f2, col_f3, col_f4 = st.columns([2, 2, 2, 2])
        with col_f1:
            filtro_busqueda = st.text_input("Buscar por Nombre o ID", placeholder="Ej: alejo, 264...")
        with col_f2:
            departamentos = get_distinct_departments()
            filtro_dep = st.selectbox("Departamento / Rotación", departamentos)
        with col_f3:
            filtro_fecha_inicio = st.date_input("Fecha Desde", value=None)
        with col_f4:
            filtro_fecha_fin = st.date_input("Fecha Hasta", value=None)

        start_str = filtro_fecha_inicio.strftime('%Y-%m-%d') if filtro_fecha_inicio else None
        end_str = filtro_fecha_fin.strftime('%Y-%m-%d') if filtro_fecha_fin else None

        master_df = get_all_attendance_filtered(
            start_date=start_str,
            end_date=end_str,
            department=filtro_dep,
            search=filtro_busqueda
        )

        st.markdown(f"**Total de marcaciones encontradas:** `{len(master_df)}`")
        
        display_master = master_df.drop(columns=['Timestamp'], errors='ignore')
        st.dataframe(display_master, use_container_width=True, hide_index=True)

        # Botones de exportación
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv_all = display_master.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Exportar a CSV",
                data=csv_all,
                file_name=f"asistencia_udea_medicina_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_exp2:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                display_master.to_excel(writer, index=False, sheet_name="Asistencia UdeA")
            excel_data = excel_buffer.getvalue()
            st.download_button(
                "📊 Exportar a Excel (.xlsx)",
                data=excel_data,
                file_name=f"asistencia_udea_medicina_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    # -------------------------------------------------------------
    # PESTAÑA 4: DIRECTORIO DE ESTUDIANTES & AJUSTES
    # -------------------------------------------------------------
    with tab_students:
        st.subheader("👥 Directorio de Estudiantes Registrados")
        students_catalog = get_all_students_df()
        st.dataframe(students_catalog, use_container_width=True, hide_index=True)

        st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
        st.subheader("⚙️ Configuración Institucional")
        
        with st.form("settings_form"):
            current_pwd = get_setting("admin_password", "admin123")
            current_inst = get_setting("institution_name", "Universidad de Antioquia - Facultad de Medicina")
            
            new_inst = st.text_input("Institución / Dependencia", value=current_inst)
            new_pwd = st.text_input("Cambiar Contraseña Administrativa", value=current_pwd, type="password")
            
            save_settings = st.form_submit_button("Guardar Cambios de Configuración", type="primary")
            if save_settings:
                set_setting("institution_name", new_inst)
                set_setting("admin_password", new_pwd)
                st.success("¡Configuración actualizada con éxito!")
                st.rerun()
