import joblib
import numpy as np
import pandas as pd
import config

def load_all_artifacts():
    scaler = joblib.load(config.SCALER_PATH)
    pca = joblib.load(config.PCA_PATH)
    kmeans = joblib.load(config.KMEANS_PATH)
    df_segmented = pd.read_csv(config.DATASET_PATH)
    return scaler, pca, kmeans, df_segmented

def predict_single_customer(input_df: pd.DataFrame, scaler, pca, kmeans) -> int:
    log_data = np.log1p(input_df)
    scaled_data = scaler.transform(log_data)
    pca_data = pca.transform(scaled_data)
    return int(kmeans.predict(pca_data)[0])

def predict_batch_customers(df: pd.DataFrame, scaler, pca, kmeans) -> pd.DataFrame:
    clean_df = df.drop(columns=["CUST_ID"], errors="ignore").fillna(df.median(numeric_only=True))
    log_data = np.log1p(clean_df)
    scaled_data = scaler.transform(log_data)
    pca_data = pca.transform(scaled_data)
    
    df["Assigned_Cluster"] = kmeans.predict(pca_data)
    cluster_names = {cid: data["name"] for cid, data in config.PERSONAS.items()}
    df["Segment_Name"] = df["Assigned_Cluster"].map(cluster_names)
    return df
