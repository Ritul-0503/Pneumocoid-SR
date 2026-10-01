
import os
import streamlit as st
from utils import inject_custom_css, show_disclaimer, render_header, BASE_DIR

st.set_page_config(page_title="Developers - PNEUMOCOID-SR", page_icon="assets/favicon.png", layout="wide")
inject_custom_css()
render_header("About the Developers")

st.write("PNEUMOCOID-SR was developed by the following team:")
st.write("")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Developer 1")
    photo_col, intro_col = st.columns([1, 2], vertical_alignment="center")
    with photo_col:
        p = os.path.join(BASE_DIR, "assets", "developer1.png")
        if os.path.exists(p):
            st.image(p, width=170)
    with intro_col:
        st.markdown("""
#### Ritul Kumari
**Bachelor of Pharmacy**
""")
    st.markdown("""
Ritul Kumari is a Bachelor of Pharmacy graduate with a focus on AI-driven drug discovery,
computational toxicology, and pharmaceutical research. During her **Research Internship at
IIT (BHU), Varanasi**, she has worked on applying machine learning and cheminformatics
approaches to drug safety and activity prediction.

Her professional training includes **Executive Diplomas in Pharmacovigilance, Medical Writing,
and Clinical Data Management**, and a **Diploma in Regulatory Affairs**. She has also gained
practical exposure through an **Industrial internship in clinical research** and has taken part
in a **Workshop on molecular docking and drug discovery**.

Her research experience includes **P2X7 receptor activity prediction** using computational
approaches. Her current project, **PNEUMOCOID-SR**, is a machine learning model that predicts
pulmonary toxicity from molecular structure-derived features, supporting early toxicity screening.

**GitHub:** [Ritul-0503](https://github.com/Ritul-0503)  |  **LinkedIn:** [Ritul Sharma](https://www.linkedin.com/in/ritul-sharma-95885b368/?isSelfProfile=true)
""")

with col2:
    st.subheader("Developer 2")
    photo_col2, intro_col2 = st.columns([1, 2], vertical_alignment="center")
    with photo_col2:
        p2 = os.path.join(BASE_DIR, "assets", "developer2.png")
        if os.path.exists(p2):
            st.image(p2, width=170)
    with intro_col2:
        st.markdown("""
#### Sneha Kumari
**Bachelor of Pharmacy**
""")
    st.markdown("""
She is a pharmacy graduate with an interest in drug safety, pharmacovigilance, clinical
research, Digital Therapeutics, and AI-driven drug discovery.

Her additional professional training includes an **Executive Diploma in Pharmacovigilance**,
an **Executive Diploma in Medical Writing**, an **Executive Certificate Course in Clinical Data
Management**, an **Executive Certificate Course in Digital Therapeutics**, and an **Industrial
Internship in Clinical Research**, along with NPTEL certifications in **Artificial Intelligence
in Drug Discovery and Development** and **Clinical Trial Regulatory Requirements in India**.

Her current work focuses on applying machine learning and cheminformatics to toxicity
prediction. This pulmonary toxicity prediction model is developed to support early-stage drug
safety screening by predicting potential pulmonary toxicity from chemical structure.

**GitHub:** [Sneha-465](https://github.com/Sneha-465)  |  **LinkedIn:** [Sneha Kumari](https://www.linkedin.com/in/sneha-kumari-b02284360/?isSelfProfile=false)
""")

show_disclaimer()
st.caption("PNEUMOCOID-SR - Pulmonary Toxicity Prediction System")
