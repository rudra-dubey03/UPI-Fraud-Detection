
import streamlit as st
import pandas as pd
import joblib

# Load our trained model
model = joblib.load("upi_fraud_model.pkl")

# Page configuration
st.set_page_config(
    page_title="UPI Fraud Detection",
    page_icon="🔐"
)

# Heading
st.title("UPI Fraud Detection System")
st.write("Detect suspicious UPI transactions using Machine Learning.")

st.divider()

# Transaction details
st.header("Enter Transaction Details")

amount = st.number_input(
    "Transaction Amount (₹)",
    min_value=1.0,
    value=1000.0
)

account_age = st.number_input(
    "Account Age (Days)",
    min_value=1,
    value=365
)

transactions = st.number_input(
    "Transactions in Last 24 Hours",
    min_value=0,
    value=2
)

new_device = st.selectbox(
    "Is this a New Device?",
    ["No", "Yes"]
)

failed_attempts = st.number_input(
    "Failed Attempts in Last 24 Hours",
    min_value=0,
    value=0
)

hour = st.slider(
    "Transaction Hour",
    0, 23, 12
)

# Detect fraud
if st.button("Detect Fraud"):

    input_data = pd.DataFrame([[
        amount,
        account_age,
        transactions,
        1 if new_device == "Yes" else 0,
        failed_attempts,
        hour
    ]], columns=[
        'amount_inr',
        'sender_account_age_days',
        'transactions_last_24h',
        'is_new_device',
        'failed_attempts_last_24h',
        'transaction_hour'
    ])

    # Model prediction
    prediction = model.predict(input_data)

    if prediction[0] == -1:
        st.error("Suspicious Transaction Detected!")
    else:
        st.success("Normal Transaction!")
