import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database import search_students_by_query, get_student_by_id, get_student_attendance

def render_student_view():
    # Banner Principal con identidad Medicina UdeA
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge-udea">Universidad de Antioquia • Facultad de Medicina</div>
        <h1 class="hero-title">Control de Asistencia Estudiantil</h1>
        <p class="hero-subtitle">
            Consulta privada de marcaciones biométricas para estudiantes y personal asistencial.
            Digita tu número de identificación o nombre completo para acceder a tu historial y métricas mensuales.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Campo de búsqueda
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        search_query = st.text_input(
            "Buscar estudiante",
            placeholder="Digita tu ID (ej. 264) o Nombre (ej. Alejo Pb)...",
            label_visibility="collapsed",
            key="student_search_input"
        )
    with col_btn:
        search_btn = st.button("🔍 Consultar", type="primary", use_container_width=True)
        
    if not search_query.strip():
        # Estado inicial: Información institucional y privacidad
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem 2rem; margin-top: 1rem;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🩺</div>
            <h3 style="color: #f0fdf4; margin-bottom: 0.5rem; font-weight: 700;">Consulta Confidencial de Asistencia</h3>
            <p style="color: #94a3b8; max-width: 580px; margin: 0 auto 1.5rem auto; font-size: 0.95rem; line-height: 1.6;">
                En cumplimiento con las directrices de privacidad institucional de la Universidad de Antioquia, 
                este portal permite consultar tus asistencias individuales digitando tu ID o nombre sin exponer las listas generales.
            </p>
            <div style="display: inline-flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
                <span class="badge-info">🏛️ Facultad de Medicina UdeA</span>
                <span class="badge-info">⚡ Monitoreo Biométrico en Vivo</span>
                <span class="badge-info">📅 Balance Mensual Completo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
        
    # Realizar búsqueda
    results = search_students_by_query(search_query, limit=15)
    
    if not results:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 2.5rem 1.5rem; border-color: rgba(239, 68, 68, 0.4);">
            <div style="font-size: 3rem; margin-bottom: 0.8rem;">🔎</div>
            <h4 style="color: #f87171; margin-bottom: 0.5rem;">No se encontraron registros</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; max-width: 480px; margin: 0 auto;">
                No existe ningún estudiante registrado con el término <b>"{search_query}"</b>. Verifica que hayas digitado correctamente tu nombre o ID asignado en el sistema biométrico.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
        
    # Selección si hay múltiples resultados
    selected_student_id = results[0]['student_id']
    if len(results) > 1:
        st.info(f"Se encontraron **{len(results)}** coincidencias. Selecciona tu perfil:")
        options = {f"{r['name']} — ID: {r['student_id']} ({r['department']})": r['student_id'] for r in results}
        selected_label = st.selectbox("Seleccionar perfil", list(options.keys()), label_visibility="collapsed")
        selected_student_id = options[selected_label]
        
    # Obtener detalles del estudiante seleccionado
    student = get_student_by_id(selected_student_id)
    if not student:
        st.error("No se pudo cargar la información del estudiante.")
        return
        
    # Obtener marcaciones
    logs_df = get_student_attendance(selected_student_id)
    
    # Calcular estado del día de hoy
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_records = logs_df[logs_df['date'] == today_str] if not logs_df.empty else pd.DataFrame()
    attended_today = not today_records.empty
    
    # Generar iniciales para avatar
    initials = "".join([part[0].upper() for part in student['name'].split()[:2]]) or "MD"
    
    # Renderizar tarjeta de perfil estilo Medicina UdeA
    if attended_today:
        hora_marcacion = today_records.iloc[0]['time']
        status_html = f'<div class="badge-success">🟢 Presente hoy ({hora_marcacion})</div>'
    else:
        status_html = '<div class="badge-warning">🟡 Sin registro hoy</div>'
        
    st.markdown(f"""
    <div class="student-profile-card">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div style="display: flex; align-items: center; gap: 1.2rem;">
                <div class="student-avatar">{initials}</div>
                <div>
                    <h2 style="color: #ffffff; margin: 0 0 0.3rem 0; font-weight: 800; font-size: 1.6rem;">{student['name']}</h2>
                    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                        <span style="color: #34d399; font-weight: 700; font-size: 0.95rem;">ID: {student['student_id']}</span>
                        <span style="color: #64748b;">•</span>
                        <span style="color: #cbd5e1; font-size: 0.95rem;">Rotación / Grupo: <b>{student['department']}</b></span>
                    </div>
                </div>
            </div>
            <div>
                {status_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cálculos para el MES COMPLETO
    now = datetime.now()
    mes_actual_str = now.strftime("%Y-%m")
    nombre_mes = now.strftime("%B %Y").capitalize()
    
    total_asistencias = len(logs_df)
    dias_totales = logs_df['date'].nunique() if not logs_df.empty else 0
    
    # Días asistidos en el mes actual
    dias_este_mes = 0
    marcaciones_este_mes = 0
    if not logs_df.empty:
        df_mes = logs_df[logs_df['date'].str.startswith(mes_actual_str)]
        dias_este_mes = df_mes['date'].nunique()
        marcaciones_este_mes = len(df_mes)
    
    # Horario promedio de llegada
    hora_promedio = "N/A"
    if not logs_df.empty:
        try:
            minutes = logs_df['time'].apply(lambda t: int(t.split(':')[0]) * 60 + int(t.split(':')[1]))
            avg_min = int(minutes.mean())
            hora_promedio = f"{avg_min // 60:02d}:{avg_min % 60:02d}"
        except Exception:
            hora_promedio = "N/A"
            
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Marcaciones del Mes</div>
            <div class="kpi-value" style="color: #34d399;">{marcaciones_este_mes}</div>
            <div class="kpi-subtext">Mes en curso ({mes_actual_str})</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Días Asistidos (Mes)</div>
            <div class="kpi-value" style="color: #6ee7b7;">{dias_este_mes} días</div>
            <div class="kpi-subtext">Fechas activas en el mes</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Hora Promedio Llegada</div>
            <div class="kpi-value" style="color: #fcd34d;">{hora_promedio}</div>
            <div class="kpi-subtext">Horario habitual de entrada</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Histórico Acumulado</div>
            <div class="kpi-value" style="color: #f0fdf4;">{dias_totales}</div>
            <div class="kpi-subtext">Total días asistidos global</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
    
    if logs_df.empty:
        st.warning("No hay registros de asistencia disponibles para este estudiante.")
        return
        
    # Pestañas de detalle
    tab_graficos, tab_tabla = st.tabs(["📊 Gráficos y Balance Mensual", "📋 Historial Completo de Marcaciones"])
    
    with tab_graficos:
        c_chart1, c_chart2 = st.columns(2)
        
        with c_chart1:
            # Gráfico de asistencias por fecha
            daily_counts = logs_df.groupby('date').size().reset_index(name='Marcaciones')
            daily_counts = daily_counts.sort_values(by='date')
            
            fig1 = px.bar(
                daily_counts, 
                x='date', 
                y='Marcaciones',
                title="Historial de Asistencias Diarias",
                labels={'date': 'Fecha', 'Marcaciones': 'Marcaciones Registradas'},
                color_discrete_sequence=['#059669']
            )
            fig1.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                height=320,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(16, 185, 129, 0.15)")
            )
            st.plotly_chart(fig1, use_container_width=True)
            
        with c_chart2:
            # Horarios exactos de llegada (hora decimal)
            logs_df['minuto_dia'] = logs_df['time'].apply(lambda t: int(t.split(':')[0]) + int(t.split(':')[1])/60.0)
            fig2 = px.scatter(
                logs_df,
                x='date',
                y='minuto_dia',
                title="Hora de Entrada por Jornada",
                labels={'date': 'Fecha', 'minuto_dia': 'Hora'},
                color_discrete_sequence=['#34d399'],
                size=[14]*len(logs_df)
            )
            fig2.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20),
                height=320,
                xaxis=dict(showgrid=False),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(16, 185, 129, 0.15)",
                    tickmode='array',
                    tickvals=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                    ticktext=['7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM']
                )
            )
            st.plotly_chart(fig2, use_container_width=True)
            
    with tab_tabla:
        # Tabla detallada con descarga
        display_df = logs_df[['date', 'time', 'device_id']].copy()
        display_df.columns = ['Fecha', 'Hora de Entrada', 'Dispositivo']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Botón para descargar reporte individual en Excel o CSV
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Certificado de Asistencia Individual (CSV)",
            data=csv_data,
            file_name=f"asistencia_udea_medicina_{student['student_id']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
