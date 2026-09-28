
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
        photo_path = os.path.join(BASE_DIR, "assets", "developer1.png")
        if os.path.exists(photo_path):
            st.image(photo_path, width=170)
    with intro_col:
        st.markdown("""
#### Ritul Sharma
**Bachelor of Pharmacy (2026)**

Research Intern, AI in Drug Discovery Internship Program 2026

IIT (BHU), Varanasi - Dept. of Pharmaceutical Engineering & Technology

Under the supervision of Dr. Rajnish Kumar
""")
    st.markdown("""
Ritul Sharma is a Bachelor of Pharmacy graduate (2026) with a focus on AI-driven drug discovery,
computational toxicology, and pharmaceutical research. During her research internship at IIT (BHU),
Varanasi, she has worked on applying machine learning and cheminformatics approaches to drug
safety and activity prediction.

Alongside her B.Pharm, she has completed executive diplomas in Pharmacovigilance, Medical Writing,
and Clinical Data Management, and a Diploma in Regulatory Affairs. She has also gained practical
exposure through an industrial internship in clinical research and has taken part in workshops on
molecular docking and drug discovery.

Her research experience includes P2X7 receptor activity prediction using computational approaches.
Her current project, PNEUMOCOID-SR, is a machine learning model that predicts pulmonary toxicity
from molecular structure-derived features, supporting early toxicity screening.

**Role:** Machine learning pipeline development - data curation, featurization, model
training, validation, and applicability domain design

**GitHub:** [Ritul-0503](https://github.com/Ritul-0503)
""")

with col2:
    st.subheader("Developer 2")
    st.markdown("""
*[Name to be added]*

*[Affiliation to be added]*

**Role:** Web application development

*[Contact / GitHub link to be added]*
""")

show_disclaimer()
st.caption("PNEUMOCOID-SR - Pulmonary Toxicity Prediction System")
