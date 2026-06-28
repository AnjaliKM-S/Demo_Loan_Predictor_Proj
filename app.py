import os
import joblib
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Loan Prediction App", page_icon="💰", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")

if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please place the trained model at models/model.pkl")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None

feature_order = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Total_Income",
    "Property_Area_Semiurban",
    "Property_Area_Urban",
]

st.title("Loan Approval Prediction")
st.write("Enter the applicant details to estimate whether the loan is likely to be approved.")

with st.sidebar:
    st.header("Applicant Information")

    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self_Employed", ["No", "Yes"])
    applicant_income = st.number_input("Applicant Income", min_value=0, step=1000)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0, step=1000)
    loan_amount = st.number_input("Loan Amount", min_value=0, step=1000)
    loan_amount_term = st.number_input("Loan Amount Term", min_value=0, step=12)
    credit_history = st.selectbox("Credit History", [0, 1])
    property_area = st.selectbox("Property Area", ["Urban", "Rural", "Semiurban"])

if st.button("Predict Loan Status"):
    try:
        data = {
            "Gender": gender,
            "Married": married,
            "Dependents": dependents,
            "Education": education,
            "Self_Employed": self_employed,
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_amount_term,
            "Credit_History": credit_history,
            "Total_Income": applicant_income + coapplicant_income,
        }

        input_df = pd.DataFrame([data])

        if os.path.exists(DATASET_PATH):
            training_df = pd.read_csv(DATASET_PATH)
            categorical_cols = ["Gender", "Married", "Dependents", "Education", "Self_Employed"]
            encoders = {}
            for col in categorical_cols:
                encoder = LabelEncoder()
                encoder.fit(training_df[col].astype(str))
                encoders[col] = encoder
                input_df[col] = encoders[col].transform(input_df[col].astype(str))
        else:
            for col in ["Gender", "Married", "Dependents", "Education", "Self_Employed"]:
                input_df[col] = input_df[col].astype(str)
                input_df[col] = LabelEncoder().fit_transform(input_df[col])

        property_dummies = pd.DataFrame(
            {
                "Property_Area_Semiurban": [0],
                "Property_Area_Urban": [0],
            }
        )
        if property_area == "Semiurban":
            property_dummies["Property_Area_Semiurban"] = 1
        elif property_area == "Urban":
            property_dummies["Property_Area_Urban"] = 1

        input_df = pd.concat([input_df, property_dummies], axis=1)

        for col in feature_order:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[feature_order]

        if scaler is not None:
            input_scaled = scaler.transform(input_df)
            prediction = model.predict(input_scaled)[0]
        else:
            prediction = model.predict(input_df)[0]

        st.success(f"Predicted Loan Status: {prediction}")
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
