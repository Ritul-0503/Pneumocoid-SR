
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

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

def inject_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #F4FAFC; }
        header[data-testid="stHeader"] { background: transparent; }
        .app-title { color: #000000; font-size: 2.6rem; font-weight: 800; text-align: left; margin: 0; line-height: 1.15; }
        .app-subtitle { color: #587080; text-align: left; font-size: 1.05rem; margin: 0.15rem 0 0 0; }
        .brand-bar { height: 4px; border-radius: 4px; margin: 0.75rem 0 1.5rem 0;
                     background: linear-gradient(90deg, #006D77, #087EA4, #38BDF8, #19B5A5); }
        h1, h2, h3, h4 { color: #123047; text-align: left; }
        .stMarkdown a { color: #087EA4; }
        section[data-testid="stSidebar"] { border-right: 1px solid #D8EEF0; }
        .stButton>button, .stDownloadButton>button {
            background-color: #006D77; color: #FFFFFF; border: none; border-radius: 8px; }
        .stButton>button p, .stDownloadButton>button p { color: #FFFFFF; }
        .stButton>button:hover, .stDownloadButton>button:hover { background-color: #087EA4; color: #FFFFFF; }
        [data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #D8EEF0; border-radius: 12px; padding: 12px 16px; }
        div[data-baseweb="input"] { border: 1px solid #D8EEF0; border-radius: 8px; background: #FFFFFF; }
        [data-testid="stDataFrame"] { border: 1px solid #D8EEF0; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle=None):
    logo_col, text_col = st.columns([1, 5], vertical_alignment="center")
    with logo_col:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=150)
    with text_col:
        st.markdown(f"<div class='app-title'>{title}</div>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<div class='app-subtitle'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-bar'></div>", unsafe_allow_html=True)

def show_disclaimer():
    st.divider()
    st.subheader("Disclaimer")
    st.warning(
        "PNEUMOCOID-SR is a research and educational tool. Its predictions are computational "
        "estimates from a machine learning model and have not been validated for clinical, "
        "regulatory, or safety-assessment decisions. They are not medical advice and do not "
        "replace experimental testing or expert toxicological evaluation. Predictions for "
        "compounds outside the applicability domain are less reliable, and the model can "
        "misclassify some compounds, particularly small or structurally unusual molecules."
    )
