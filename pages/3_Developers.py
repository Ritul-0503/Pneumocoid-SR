
import streamlit as st
from utils import inject_custom_css

st.set_page_config(page_title="Developers - PNEUMOCOID-SR", page_icon="🫁", layout="wide")
inject_custom_css()

st.markdown("<div class='app-title' style='font-size:2rem;'>About the Developers</div>", unsafe_allow_html=True)
st.divider()

st.write("PNEUMOCOID-SR was developed by the following team:")
st.write("")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Developer 1")
    st.markdown("""
    **Rits**

    Intern, AI in Drug Discovery Internship Program 2026
    Indian Institute of Technology (BHU), Varanasi

    Dept. of Pharmaceutical Engineering & Technology
    Under the supervision of Dr. Rajnish Kumar

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

st.divider()
st.subheader("Acknowledgment")
st.write("""
This project was developed as part of the **AI in Drug Discovery Internship Program 2026** at
IIT (BHU) Varanasi, under the guidance of **Dr. Rajnish Kumar**, Dept. of Pharmaceutical
Engineering & Technology.
""")
st.caption("PNEUMOCOID-SR - Pulmonary Toxicity Prediction System")
