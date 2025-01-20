import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Tuple

def calculate_market_shares(df: pd.DataFrame) -> Tuple[List[float], float]:
    """
    Calcula participaciones de mercado y CR4
    """
    activity_groups = df.groupby("Nombre de la Unidad Económica")
    n_firms = activity_groups.size()
    
    total_firms = n_firms.sum()
    market_shares = (n_firms / total_firms).tolist()
    
    cr4 = sum(sorted(market_shares, reverse=True)[:4])
    
    return market_shares, cr4

def calculate_hhi(market_shares: List[float]) -> float:
    """Calcula el índice Herfindahl-Hirschman"""
    return sum(share ** 2 for share in market_shares) * 10000

def determine_market_structure(hhi: float, cr4: float, n_firms: int) -> str:
    """
    Determina la estructura de mercado usando múltiples indicadores:
    - HHI
    - CR4 (Ratio de concentración de 4 empresas)
    - Número de empresas
    """
    if hhi > 7500 and cr4 > 0.9:
        return "Monopolio"
    elif hhi > 2500 and cr4 > 0.6:
        return "Oligopolio"
    elif hhi > 1500 and n_firms > 10:
        return "Competencia Monopolística"
    else:
        return "Competencia Perfecta"

def analyze_all_market_structures(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Analiza todas las actividades económicas y clasifica las empresas por estructura de mercado
    """
    market_structures = {"Monopolio": [], "Oligopolio": [], 
                        "Competencia Monopolística": [], "Competencia Perfecta": []}
    
    for activity in df["Nombre de clase de la actividad"].unique():
        df_activity = df[df["Nombre de clase de la actividad"] == activity]
        market_shares, cr4 = calculate_market_shares(df_activity)
        hhi = calculate_hhi(market_shares)
        n_firms = len(df_activity)
        structure = determine_market_structure(hhi, cr4, n_firms)
        market_structures[structure].append(activity)
    
    return market_structures

def cournot_model(n_firms: int, a: float, b: float, c: float) -> Dict:
    """Modelo de Cournot para oligopolio"""
    Q = n_firms * (a - c) / (b * (n_firms + 1))
    P = a - b * Q
    q_individual = Q / n_firms
    profit_individual = (P - c) * q_individual
    
    return {
        "Q_total": Q,
        "P_equilibrio": P,
        "q_individual": q_individual,
        "beneficio_individual": profit_individual
    }

def bertrand_model(c: float) -> Dict:
    """Modelo de Bertrand para oligopolio"""
    return {
        "P_equilibrio": c,
        "beneficio_individual": 0
    }

def stackelberg_model(a: float, b: float, c: float) -> Dict:
    """Modelo de Stackelberg para oligopolio"""
    q_leader = (a - c) / (2 * b)
    q_follower = (a - c - b * q_leader) / (2 * b)
    Q = q_leader + q_follower
    P = a - b * Q
    
    profit_leader = (P - c) * q_leader
    profit_follower = (P - c) * q_follower
    
    return {
        "q_lider": q_leader,
        "q_seguidor": q_follower,
        "Q_total": Q,
        "P_equilibrio": P,
        "beneficio_lider": profit_leader,
        "beneficio_seguidor": profit_follower
    }

def cartel_model(n_firms: int, a: float, b: float, c: float) -> Dict:
    """Modelo de Cartel"""
    Q = (a - c) / (2 * b)
    P = a - b * Q
    q_individual = Q / n_firms
    profit_total = (P - c) * Q
    profit_individual = profit_total / n_firms
    
    return {
        "Q_total": Q,
        "P_equilibrio": P,
        "q_individual": q_individual,
        "beneficio_total": profit_total,
        "beneficio_individual": profit_individual
    }

def perfect_competition_model(a: float, b: float, c: float) -> Dict:
    """Modelo de competencia perfecta"""
    P = c
    Q = (a - P) / b
    return {"P_equilibrio": P, "Q_total": Q}

def monopolistic_competition_model(n_firms: int, a: float, b: float, c: float, d: float) -> Dict:
    """Modelo de competencia monopolística"""
    P = (a + c) / 2
    q = (a - P) / (b * (1 + d))
    Q = n_firms * q
    return {"P_equilibrio": P, "q_individual": q, "Q_total": Q}

def monopoly_model(a: float, b: float, c: float) -> Dict:
    """Modelo de monopolio"""
    Q = (a - c) / (2 * b)
    P = a - b * Q
    profit = (P - c) * Q
    return {"Q_total": Q, "P_equilibrio": P, "beneficio": profit}

def main():
    st.title("Analizador de Estructuras de Mercado")
    
    uploaded_file = st.file_uploader("Cargar archivo DENUE (CSV)", type="csv")
    
    if uploaded_file is not None:
        # Leer archivo con codificación latin1
        df = pd.read_csv(uploaded_file, encoding='latin1')
        
        # Analizar todas las estructuras de mercado
        market_structures = analyze_all_market_structures(df)
        
        # Mostrar resumen de estructuras de mercado
        st.header("Resumen de Estructuras de Mercado")
        for structure, activities in market_structures.items():
            if activities:  # Solo mostrar estructuras que tengan actividades
                st.subheader(f"{structure} ({len(activities)} actividades)")
                for activity in activities:
                    st.write(f"- {activity}")
        
        # Seleccionar estructura de mercado
        available_structures = [struct for struct, acts in market_structures.items() if acts]
        selected_structure = st.selectbox(
            "Selecciona una estructura de mercado para analizar",
            available_structures
        )
        
        # Seleccionar actividad dentro de la estructura
        selected_activity = st.selectbox(
            "Selecciona la actividad económica",
            market_structures[selected_structure]
        )
        
        df_activity = df[df["Nombre de clase de la actividad"] == selected_activity]
        
        # Calcular métricas de mercado
        market_shares, cr4 = calculate_market_shares(df_activity)
        hhi = calculate_hhi(market_shares)
        n_firms = len(df_activity)
        
        # Mostrar métricas de mercado
        st.subheader("Métricas del Mercado")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Número de Empresas", n_firms)
        with col2:
            st.metric("HHI", f"{hhi:.2f}")
        with col3:
            st.metric("CR4", f"{cr4*100:.1f}%")
        with col4:
            st.metric("Estructura", selected_structure)
        
        # Mostrar empresas en esta actividad
        st.subheader("Empresas en esta Actividad")
        empresas_df = df_activity["Nombre de la Unidad Económica"].value_counts().reset_index()
        empresas_df.columns = ["Empresa", "Número de Unidades"]
        st.dataframe(empresas_df)
        
        # Parámetros del modelo
        st.subheader("Parámetros del Modelo")
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("Demanda máxima (a)", value=100.0)
        with col2:
            b = st.number_input("Pendiente demanda (b)", value=1.0)
        with col3:
            c = st.number_input("Costo marginal (c)", value=20.0)
        
        # Aplicar modelos según estructura
        st.subheader("Resultados del Modelo")
        
        if selected_structure == "Oligopolio":
            tabs = st.tabs(["Cournot", "Bertrand", "Stackelberg", "Cartel"])
            
            with tabs[0]:
                results = cournot_model(n_firms, a, b, c)
                st.write("### Modelo de Cournot")
                st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
                st.write(f"Cantidad total: {results['Q_total']:.2f}")
                st.write(f"Cantidad por empresa: {results['q_individual']:.2f}")
                st.write(f"Beneficio por empresa: ${results['beneficio_individual']:.2f}")
            
            with tabs[1]:
                results = bertrand_model(c)
                st.write("### Modelo de Bertrand")
                st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
                st.write(f"Beneficio por empresa: ${results['beneficio_individual']:.2f}")
            
            with tabs[2]:
                results = stackelberg_model(a, b, c)
                st.write("### Modelo de Stackelberg")
                st.write(f"Cantidad líder: {results['q_lider']:.2f}")
                st.write(f"Cantidad seguidor: {results['q_seguidor']:.2f}")
                st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
                st.write(f"Beneficio líder: ${results['beneficio_lider']:.2f}")
                st.write(f"Beneficio seguidor: ${results['beneficio_seguidor']:.2f}")
            
            with tabs[3]:
                results = cartel_model(n_firms, a, b, c)
                st.write("### Modelo de Cartel")
                st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
                st.write(f"Cantidad total: {results['Q_total']:.2f}")
                st.write(f"Cantidad por empresa: {results['q_individual']:.2f}")
                st.write(f"Beneficio total: ${results['beneficio_total']:.2f}")
                st.write(f"Beneficio por empresa: ${results['beneficio_individual']:.2f}")
        
        elif selected_structure == "Competencia Perfecta":
            results = perfect_competition_model(a, b, c)
            st.write("### Modelo de Competencia Perfecta")
            st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
            st.write(f"Cantidad total: {results['Q_total']:.2f}")
        
        elif selected_structure == "Competencia Monopolística":
            d = st.slider("Parámetro de diferenciación (d)", 0.0, 1.0, 0.5)
            results = monopolistic_competition_model(n_firms, a, b, c, d)
            st.write("### Modelo de Competencia Monopolística")
            st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
            st.write(f"Cantidad por empresa: {results['q_individual']:.2f}")
            st.write(f"Cantidad total: {results['Q_total']:.2f}")
        
        elif selected_structure == "Monopolio":
            results = monopoly_model(a, b, c)
            st.write("### Modelo de Monopolio")
            st.write(f"Precio de equilibrio: ${results['P_equilibrio']:.2f}")
            st.write(f"Cantidad total: {results['Q_total']:.2f}")
            st.write(f"Beneficio: ${results['beneficio']:.2f}")
        
        # Visualización de concentración
        st.subheader("Concentración del Mercado")
        
        # Calcular participaciones y agregar nombres únicos de empresas
        empresa_counts = df_activity["Nombre de la Unidad Económica"].value_counts()
        total_empresas = empresa_counts.sum()
        participaciones = (empresa_counts / total_empresas).reset_index()
        participaciones.columns = ["Empresa", "Participacion"]
        
        # Crear gráfico
        fig = go.Figure(data=[
            go.Bar(
                x=participaciones.index + 1,
                y=participaciones["Participacion"] * 100,
                hovertext=participaciones["Empresa"],
                hoverinfo="text+y",
                name="Participación de Mercado"
            )
        ])
        
        fig.update_layout(
            title="Distribución de Participaciones de Mercado",
            xaxis_title="Empresa (ordenadas por tamaño)",
            yaxis_title="Participación (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig)
        
# La parte del mapa que necesita corrección
        st.subheader("Distribución Geográfica del Mercado")
        
        # Crear un DataFrame con las coordenadas y participación
        map_data = df_activity.copy()
        map_data['Latitud'] = pd.to_numeric(map_data['Latitud'], errors='coerce')
        map_data['Longitud'] = pd.to_numeric(map_data['Longitud'], errors='coerce')
        
        # Calcular participación por empresa
        empresa_counts = map_data["Nombre de la Unidad Económica"].value_counts()
        total_empresas = empresa_counts.sum()
        empresa_shares = empresa_counts / total_empresas
        
        map_data['Participacion'] = map_data['Nombre de la Unidad Económica'].map(empresa_shares)
        map_data = map_data.dropna(subset=['Latitud', 'Longitud'])
        
        # Crear figura del mapa
        fig_map = go.Figure()
        
        # Añadir los puntos al mapa
        fig_map.add_trace(go.Scattermapbox(
            lat=map_data['Latitud'],
            lon=map_data['Longitud'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                color=map_data['Participacion'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title='Participación de Mercado',
                    titleside='right')
            ),
            text=map_data.apply(
                lambda row: f"Empresa: {row['Nombre de la Unidad Económica']}<br>" +
                          f"Participación: {row['Participacion']*100:.2f}%<br>" +
                          f"Dirección: {row['Nombre de la vialidad']} {row['Número exterior o kilómetro']}", 
                axis=1
            ),
            hoverinfo='text'
        ))

        # Actualizar el diseño del mapa
        fig_map.update_layout(
            mapbox_style="carto-positron",
            mapbox=dict(
                center=dict(
                    lat=map_data['Latitud'].mean(),
                    lon=map_data['Longitud'].mean()
                ),
                zoom=10
            ),
            height=600,
            margin=dict(l=0, r=0, t=30, b=0),
            title="Distribución Geográfica de Empresas por Participación de Mercado"
        )

        # Mostrar el mapa
        st.plotly_chart(fig_map)

if __name__ == "__main__":
    main()