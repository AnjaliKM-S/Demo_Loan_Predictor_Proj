# Loan Prediction App

This project provides a Streamlit web app for predicting loan approval status using a trained machine learning model.

## Project Structure

```text
project-root/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── dataset.csv
├── models/
│   ├── model.pkl
│   └── scaler.pkl
└── notebooks/
    └── training_file.py
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```
