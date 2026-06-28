# ML Deployment Prompt (VS Code)

I have already completed the Machine Learning part of this project in Google Colab.

## Current Status

* Dataset cleaning and preprocessing completed.
* Exploratory Data Analysis (EDA) completed.
* Feature engineering completed.
* Missing values, outliers, encoding, and scaling handled wherever required.
* Model training and evaluation completed.
* Trained model saved using `joblib`.
* The training Python file has been copied into the `notebooks` folder.
* Generate only the deployment part of the project.

---

## Your Task

Do NOT retrain the model.

Do NOT modify preprocessing.

Do NOT recreate EDA.

Read the Python training file inside the `notebooks` folder and reuse the exact preprocessing, feature names, encoding, scaling (if used), target variable, and feature order from that file.

Generate the following files only:

* `app.py`
* `requirements.txt`
* `README.md`

---

# Mandatory Project Structure

Create the project EXACTLY in the following structure.

```text
project-root/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── dataset.csv
│
├── models/
│   ├── model.pkl
│   └── scaler.pkl          (only if scaling was used)
│
└── notebooks/
    └── training_file.py
```

Rules:

* Store the trained model inside the `models` folder as `model.pkl`.
* Store `scaler.pkl` inside the `models` folder if scaling was used.
* Store the complete training Python file inside the `notebooks` folder.
* Never keep `.pkl` files in the project root.
* Never keep the training Python file in the project root.
* Update the application so it always loads:

```python
models/model.pkl
```

If scaling was used, load:

```python
models/scaler.pkl
```

---

# Streamlit Application Requirements

Generate a professional Streamlit application that:

* Loads the trained model from `models/model.pkl`.
* Loads `models/scaler.pkl` only if scaling was used.
* Reads the training Python file from the `notebooks` folder.
* Reuses the exact preprocessing logic used during training.
* Uses the exact feature names and feature order used during model training.
* Uses:

  * `st.number_input()` for numerical features.
  * `st.selectbox()` for categorical features.
* Applies label encoding or one-hot encoding exactly as used during training.
* Creates the prediction DataFrame with the exact columns expected by the model.
* Handles invalid inputs gracefully.
* Displays prediction in a clean, professional UI.
* Includes:

  * Page title
  * Sidebar
  * Proper spacing
  * Prediction button
  * Success/Error messages

---

# requirements.txt

Generate a `requirements.txt` containing only the required libraries.

---

# README.md

Generate a simple README containing:

* Project description
* Folder structure
* Installation steps
* Virtual environment creation
* How to run the Streamlit application

---

# Running Instructions

Provide the following commands:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

# Validation Checklist

Before generating the files, ensure:

* Model path is correct.
* Scaler path is correct (if used).
* Feature names exactly match the training code.
* Feature order exactly matches the training code.
* Encoding exactly matches the training code.
* Scaling exactly matches the training code.
* Prediction DataFrame matches the training features.
* No feature mismatch errors.
* No missing imports.
* The application runs successfully.

---

# Important Rules

* Do NOT retrain the model.
* Do NOT modify preprocessing.
* Do NOT generate EDA.
* Do NOT ask for confirmation.
* Do NOT explain your reasoning.
* Generate the required files directly.
* Keep comments minimal and meaningful.
* Produce clean, professional, interview-ready Python code.
* Reuse everything from the training Python file to ensure the Streamlit application behaves exactly like the trained model.

===============================
Open prompt.md and ask Copilot Agent:

"Generate the remaining deployment files according to prompt.md."
==========================================

==================================================
For the fastest results during your machine test:

Copy your Colab code into notebooks/training_file.py.
Save model.pkl (and scaler.pkl if used) in the models folder.
Open the project in VS Code.