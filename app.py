import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

MODEL_PATH = Path("models/model.pkl")
SCALER_PATH = Path("models/scaler.pkl")

FEATURE_ORDER = [
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

LABEL_ENCODINGS = {
    "Gender": {"Female": 0, "Male": 1},
    "Married": {"No": 0, "Yes": 1},
    "Dependents": {"0": 0, "1": 1, "2": 2, "3+": 3},
    "Education": {"Graduate": 0, "Not Graduate": 1},
    "Self_Employed": {"No": 0, "Yes": 1},
}

PROPERTY_AREAS = ["Rural", "Semiurban", "Urban"]
CREDIT_HISTORY_OPTIONS = ["1.0", "0.0"]


def load_artifacts():
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Required artifacts are missing. Expected {MODEL_PATH} and {SCALER_PATH}."
        )

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def build_feature_vector(user_inputs: dict) -> pd.DataFrame:
    encoded = {
        "Gender": LABEL_ENCODINGS["Gender"][user_inputs["Gender"]],
        "Married": LABEL_ENCODINGS["Married"][user_inputs["Married"]],
        "Dependents": LABEL_ENCODINGS["Dependents"][user_inputs["Dependents"]],
        "Education": LABEL_ENCODINGS["Education"][user_inputs["Education"]],
        "Self_Employed": LABEL_ENCODINGS["Self_Employed"][user_inputs["Self_Employed"]],
        "ApplicantIncome": float(user_inputs["ApplicantIncome"]),
        "CoapplicantIncome": float(user_inputs["CoapplicantIncome"]),
        "LoanAmount": float(user_inputs["LoanAmount"]),
        "Loan_Amount_Term": float(user_inputs["Loan_Amount_Term"]),
        "Credit_History": float(user_inputs["Credit_History"]),
    }

    encoded["Total_Income"] = encoded["ApplicantIncome"] + encoded["CoapplicantIncome"]
    encoded["Property_Area_Semiurban"] = 1 if user_inputs["Property_Area"] == "Semiurban" else 0
    encoded["Property_Area_Urban"] = 1 if user_inputs["Property_Area"] == "Urban" else 0

    return pd.DataFrame([encoded], columns=FEATURE_ORDER)


def predict_loan_status(model, scaler, feature_df: pd.DataFrame) -> tuple[str, float]:
    scaled_features = scaler.transform(feature_df)
    prediction = model.predict(scaled_features)[0]

    probability = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(scaled_features)[0]
            classes = list(model.classes_)
            if "Y" in classes:
                probability = float(proba[classes.index("Y")])
            else:
                probability = float(proba.max())
        except Exception:
            probability = None

    status = "Approved" if str(prediction) == "Y" else "Not Approved"
    return status, probability


def main():
    st.set_page_config(
        page_title="Loan Approval Predictor",
        page_icon="💰",
        layout="centered",
    )

    st.title("Loan Approval Prediction")
    st.write(
        "Enter the applicant details below to get a quick loan approval prediction. "
        "This app reproduces the exact preprocessing and feature order used during model training."
    )

    with st.sidebar:
        st.header("Applicant Inputs")
        st.markdown(
            "Use the form controls to provide all required fields. "
            "The prediction is based on a pretrained classification model." 
        )
        st.caption("Loan status is predicted as Approved or Not Approved.")

    try:
        model, scaler = load_artifacts()
    except FileNotFoundError as error:
        st.error(error)
        st.stop()
    except Exception as error:
        st.error("Unable to load model artifacts. Please check the files in the models folder.")
        st.stop()

    with st.form(key="loan_form"):
        gender = st.selectbox("Gender", options=["Female", "Male"])
        married = st.selectbox("Married", options=["No", "Yes"])
        dependents = st.selectbox("Dependents", options=["0", "1", "2", "3+"])
        education = st.selectbox("Education", options=["Graduate", "Not Graduate"])
        self_employed = st.selectbox("Self Employed", options=["No", "Yes"])

        applicant_income = st.number_input(
            "Applicant Income", min_value=0.0, value=2500.0, step=100.0, format="%.2f"
        )
        coapplicant_income = st.number_input(
            "Coapplicant Income", min_value=0.0, value=0.0, step=100.0, format="%.2f"
        )
        loan_amount = st.number_input(
            "Loan Amount (in thousands)", min_value=0.0, value=120.0, step=10.0, format="%.2f"
        )
        loan_term = st.number_input(
            "Loan Amount Term (days)", min_value=0.0, value=360.0, step=12.0, format="%.0f"
        )
        credit_history = st.selectbox("Credit History", options=CREDIT_HISTORY_OPTIONS)
        property_area = st.selectbox("Property Area", options=PROPERTY_AREAS)

        submit_button = st.form_submit_button("Predict Loan Status")

    if submit_button:
        if loan_amount <= 0 or loan_term <= 0:
            st.error("Loan amount and term must be positive numbers.")
        else:
            user_inputs = {
                "Gender": gender,
                "Married": married,
                "Dependents": dependents,
                "Education": education,
                "Self_Employed": self_employed,
                "ApplicantIncome": applicant_income,
                "CoapplicantIncome": coapplicant_income,
                "LoanAmount": loan_amount,
                "Loan_Amount_Term": loan_term,
                "Credit_History": credit_history,
                "Property_Area": property_area,
            }
            feature_df = build_feature_vector(user_inputs)

            try:
                status, proba = predict_loan_status(model, scaler, feature_df)
                st.subheader("Prediction Result")
                if status == "Approved":
                    st.success(f"Loan Status: {status}")
                else:
                    st.error(f"Loan Status: {status}")

                if proba is not None:
                    st.write(f"Approval probability: {proba:.1%}")

                with st.expander("View processed input features"):
                    st.table(feature_df.T.rename(columns={0: "Value"}))
            except Exception as error:
                st.error("Prediction failed. Please verify the input values and model files.")
                st.exception(error)

    st.markdown("---")
    st.markdown(
        "### Notes\n"
        "- This app uses the exact feature order and preprocessing steps from the original training pipeline.\n"
        "- Categorical values are encoded with the same label mapping as training.\n"
        "- Property Area uses one-hot encoding with the same dropped column logic."
    )


if __name__ == "__main__":
    main()
