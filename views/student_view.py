import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
from datetime import datetime
from database import (
    search_students_by_query,
    get_student_by_id,
    get_student_attendance,
    mask_name,
    get_spanish_day_name,
    get_spanish_date_formatted,
    get_total_sessions_count
)

# Paleta Semillero Medicina UdeA
COLOR_SEMILLERO_GREEN = "#558b2f"
COLOR_GOLD = "#e58e12"
COLOR_DEEP_GREEN = "#2e7d32"

def render_mini_calendar(logs_df: pd.DataFrame):
    """Renderiza el mini-calendario mensual con los días asistidos resaltados."""
    if logs_df.empty:
        st.info("No hay fechas de asistencia registradas para mostrar en el calendario.")
        return
        
    now = datetime.now()
    # Meses presentes en el historial del estudiante
    meses_disponibles = sorted(logs_df['date'].str.slice(0, 7).unique(), reverse=True)
    if not meses_disponibles:
        meses_disponibles = [now.strftime("%Y-%m")]
        
    spanish_months_map = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
        "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
        "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }
    
    def format_month_label(m_str):
        try:
            y, m = m_str.split('-')
            return f"{spanish_months_map.get(m, m)} {y}"
        except Exception:
            return m_str
            
    col_sel, col_stats = st.columns([2, 3])
    with col_sel:
        selected_month = st.selectbox(
            "Mes en el Calendario",
            options=meses_disponibles,
            format_func=format_month_label,
            key="cal_selected_month"
        )
        
    df_mes = logs_df[logs_df['date'].str.startswith(selected_month)]
    attended_days_dict = {}
    for _, row in df_mes.iterrows():
        try:
            day_int = int(row['date'].split('-')[2])
            if day_int not in attended_days_dict:
                attended_days_dict[day_int] = []
            attended_days_dict[day_int].append(row['time'])
        except Exception:
            pass
            
    year_sel, month_sel = map(int, selected_month.split('-'))
    first_weekday, num_days = calendar.monthrange(year_sel, month_sel)
    
    with col_stats:
        dias_asistidos_mes = len(attended_days_dict)
        st.markdown(f"""
        <div style="padding-top: 1.8rem; font-size: 0.92rem; color: #4b5563;">
            Total días asistidos en <b>{format_month_label(selected_month)}</b>: 
            <span style="font-weight: 800; color: #2e7d32; font-size: 1.15rem;">{dias_asistidos_mes}</span>
        </div>
        """, unsafe_allow_html=True)
        
    days_headers = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    header_cells_html = "".join([f'<div class="cal-header-cell">{h}</div>' for h in days_headers])
    
    today_dt = now.date()
    grid_cells_html = []
    
    # Celdas vacías previas al día 1
    for _ in range(first_weekday):
        grid_cells_html.append('<div class="cal-day-cell empty"></div>')
        
    for day in range(1, num_days + 1):
        cell_date = datetime(year_sel, month_sel, day).date()
        is_today = (cell_date == today_dt)
        is_attended = (day in attended_days_dict)
        
        classes = ["cal-day-cell"]
        if is_attended:
            classes.append("attended")
        if is_today:
            classes.append("today")
            
        badge_html = ""
        dia_semana_nombre = get_spanish_day_name(f"{year_sel:04d}-{month_sel:02d}-{day:02d}")
        title_attr = f"{dia_semana_nombre} {day} de {spanish_months_map.get(f'{month_sel:02d}', '')}"
        
        if is_attended:
            horas_str = ", ".join(attended_days_dict[day])
            badge_html = '<span class="cal-check-badge">✓ Asistió</span>'
            title_attr += f" • Hora: {horas_str}"
        elif is_today:
            badge_html = '<span class="cal-check-badge" style="color: #e58e12;">Hoy</span>'
            
        grid_cells_html.append(f"""
        <div class="{' '.join(classes)}" title="{title_attr}">
            <span>{day}</span>
            {badge_html}
        </div>
        """)
        
    month_title = f"{spanish_months_map.get(f'{month_sel:02d}', '')} {year_sel}"
    calendar_html = f"""
    <div class="cal-card">
        <div class="cal-month-title">
            <span>📅 {month_title}</span>
        </div>
        <div class="cal-grid-header">
            {header_cells_html}
        </div>
        <div class="cal-grid-days">
            {''.join(grid_cells_html)}
        </div>
        <div class="cal-legend">
            <div class="cal-legend-item">
                <div class="cal-legend-dot" style="background: #2e7d32;"></div>
                <span>Día asistido (✓)</span>
            </div>
            <div class="cal-legend-item">
                <div class="cal-legend-dot" style="background: #f9fafb; border: 1px solid #d1d5db;"></div>
                <span>Sin registro</span>
            </div>
            <div class="cal-legend-item">
                <div class="cal-legend-dot" style="background: #ffffff; border: 2px solid #e58e12;"></div>
                <span>Fecha de hoy</span>
            </div>
        </div>
    </div>
    """
    st.markdown(calendar_html, unsafe_allow_html=True)

def render_student_view():
    # Banner Semillero Medicina UdeA (Centrado y elegante)
    st.markdown("""
    <div class="semillero-banner" style="text-align: center;">
        <div style="display: inline-block; text-align: center;">
            <div class="badge-vocacional" style="margin: 0 auto 0.6rem auto;">
                <span class="dot-gold"></span> Experiencia vocacional
            </div>
            <div class="semillero-title-group" style="justify-content: center;">
                <span class="semillero-medicina">Medicina</span>
                <span class="semillero-sub-label"><span class="dot-gold" style="width: 10px; height: 10px;"></span> Semillero</span>
            </div>
            <div class="semillero-tagline">• Camino a la Formación en Salud •</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Campo de búsqueda confidencial
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        search_query = st.text_input(
            "Buscar estudiante",
            placeholder="Ingrese datos...",
            label_visibility="collapsed",
            key="student_search_input"
        )
    with col_btn:
        search_btn = st.button("Consultar", type="primary", use_container_width=True)
        
    if not search_query.strip():
        # Estado inicial limpio y profesional
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2.8rem 2rem; margin-top: 1rem;">
            <div style="font-size: 2.8rem; margin-bottom: 0.6rem; color: #558b2f;">🩺</div>
            <h3 style="color: #2e7d32; margin-bottom: 0.5rem; font-weight: 800; font-size: 1.45rem;">Control de Asistencia Semillero Medicina</h3>
            <p style="color: #4b5563; max-width: 580px; margin: 0 auto; font-size: 0.96rem; line-height: 1.6;">
                Por políticas de protección de datos, este portal no lista públicamente a todos los participantes. 
                Ingresa tu número de documento para consultar tu estado y registros de asistencia.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
        
    # Realizar búsqueda
    results = search_students_by_query(search_query, limit=15)
    
    if not results:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 2rem 1.5rem; border: 1.5px solid #fca5a5; background-color: #fef2f2;">
            <h4 style="color: #b91c1c; margin-bottom: 0.4rem; font-weight: 800;">No se encontraron registros</h4>
            <p style="color: #7f1d1d; font-size: 0.92rem; max-width: 480px; margin: 0 auto;">
                No existe ningún estudiante registrado con el término <b>"{search_query}"</b>. Verifica que hayas digitado correctamente tu nombre o ID asignado.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
        
    # Selección si hay múltiples resultados
    selected_student_id = results[0]['student_id']
    if len(results) > 1:
        st.info(f"Se encontraron **{len(results)}** coincidencias. Selecciona tu perfil:")
        options = {f"{mask_name(r['name'])} — ID: {r['student_id']} ({r['department']})": r['student_id'] for r in results}
        selected_label = st.selectbox("Seleccionar perfil", list(options.keys()), label_visibility="collapsed")
        selected_student_id = options[selected_label]
        
    # Obtener detalles del estudiante seleccionado
    student = get_student_by_id(selected_student_id)
    if not student:
        st.error("No se pudo cargar la información del estudiante.")
        return
        
    # Obtener marcaciones
    logs_df = get_student_attendance(selected_student_id)
    
    # Calcular estado del día de hoy con identificación del día
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_day_name = get_spanish_day_name(today_str)
    today_records = logs_df[logs_df['date'] == today_str] if not logs_df.empty else pd.DataFrame()
    attended_today = not today_records.empty
    
    # Generar iniciales para avatar
    initials = "".join([part[0].upper() for part in student['name'].split()[:2]]) or "MD"
    
    # Renderizar tarjeta de perfil con día de la semana
    if attended_today:
        hora_marcacion = today_records.iloc[0]['time']
        status_html = f'<div class="badge-success">Presente hoy ({today_day_name} • {hora_marcacion})</div>'
    else:
        status_html = f'<div class="badge-warning">Sin registro hoy ({today_day_name})</div>'
        
    st.markdown(f"""
    <div class="student-profile-card">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div style="display: flex; align-items: center; gap: 1.2rem;">
                <div class="student-avatar">{initials}</div>
                <div>
                    <h2 style="color: #2e7d32; margin: 0 0 0.2rem 0; font-weight: 800; font-size: 1.65rem;">{mask_name(student['name'])}</h2>
                    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                        <span style="color: #d97706; font-weight: 800; font-size: 0.95rem;">ID: {student['student_id']}</span>
                        <span style="color: #9ca3af;">•</span>
                        <span style="color: #4b5563; font-size: 0.95rem;">Módulo / Grupo: <b>{student['department']}</b></span>
                    </div>
                </div>
            </div>
            <div>
                {status_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 1. SEMÁFORO Y PROGRESO DE CERTIFICACIÓN ACADÉMICA (OPCIÓN 1)
    # -------------------------------------------------------------
    dias_asistidos_global = logs_df['date'].nunique() if not logs_df.empty else 0
    total_sesiones_programadas = max(get_total_sessions_count(student.get('department')), dias_asistidos_global, 1)
    pct_asistencia = min(round((dias_asistidos_global / total_sesiones_programadas) * 100, 1), 100.0)
    
    if pct_asistencia >= 80.0:
        color_cert = "#2e7d32"
        badge_bg = "#e8f5e9"
        badge_text = "🟢 Al Día — Requisito Cumplido"
        msg_cert = "¡Excelente compromiso! Cumples con el 80% mínimo de asistencia reglamentaria para la certificación del semillero."
    elif pct_asistencia >= 70.0:
        color_cert = "#d97706"
        badge_bg = "#fef3c7"
        badge_text = "🟡 En Observación — Cerca del Límite"
        msg_cert = "Atención: Tu porcentaje de asistencia está cerca del mínimo exigido (80%). Procura asistir puntualmente a las próximas jornadas."
    else:
        color_cert = "#dc2626"
        badge_bg = "#fee2e2"
        badge_text = "🔴 En Riesgo de Inasistencia"
        msg_cert = "Alerta: Tu asistencia actual está por debajo del 80% mínimo reglamentario. Consulta tu situación con la coordinación del Semillero."
        
    st.markdown(f"""
    <div class="cert-progress-card">
        <div class="cert-header-flex">
            <div>
                <div class="cert-title">Cumplimiento y Avance de Certificación</div>
                <div class="cert-subtitle">Requisito reglamentario: Mínimo 80% de asistencia a las jornadas presenciales</div>
            </div>
            <div class="cert-pct-badge" style="background-color: {badge_bg}; color: {color_cert};">
                {pct_asistencia}%
            </div>
        </div>
        <div class="cert-bar-track">
            <div class="cert-bar-fill" style="width: {pct_asistencia}%; background-color: {color_cert};"></div>
        </div>
        <div class="cert-footer-flex">
            <span style="font-weight: 800; color: {color_cert};">{badge_text}</span>
            <span style="color: #4b5563;"><b>{dias_asistidos_global}</b> de <b>{total_sesiones_programadas}</b> jornadas registradas</span>
        </div>
        <div style="font-size: 0.83rem; color: #6b7280; margin-top: 0.45rem; line-height: 1.4;">
            {msg_cert}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas numéricas del mes
    now = datetime.now()
    mes_actual_str = now.strftime("%Y-%m")
    
    dias_totales = logs_df['date'].nunique() if not logs_df.empty else 0
    dias_este_mes = 0
    marcaciones_este_mes = 0
    if not logs_df.empty:
        df_mes = logs_df[logs_df['date'].str.startswith(mes_actual_str)]
        dias_este_mes = df_mes['date'].nunique()
        marcaciones_este_mes = len(df_mes)
    
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
        <div class="kpi-card" style="border-top-color: #558b2f;">
            <div class="kpi-label">Marcaciones del Mes</div>
            <div class="kpi-value" style="color: #558b2f;">{marcaciones_este_mes}</div>
            <div class="kpi-subtext">Mes en curso ({mes_actual_str})</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #2e7d32;">
            <div class="kpi-label">Días Asistidos (Mes)</div>
            <div class="kpi-value" style="color: #2e7d32;">{dias_este_mes} días</div>
            <div class="kpi-subtext">Jornadas activas</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #e58e12;">
            <div class="kpi-label">Hora Promedio Entrada</div>
            <div class="kpi-value" style="color: #d97706;">{hora_promedio}</div>
            <div class="kpi-subtext">Horario habitual de llegada</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #4b5563;">
            <div class="kpi-label">Histórico Acumulado</div>
            <div class="kpi-value" style="color: #374151;">{dias_totales}</div>
            <div class="kpi-subtext">Total días asistidos global</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
    
    if logs_df.empty:
        st.warning("No hay registros de asistencia disponibles para este estudiante.")
        return
        
    # Pestañas principales
    tab_graficos, tab_tabla = st.tabs(["Calendario y Gráficos de Asistencia", "Historial Completo de Marcaciones"])
    
    with tab_graficos:
        # -------------------------------------------------------------
        # 3. MINI-CALENDARIO VISUAL DE ASISTENCIAS (OPCIÓN 3)
        # -------------------------------------------------------------
        st.markdown("<h4 style='color: #2e7d32; font-weight: 800; margin-bottom: 0.8rem;'>Calendario Mensual de Asistencia</h4>", unsafe_allow_html=True)
        render_mini_calendar(logs_df)
        
        st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #2e7d32; font-weight: 800; margin-bottom: 0.8rem;'>Métricas y Distribución Horaria</h4>", unsafe_allow_html=True)
        
        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            daily_counts = logs_df.groupby('date').size().reset_index(name='Marcaciones')
            daily_counts = daily_counts.sort_values(by='date')
            daily_counts['dia_nombre'] = daily_counts['date'].apply(get_spanish_day_name)
            daily_counts['etiqueta'] = daily_counts.apply(lambda r: f"{r['dia_nombre']} {r['date'].split('-')[2]}", axis=1)
            daily_counts['fecha_completa'] = daily_counts['date'].apply(get_spanish_date_formatted)
            
            fig1 = px.bar(
                daily_counts, 
                x='etiqueta', 
                y='Marcaciones',
                title="Historial de Asistencias por Jornada",
                labels={'etiqueta': 'Día de Jornada', 'Marcaciones': 'Marcaciones'},
                color_discrete_sequence=[COLOR_SEMILLERO_GREEN]
            )
            fig1.update_layout(
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font_color="#1f2937",
                margin=dict(l=20, r=20, t=40, b=20),
                height=320,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6")
            )
            st.plotly_chart(fig1, use_container_width=True)
            
        with c_chart2:
            logs_df_plot = logs_df.copy()
            logs_df_plot['minuto_dia'] = logs_df_plot['time'].apply(lambda t: int(t.split(':')[0]) + int(t.split(':')[1])/60.0)
            logs_df_plot['dia_nombre'] = logs_df_plot['date'].apply(get_spanish_day_name)
            
            fig2 = px.scatter(
                logs_df_plot,
                x='date',
                y='minuto_dia',
                title="Hora Exacta de Entrada por Fecha",
                labels={'date': 'Fecha', 'minuto_dia': 'Hora'},
                color_discrete_sequence=[COLOR_GOLD],
                size=[14]*len(logs_df_plot)
            )
            fig2.update_layout(
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font_color="#1f2937",
                margin=dict(l=20, r=20, t=40, b=20),
                height=320,
                xaxis=dict(showgrid=False),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f3f4f6",
                    tickmode='array',
                    tickvals=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                    ticktext=['7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM']
                )
            )
            st.plotly_chart(fig2, use_container_width=True)
            
    with tab_tabla:
        # Tabla con columna 'Día' en español (¿según la fecha cuál día es?)
        display_df = logs_df[['date', 'time', 'device_id']].copy()
        display_df['Día'] = display_df['date'].apply(get_spanish_day_name)
        display_df['Fecha'] = display_df['date']
        display_df['Hora de Entrada'] = display_df['time']
        display_df['Dispositivo'] = display_df['device_id']
        
        display_table = display_df[['Día', 'Fecha', 'Hora de Entrada', 'Dispositivo']]
        st.dataframe(
            display_table,
            use_container_width=True,
            hide_index=True
        )
        
        csv_data = display_table.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Reporte de Asistencia (CSV)",
            data=csv_data,
            file_name=f"asistencia_semillero_medicina_{student['student_id']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
