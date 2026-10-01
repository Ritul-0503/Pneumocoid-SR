
import os
import streamlit as st
from utils import inject_custom_css, show_disclaimer, render_header, BASE_DIR

st.set_page_config(page_title="Developers - PNEUMOCOID-SR", page_icon="assets/favicon.png", layout="wide")
inject_custom_css()
render_header("About the Developers")

st.write("PNEUMOCOID-SR was developed by the following team:")
st.write("")

def developer_card(photo_file, name, qualification, bio_markdown, github_url, github_label, linkedin_url=None):
    photo_col, intro_col = st.columns([1, 2], vertical_alignment="center")
    with photo_col:
        p = os.path.join(BASE_DIR, "assets", photo_file)
        if os.path.exists(p):
            st.markdown(f"<div style='text-align: center;'>", unsafe_allow_html=True)
            st.image(p, width=170)
            st.markdown(f"</div>", unsafe_allow_html=True)
    with intro_col:
        st.markdown(f"""
#### {name}
**{qualification}**
""")
    st.markdown(bio_markdown)
    links = f"**GitHub:** [{github_label}]({github_url})"
    if linkedin_url:
        links += f"  |  **LinkedIn:** [Profile]({linkedin_url})"
    else:
        links += "  |  **LinkedIn:** [Add link]()"
    st.markdown(links)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Project Head")
    developer_card(
        photo_file="developer1.png",
        name="Ritul Kumari",
        qualification="Bachelor of Pharmacy",
        bio_markdown="""
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
""",
        github_url="https://github.com/Ritul-0503", github_label="Ritul-0503",
        linkedin_url="https://www.linkedin.com/in/ritul-sharma-95885b368/?isSelfProfile=true"
    )

with row1_col2:
    st.subheader("Project Head")
    developer_card(
        photo_file="developer2.png",
        name="Sneha Kumari",
        qualification="Bachelor of Pharmacy",
        bio_markdown="""
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
""",
        github_url="https://github.com/Sneha-465", github_label="Sneha-465",
        linkedin_url="https://www.linkedin.com/in/sneha-kumari-b02284360/?isSelfProfile=false"
    )

st.write("")
row2_spacer1, row2_col, row2_spacer2 = st.columns([1, 2, 1])
with row2_col:
    st.subheader("Developer")
    developer_card(
        photo_file="developer3.png",
        name="Utkarsh Kumar",
        qualification="AI in Drug Discovery Intern, IIT (BHU) Varanasi",
        bio_markdown="""
Utkarsh completed his **Bachelor of Pharmacy in 2026** and went on to complete a **research
internship at IIT (BHU) Varanasi**, focused on AI in Drug Discovery.

He has also completed an **Executive Diploma in Pharmacovigilance**, an **Executive Diploma in
Medical Writing**, an **Industrial Internship in Clinical Research**, an **Executive Diploma in
Clinical Data Management**, a **Diploma in Regulatory Affairs**, and an **Advanced Diploma in
Computer Applications**.

He has previously worked on developing a **hepatotoxicity (DILI) prediction model** and a
**P2X7 receptor activity prediction model**, and is currently developing **cardiotoxicity
prediction models** using machine learning and cheminformatics - combining a pharmaceutical
sciences background with applied AI to build tools for early-stage drug safety and activity
screening. **CardioTriad-UR** is his latest project, predicting ion-channel-mediated
cardiotoxicity risk from molecular structure.
""",
        github_url="https://github.com/Utkarsh-1417", github_label="Utkarsh-1417",
        linkedin_url="https://www.linkedin.com/in/utkarsh-kumar-962046330/?isSelfProfile=false"
    )

show_disclaimer()
st.caption("PNEUMOCOID-SR - Pulmonary Toxicity Prediction System")
