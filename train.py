import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Force include root directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import config

print("Training Machine Learning Pipeline...")

if not os.path.exists(config.RAW_DATA_PATH):
    # Fallback to Downloads if CC GENERAL.csv is there
    fallback_path = r"C:\Users\Pathan Safeenkhan\Downloads\CC GENERAL.csv"
    if os.path.exists(fallback_path):
        import shutil
        shutil.copy(fallback_path, config.RAW_DATA_PATH)
    else:
        raise FileNotFoundError(f"Place 'CC GENERAL.csv' into {config.BASE_DIR}")

df = pd.read_csv(config.RAW_DATA_PATH)
df_clean = df.drop(columns=["CUST_ID"], errors="ignore")
df_clean["MINIMUM_PAYMENTS"] = df_clean["MINIMUM_PAYMENTS"].fillna(df_clean["MINIMUM_PAYMENTS"].median())
df_clean["CREDIT_LIMIT"] = df_clean["CREDIT_LIMIT"].fillna(df_clean["CREDIT_LIMIT"].median())

df_log = np.log1p(df_clean)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_log)

pca = PCA(n_components=3, random_state=42)
X_pca = pca.fit_transform(X_scaled)

kmeans = KMeans(n_clusters=4, init="k-means++", random_state=42, n_init=10)
df_clean["Cluster"] = kmeans.fit_predict(X_pca)

joblib.dump(scaler, config.SCALER_PATH)
joblib.dump(pca, config.PCA_PATH)
joblib.dump(kmeans, config.KMEANS_PATH)
df_clean.to_csv(config.DATASET_PATH, index=False)

print("Pipeline artifacts successfully saved to C:\\CreditCard_AI_Project.")