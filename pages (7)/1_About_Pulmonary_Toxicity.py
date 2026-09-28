
import streamlit as st
from utils import inject_custom_css

st.set_page_config(page_title="About Pulmonary Toxicity - PNEUMOCOID-SR", page_icon="\U0001FAC1", layout="wide")
inject_custom_css()

st.markdown("<div class='app-title' style='font-size:2rem;'>About Pulmonary Toxicity</div>", unsafe_allow_html=True)
st.divider()

# ===== Section 1: The Respiratory System =====
st.header("The Respiratory System")
st.write("""
The respiratory system is responsible for one of the body"'s most essential functions: exchanging
oxygen and carbon dioxide between the air and the bloodstream. Air travels through the **nose and
mouth**, down the **trachea**, and branches into the **bronchi** and progressively smaller
**bronchioles**, finally reaching millions of tiny air sacs called **alveoli**.
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Key Structures")
    st.markdown("""
    - **Trachea** - the main airway carrying air to the lungs
    - **Bronchi & Bronchioles** - branching airways that distribute air within each lung
    - **Alveoli** - roughly 300-500 million tiny air sacs where gas exchange occurs
    - **Pulmonary capillaries** - tiny blood vessels wrapping around each alveolus
    - **Diaphragm** - the primary muscle driving breathing
    """)
with col2:
    st.subheader("Normal Lung Function")
    st.markdown("""
    - Oxygen from inhaled air diffuses across the thin alveolar walls into the blood
    - Carbon dioxide, a waste product, diffuses from blood into the alveoli to be exhaled
    - This exchange happens continuously, roughly 12-20 breaths per minute at rest
    - Healthy alveoli are thin, elastic, and have a huge surface area (roughly the size of a
      tennis court) to maximize gas exchange efficiency
    """)

st.divider()

# ===== Section 2: What is Pulmonary Toxicity =====
st.header("What is Pulmonary Toxicity?")
st.write("""
**Pulmonary toxicity** refers to damage or dysfunction of the lungs caused by exposure to a
harmful substance - this can be a drug, an industrial chemical, an environmental pollutant, or a
naturally occurring toxin. Because the lungs have such a large surface area directly exposed to
the outside environment (through breathing) and receive the body"'s entire blood supply with every
heartbeat, they are especially vulnerable to toxic injury from both inhaled and bloodborne agents.
""")

st.subheader("How Pulmonary Toxicity Affects the Body")
st.markdown("""
Toxic injury to the lungs can manifest in several distinct ways, depending on the agent, dose,
and duration of exposure:

- **Inflammation (Pneumonitis)** - the immune system reacts to the toxic insult, causing swelling
  and irritation of lung tissue, leading to coughing, shortness of breath, and chest discomfort
- **Pulmonary Fibrosis** - repeated or severe injury can trigger scarring of lung tissue, which
  stiffens the alveoli and permanently reduces their ability to exchange gases - this damage is
  often irreversible
- **Pulmonary Edema** - fluid leaks into the alveoli, effectively ""drowning"" the air sacs, and
  drastically reducing oxygen uptake
- **Oxidative Stress** - many toxicants generate reactive oxygen species inside lung cells,
  damaging cell membranes, proteins, and DNA, and triggering a cascade of inflammatory injury
- **Bronchoconstriction** - the airways themselves narrow in response to irritants, restricting
  airflow, as seen in occupational asthma or chemical exposure

Depending on severity, effects can range from mild, reversible irritation to chronic, irreversible
lung disease or acute respiratory failure requiring emergency medical intervention.
""")

st.divider()

# ===== Section 3: Common Causes =====
st.header("Common Causes of Pulmonary Toxicity")
tab1, tab2, tab3 = st.tabs(["Pharmaceutical", "Environmental / Occupational", "Other"])

with tab1:
    st.markdown("""
    - Certain chemotherapy drugs (e.g., bleomycin) are well-documented to cause pulmonary fibrosis
    - Some cardiovascular drugs (e.g., amiodarone) carry a known risk of chronic lung toxicity
      with long-term use
    - Adverse drug reactions affecting the lungs are a significant concern during drug development,
      since pulmonary toxicity can go undetected in early trials and only emerge after prolonged
      exposure
    """)
with tab2:
    st.markdown("""
    - Industrial chemicals and solvents (inhaled during occupational exposure)
    - Air pollutants such as particulate matter, ozone, and nitrogen oxides
    - Agricultural chemicals, including certain herbicides (e.g., paraquat, a well-known and severe
      pulmonary toxicant)
    - Asbestos and other mineral fibers, associated with long-term fibrotic lung disease
    """)
with tab3:
    st.markdown("""
    - Smoke inhalation (fires, tobacco, vaping-related lung injury)
    - Certain natural toxins and biological agents
    - Radiation-induced lung injury (e.g., following radiotherapy to the chest)
    """)

st.divider()

# ===== Section 4: Why It"'s a Challenge for Medical Science =====
st.header("Why Pulmonary Toxicity is a Challenge for Medical Science")
st.write("""
Pulmonary toxicity presents several distinct challenges that make it a persistent focus of
toxicology and drug safety research:
""")
st.markdown("""
- **Delayed onset** - toxic effects on the lungs, especially fibrosis, often don"'t appear until
  weeks, months, or even years after exposure, making early detection and attribution difficult
- **Irreversibility** - unlike some other tissues, damaged alveolar and fibrotic lung tissue often
  cannot regenerate, meaning prevention is far more valuable than treatment after the fact
- **Limited early biomarkers** - there are few reliable, early biological markers that can flag
  pulmonary toxicity before symptoms or structural damage become apparent
- **High cost of late discovery in drug development** - when a drug candidate"'s pulmonary
  toxicity is only discovered in late-stage clinical trials (or after approval), it represents a
  significant financial and patient-safety cost - this is a major reason computational prediction
  tools (like the one this application provides) are valuable early in the drug discovery pipeline
- **Compound diversity** - the sheer number and structural diversity of chemicals humans are
  exposed to (industrial, pharmaceutical, environmental) makes exhaustive experimental testing of
  every compound practically impossible, motivating machine learning-based prediction as a
  scalable screening tool
""")

st.info("""
This is precisely the gap that computational toxicity prediction aims to fill - by learning
patterns from known toxic and non-toxic compounds, machine learning models can flag potentially
harmful compounds early, before expensive and time-consuming experimental testing, helping
prioritize which compounds deserve closer safety scrutiny.
""")
