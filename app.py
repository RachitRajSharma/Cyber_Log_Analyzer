import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Network Log Analyzer", layout="wide")

st.title("📊 Network Log Analyzer")

uploaded_file = st.file_uploader("Upload Network Log CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Logs")
    st.dataframe(df)

    # Basic stats
    st.subheader("📈 Summary Stats")
    st.write(df.describe(include='all'))

    # Anomaly Detection
    st.subheader("🚨 Anomaly Detection (Isolation Forest)")

    # Select features to analyze
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if len(numeric_features) >= 2:
        selected_features = st.multiselect("Select numeric features", numeric_features, default=numeric_features[:2])

        if selected_features:
            model = IsolationForest(contamination=0.1, random_state=42)
            df['anomaly'] = model.fit_predict(df[selected_features])

            st.success("Anomalies marked as -1")

            anomalies = df[df['anomaly'] == -1]
            st.write("🔴 Suspicious Entries Detected:", anomalies.shape[0])
            st.dataframe(anomalies)

            st.download_button("Download Anomalies CSV", anomalies.to_csv(index=False), file_name="anomalies.csv")
    else:
        st.warning("No numeric features available for anomaly detection.")
