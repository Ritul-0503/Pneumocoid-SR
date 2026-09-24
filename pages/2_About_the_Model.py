
import streamlit as st
from utils import load_artifacts, inject_custom_css

st.set_page_config(page_title="About the Model - PNEUMOCOID-SR", page_icon="🫁", layout="wide")
inject_custom_css()

model, ad_scaler, ad_nn_model, ad_metadata, model_metadata = load_artifacts()

st.markdown("<div class='app-title' style='font-size:2rem;'>About the Model</div>", unsafe_allow_html=True)
st.divider()

st.header("Model Overview")
st.write(f"""
PNEUMOCOID-SR uses an **{model_metadata.get("model_type", "ExtraTreesClassifier")}** - an ensemble
machine learning algorithm - to predict whether a chemical compound is likely to cause pulmonary
toxicity, based solely on its molecular structure (given as a SMILES string).
""")

st.subheader("Why ExtraTrees?")
st.markdown("""
ExtraTrees (Extremely Randomized Trees) builds a large collection of decision trees, where each
tree is trained with an added layer of randomness in how it chooses split points. This makes
ExtraTrees less prone to overfitting than a standard Random Forest, especially on high-dimensional,
sparse data like molecular fingerprints. During development, ExtraTrees was compared directly
against several other algorithms (Random Forest, XGBoost, LightGBM, CatBoost, SVM, Logistic
Regression, K-Nearest Neighbors, and ensemble/stacking approaches) on the same dataset and
features, and consistently came out on top on the metrics that matter most for this task.
""")

st.divider()
st.header("How the Model 'Sees' a Molecule")
st.write("""
A chemical structure first has to be converted into a fixed set of numbers (features) that
capture its structural and physicochemical properties. This model uses two complementary types:
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Morgan Fingerprints")
    st.markdown("""
    Each molecule is broken into overlapping substructures (radius = 2, each atom's local
    neighborhood out to 2 bonds), encoded as a **1024-bit binary vector** - each bit flags the
    presence of a specific substructural pattern.
    """)
with col2:
    st.subheader("2. RDKit Molecular Descriptors")
    st.markdown("""
    Roughly **217 calculated physicochemical properties** - molecular weight, LogP, topological
    polar surface area, hydrogen bond donor/acceptor counts, ring counts, and more.
    """)

st.info("Together, these give the model roughly **1,241 numerical features** per compound.")

st.divider()
st.header("How the Model Was Trained and Validated")
st.markdown("""
- **Data cleaning:** invalid structures removed, salts/mixtures standardized, duplicates and
  conflicting labels resolved
- **Class balancing:** class-weighting used during training to avoid bias toward the majority class
- **Scaffold split:** compounds split into training, test, and external validation sets by
  chemical scaffold, ensuring structurally similar molecules don't appear in both training and
  evaluation sets
- **Cross-validation:** 5-fold, scaffold-aware cross-validation confirmed results were stable
- **Hyperparameter tuning:** a systematic search checked whether adjusting the model's settings
  could improve performance
- **Probability calibration:** raw confidence scores were recalibrated so stated probabilities
  more accurately reflect true observed likelihood
""")

st.divider()
st.header("Performance Metrics")
perf = model_metadata.get("performance", {})
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("External Validation Accuracy", f"{perf.get('external_validation_accuracy', 0):.1%}")
with metric_col2:
    st.metric("Toxic-Class Recall", f"{perf.get('external_validation_toxic_recall', 0):.1%}")
with metric_col3:
    st.metric("Non-Toxic Recall", f"{perf.get('external_validation_nontoxic_recall', 0):.1%}")

st.write("Additional validation results:")
for key, value in perf.items():
    if key not in ["external_validation_accuracy", "external_validation_toxic_recall", "external_validation_nontoxic_recall"]:
        st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")

st.caption("""
This model prioritizes catching truly toxic compounds (high toxic-class recall) somewhat more
than avoiding false alarms on non-toxic compounds - a deliberate, safety-conscious trade-off
appropriate for an early-stage screening tool.
""")

st.divider()
st.header("Applicability Domain")
st.write(f"""
This model includes an **Applicability Domain (AD)** check - it measures how structurally similar
a query compound is to the molecules the model was trained on (distance to its
{ad_metadata.get("k_neighbors", 5)} nearest neighbors in the training set). If a compound is too
structurally different, the prediction is flagged as **"outside the applicability domain"** and
should be treated with extra caution.
""")

st.divider()
st.header("Known Limitations")
st.warning(model_metadata.get("notes", "See model documentation for known limitations."))
