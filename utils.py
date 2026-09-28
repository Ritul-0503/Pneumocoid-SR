
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
from datetime import datetime
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Draw
from rdkit import RDLogger
RDLogger.DisableLog("rdApp.*")

PUBCHEM_URL = "https://pubchem.ncbi.nlm.nih.gov/"

@st.cache_resource
def load_artifacts():
    model = joblib.load("pulmonary_toxicity_model.pkl")
    ad_scaler = joblib.load("ad_scaler.pkl")
    ad_nn_model = joblib.load("ad_nn_model.pkl")
    with open("ad_metadata.json") as f:
        ad_metadata = json.load(f)
    with open("model_metadata.json") as f:
        model_metadata = json.load(f)
    return model, ad_scaler, ad_nn_model, ad_metadata, model_metadata

def featurize_smiles(smiles, radius=2, n_bits=1024):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    fp_array = np.array(fp)
    desc_values = []
    for name, func in Descriptors._descList:
        try:
            desc_values.append(func(mol))
        except Exception:
            desc_values.append(np.nan)
    desc_array = np.array(desc_values)
    desc_array[np.isinf(desc_array)] = np.nan
    desc_array = np.nan_to_num(desc_array, nan=0.0)
    features = np.hstack([fp_array, desc_array])
    return features, mol

def predict_with_ad(smiles, model, ad_scaler, ad_nn_model, ad_threshold, k=5):
    features, mol = featurize_smiles(smiles)
    if features is None:
        return None
    features = features.reshape(1, -1)
    pred_label = int(model.predict(features)[0])
    pred_proba = float(model.predict_proba(features)[0][1])
    features_scaled = ad_scaler.transform(features)
    distances, _ = ad_nn_model.kneighbors(features_scaled, n_neighbors=k)
    avg_distance = distances.mean()
    in_domain = bool(avg_distance <= ad_threshold)
    return {
        "smiles": smiles, "mol": mol,
        "predicted_label": "Toxic" if pred_label == 1 else "Non-toxic",
        "toxicity_probability": round(pred_proba, 4),
        "avg_distance_to_training": round(float(avg_distance), 4),
        "in_applicability_domain": in_domain,
        "reliability": "Reliable" if in_domain else "Caution - outside training domain"
    }

def add_to_history(result, source="Single Prediction"):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Source": source, "SMILES": result["smiles"],
        "Prediction": result["predicted_label"],
        "Toxicity Probability": result["toxicity_probability"],
        "In Applicability Domain": result["in_applicability_domain"]
    })

def generate_csv_report(df):
    return df.to_csv(index=False).encode("utf-8")

def generate_pdf_report(df, title="Pulmonary Toxicity Prediction Report"):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 77, 64)
    pdf.cell(0, 12, title, ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 9)
    col_widths = [55, 25, 30, 35, 35]
    headers = ["SMILES", "Prediction", "Probability", "In Domain", "Timestamp"]
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 8, h, border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 8)
    for _, row in df.iterrows():
        smiles_display = str(row.get("SMILES", ""))[:30]
        pdf.cell(col_widths[0], 8, smiles_display, border=1)
        pdf.cell(col_widths[1], 8, str(row.get("Prediction", "")), border=1)
        pdf.cell(col_widths[2], 8, str(row.get("Toxicity Probability", "")), border=1)
        pdf.cell(col_widths[3], 8, str(row.get("In Applicability Domain", "")), border=1)
        pdf.cell(col_widths[4], 8, str(row.get("Timestamp", "")), border=1)
        pdf.ln()
    return bytes(pdf.output())

def inject_custom_css():
    st.markdown("""
        <style>
        .app-title { color: #000000; font-size: 2.6rem; font-weight: 800; text-align: center; margin-bottom: 0px; }
        .app-subtitle { color: #004D40; text-align: center; font-size: 1.05rem; margin-top: 0px; margin-bottom: 1.5rem; }
        .stButton>button { background-color: #004D40; color: white; border-radius: 8px; border: none; }
        .stButton>button:hover { background-color: #00897B; color: white; }
        </style>
    """, unsafe_allow_html=True)
