import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Artifact & Asset Paths
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
PCA_PATH = os.path.join(BASE_DIR, "pca.pkl")
KMEANS_PATH = os.path.join(BASE_DIR, "kmeans_model.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "segmented_customers.csv")
RAW_DATA_PATH = os.path.join(BASE_DIR, "CC GENERAL.csv")
CSS_PATH = os.path.join(BASE_DIR, "assets", "style.css")

# Feature Architecture
FEATURE_COLUMNS = [
    "BALANCE", "BALANCE_FREQUENCY", "PURCHASES", "ONEOFF_PURCHASES",
    "INSTALLMENTS_PURCHASES", "CASH_ADVANCE", "PURCHASES_FREQUENCY",
    "ONEOFF_PURCHASES_FREQUENCY", "PURCHASES_INSTALLMENTS_FREQUENCY",
    "CASH_ADVANCE_FREQUENCY", "CASH_ADVANCE_TRX", "PURCHASES_TRX",
    "CREDIT_LIMIT", "PAYMENTS", "MINIMUM_PAYMENTS", "PRC_FULL_PAYMENT", "TENURE"
]

# Business Persona Archetypes
PERSONAS = {
    0: {
        "name": "Installment Buyers & Regular Transactors",
        "badge_class": "badge-0",
        "badge_text": "Retail Installment Planner",
        "risk_score": 30,
        "behavior": "Consistent retail purchases converted into monthly EMI installments with steady repayment track records.",
        "strategy": "Offer 0% merchant EMI promotions, point-of-sale checkout discounts, and retail rewards.",
        "risk_desc": "Low Risk — regular cash flows and structured installments ensure portfolio stability."
    },
    1: {
        "name": "High Spenders & VIP Transactors",
        "badge_class": "badge-1",
        "badge_text": "High Value Prime Segment",
        "risk_score": 12,
        "behavior": "High-volume direct purchases, high credit limits, and full settlement of monthly balances.",
        "strategy": "Provide airport lounge access, concierge privileges, and proactive credit line expansions.",
        "risk_desc": "Minimal Risk — high liquidity and prime repayment capabilities."
    },
    2: {
        "name": "Revolvers / Cash-Advance Reliant",
        "badge_class": "badge-2",
        "badge_text": "High Borrowing & Cash Heavy",
        "risk_score": 85,
        "behavior": "Heavy dependence on cash advance withdrawals, low direct card transactions, and high revolving balances.",
        "strategy": "Promote lower-interest debt consolidation lines and implement cash-draw credit caps.",
        "risk_desc": "High Risk — elevated default vulnerability requiring ongoing risk monitoring."
    },
    3: {
        "name": "Low-Activity & Inactive Cardholders",
        "badge_class": "badge-3",
        "badge_text": "Dormant / Low Utilization",
        "risk_score": 42,
        "behavior": "Low account balances, minimal transaction frequency, and conservative overall card utilization.",
        "strategy": "Deploy lifecycle activation cashback vouchers and annual maintenance fee waivers.",
        "risk_desc": "Low Financial Risk, High Churn Risk — target with re-engagement incentives."
    }
}