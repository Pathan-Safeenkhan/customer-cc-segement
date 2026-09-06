import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_risk_gauge(score: int) -> go.Figure:
    color = "#38bdf8" if score < 40 else ("#facc15" if score < 70 else "#f87171")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Default Risk Score Index", 'font': {'size': 14, 'color': '#94a3b8'}},
        number={'font': {'color': '#f8fafc', 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#64748b'},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 35], 'color': "rgba(56, 189, 248, 0.12)"},
                {'range': [35, 70], 'color': "rgba(250, 204, 21, 0.12)"},
                {'range': [70, 100], 'color': "rgba(248, 113, 113, 0.12)"}
            ]
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_utilization_gauge(utilization: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=utilization,
        number={'suffix': "%", 'font': {'color': '#f8fafc', 'family': 'JetBrains Mono'}},
        title={'text': "Credit Line Utilization", 'font': {'size': 14, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#64748b'},
            'bar': {'color': '#818cf8'},
            'threshold': {'line': {'color': "#f87171", 'width': 3}, 'thickness': 0.75, 'value': 80}
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_radar_benchmark(user_vals: list, avg_vals: list, cluster_id: int) -> go.Figure:
    categories = ["Balance", "Purchases", "Cash Advance", "Credit Limit", "Payments"]
    max_vals = [max(u, a, 1.0) for u, a in zip(user_vals, avg_vals)]
    user_norm = [u / m * 100 for u, m in zip(user_vals, max_vals)]
    avg_norm = [a / m * 100 for a, m in zip(avg_vals, max_vals)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=user_norm, theta=categories, fill='toself', name='Active Customer', line_color='#38bdf8'))
    fig.add_trace(go.Scatterpolar(r=avg_norm, theta=categories, fill='toself', name=f'Cluster {cluster_id} Mean', line_color='#c084fc'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickcolor='#64748b')),
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        height=360,
        margin=dict(l=30, r=30, t=30, b=30)
    )
    return fig

def create_3d_pca_scatter(df_segmented, scaler, pca) -> go.Figure:
    sample = df_segmented.sample(min(2000, len(df_segmented)), random_state=42)
    clean_sample = sample.drop(columns=["CUST_ID", "Cluster"], errors="ignore").fillna(0)
    X_3d = pca.transform(scaler.transform(np.log1p(clean_sample)))

    plot_df = pd.DataFrame(X_3d[:, :3], columns=["PC1", "PC2", "PC3"])
    plot_df["Cluster"] = sample["Cluster"].values
    plot_df["Segment"] = plot_df["Cluster"].map({
        0: "Installment Buyers", 1: "High Spenders / VIP",
        2: "Cash-Advance Revolvers", 3: "Low Activity"
    })

    fig = px.scatter_3d(
        plot_df, x="PC1", y="PC2", z="PC3", color="Segment",
        opacity=0.75, size_max=4,
        color_discrete_sequence=['#38bdf8', '#facc15', '#f87171', '#94a3b8'],
        template="plotly_dark"
    )
    fig.update_layout(height=650, paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=30, b=10))
    return fig