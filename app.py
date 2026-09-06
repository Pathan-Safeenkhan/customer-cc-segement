import os
import sys
import streamlit as st  # type: ignore
import pandas as pd
import numpy as np

# Inject current directory into sys.path to guarantee imports work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
import ml_pipeline
import visualizations as viz
import plotly.express as px  # type: ignore

st.set_page_config(page_title="customer", page_icon="💳", layout="wide")

# Load CSS
if os.path.exists(config.CSS_PATH):
    with open(config.CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    scaler, pca, kmeans, df_segmented = ml_pipeline.load_all_artifacts()
except Exception as e:
    st.error(f"Artifacts missing or unreadable: {e}")
    st.info("Please run `python train.py` first to generate model artifacts.")
    st.stop()

# Header HTML
st.markdown("""
<div class="hud-header">
    <div class="hud-title">💳 customer credit card Segment // Enterprise Intelligence Suite</div>
    <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.3rem;">
        Unsupervised Machine Learning & Behavioral Segmentation Engine (PCA + K-Means)
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Navigation")
    mode = st.radio("Select View", [
        "Single Customer Inference",
        "What-If Strategy Simulator",
        "3D Cluster Space",
        "Batch Portfolio Scoring",
        "Portfolio EDA Matrix"
    ])
    st.markdown("---")
    st.markdown(f"**Target Clusters ($k$):** `4`")
    st.markdown(f"**Variance Explained:** `{pca.explained_variance_ratio_.sum() * 100:.1f}%`")
    st.markdown(f"**Indexed Records:** `{len(df_segmented):,}`")

# ----------------- VIEW 1: SINGLE CUSTOMER -----------------
if mode == "Single Customer Inference":
    col1, col2 = st.columns([1.1, 1.4], gap="large")
    with col1:
        st.markdown("#### 📝 Customer Profile Inputs")
        t1, t2, t3 = st.tabs(["Balances", "Purchases", "Payments & Advances"])
        with t1:
            bal = st.number_input("Balance ($)", 0.0, 50000.0, 2500.0, 100.0)
            limit = st.number_input("Credit Limit ($)", 100.0, 50000.0, 8000.0, 500.0)
            bal_freq = st.slider("Balance Frequency", 0.0, 1.0, 0.95)
            tenure = st.slider("Tenure (Months)", 6, 12, 12)
        with t2:
            pur = st.number_input("Total Purchases ($)", 0.0, 50000.0, 3200.0, 100.0)
            oneoff = st.number_input("One-off Purchases ($)", 0.0, 50000.0, 2000.0, 100.0)
            install = st.number_input("Installments ($)", 0.0, 50000.0, 1200.0, 100.0)
            pur_freq = st.slider("Purchase Frequency", 0.0, 1.0, 0.75)
            pur_trx = st.number_input("Purchase Transactions", 0, 400, 24)
        with t3:
            cash = st.number_input("Cash Advance ($)", 0.0, 50000.0, 0.0, 100.0)
            cash_freq = st.slider("Cash Advance Frequency", 0.0, 1.0, 0.0)
            cash_trx = st.number_input("Cash Advance Transactions", 0, 150, 0)
            pay = st.number_input("Payments ($)", 0.0, 50000.0, 2800.0, 100.0)
            min_pay = st.number_input("Minimum Payments ($)", 0.0, 50000.0, 300.0, 25.0)
            prc_full = st.slider("Full Payment Ratio", 0.0, 1.0, 0.40)

    with col2:
        input_data = pd.DataFrame([[
            bal, bal_freq, pur, oneoff, install, cash, pur_freq, 0.5, 0.5,
            cash_freq, cash_trx, pur_trx, limit, pay, min_pay, prc_full, float(tenure)
        ]], columns=config.FEATURE_COLUMNS)

        cluster_id = ml_pipeline.predict_single_customer(input_data, scaler, pca, kmeans)
        persona = config.PERSONAS[cluster_id]
        utilization = (bal / limit) * 100 if limit > 0 else 0.0

        st.markdown(f"""
        <div class="result-card">
            <div class="kpi-badge {persona['badge_class']}">{persona['badge_text']} &bull; Cluster {cluster_id}</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">{persona['name']}</div>
            <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.1); margin: 0.8rem 0;">
            <div class="hud-section-label">Behavioral Profile</div>
            <div class="hud-section-content">{persona['behavior']}</div>
            <div class="hud-section-label">Recommended Marketing Strategy</div>
            <div class="hud-section-content">{persona['strategy']}</div>
            <div class="hud-section-label">Portfolio Risk Assessment</div>
            <div class="hud-section-content">{persona['risk_desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(viz.create_risk_gauge(persona["risk_score"]), use_container_width=True)
        with g2:
            st.plotly_chart(viz.create_utilization_gauge(utilization), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🎯 Benchmark Radar vs. Cluster Average")
    cluster_avg = df_segmented[df_segmented["Cluster"] == cluster_id][["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS"]].mean()
    radar_fig = viz.create_radar_benchmark([bal, pur, cash, limit, pay], cluster_avg.values.tolist(), cluster_id)
    st.plotly_chart(radar_fig, use_container_width=True)

# ----------------- VIEW 2: WHAT-IF SIMULATOR -----------------
elif mode == "What-If Strategy Simulator":
    st.markdown("### 🧪 Behavioral Shift Simulator")
    s1, s2 = st.columns([1, 1], gap="large")
    with s1:
        base_bal = st.number_input("Base Balance ($)", value=2000.0, step=100.0)
        base_pur = st.number_input("Base Purchases ($)", value=1000.0, step=100.0)
        base_cash = st.number_input("Base Cash Advance ($)", value=1500.0, step=100.0)
        base_limit = st.number_input("Base Credit Limit ($)", value=4000.0, step=500.0)
        limit_adj = st.slider("Credit Line Boost (%)", -50, 100, 25)
        emi_conv = st.slider("Convert to Installments (%)", 0, 100, 50)
        cash_red = st.slider("Reduce Cash Draw (%)", 0, 100, 60)
    with s2:
        new_limit = base_limit * (1 + limit_adj / 100.0)
        new_cash = base_cash * (1 - cash_red / 100.0)
        new_install = base_pur * (emi_conv / 100.0)
        new_oneoff = base_pur - new_install
        
        def simulate(b, p, o, i, c, l):
            v = pd.DataFrame(np.zeros((1, 17)), columns=config.FEATURE_COLUMNS)
            v["BALANCE"], v["PURCHASES"], v["ONEOFF_PURCHASES"], v["INSTALLMENTS_PURCHASES"], v["CASH_ADVANCE"], v["CREDIT_LIMIT"] = b, p, o, i, c, l
            v["BALANCE_FREQUENCY"], v["PURCHASES_FREQUENCY"], v["PAYMENTS"], v["TENURE"] = 1.0, 0.6, p * 0.8, 12.0
            return ml_pipeline.predict_single_customer(v, scaler, pca, kmeans)
            
        c_before = simulate(base_bal, base_pur, base_pur*0.6, base_pur*0.4, base_cash, base_limit)
        c_after = simulate(base_bal, base_pur, new_oneoff, new_install, new_cash, new_limit)

        st.markdown(f"""
        <div class="result-card">
            <div style="font-size: 0.85rem; color: #94a3b8;">Original Segment:</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #f87171;">Cluster {c_before}: {config.PERSONAS[c_before]['name']}</div>
            <div style="font-size: 1.4rem; text-align: center; margin: 0.5rem 0;">⬇️ <i>Policy Intervention</i> ⬇️</div>
            <div style="font-size: 0.85rem; color: #94a3b8;">Projected Segment:</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #38bdf8;">Cluster {c_after}: {config.PERSONAS[c_after]['name']}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- VIEW 3: 3D CLUSTER SPACE -----------------
elif mode == "3D Cluster Space":
    st.markdown("### 🌌 3D PCA Manifold Space")
    st.plotly_chart(viz.create_3d_pca_scatter(df_segmented, scaler, pca), use_container_width=True)

# ----------------- VIEW 4: BATCH SCORING -----------------
elif mode == "Batch Portfolio Scoring":
    st.markdown("### 📂 Bulk Inference Pipeline")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file and st.button("⚡ Execute Batch Segmentation", type="primary"):
        batch_res = ml_pipeline.predict_batch_customers(pd.read_csv(file), scaler, pca, kmeans)
        st.success("Batch segmentation complete!")
        fig_dist = px.histogram(batch_res, x="Segment_Name", color="Segment_Name", template="plotly_dark")
        fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_dist, use_container_width=True)
        st.download_button("📥 Download Results", batch_res.to_csv(index=False).encode('utf-8'), "segmented_output.csv")

# ----------------- VIEW 5: PORTFOLIO EDA -----------------
elif mode == "Portfolio EDA Matrix":
    st.markdown("### 📈 Centroid Feature Matrix")
    st.dataframe(df_segmented.groupby("Cluster").mean().T.style.highlight_max(axis=1, color="#1e3a8a"), use_container_width=True)