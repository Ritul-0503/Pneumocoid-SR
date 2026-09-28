
import streamlit as st
from utils import load_artifacts, inject_custom_css

st.set_page_config(page_title="About the Model - PNEUMOCOID-SR", page_icon="\U0001FAC1", layout="wide")
inject_custom_css()

model, ad_scaler, ad_nn_model, ad_metadata, model_metadata = load_artifacts()

st.markdown("<div class='app-title' style='font-size:2rem;'>About the Model</div>", unsafe_allow_html=True)
st.divider()

# ===== Section 1: Model Overview =====
st.header("Model Overview")
st.write(f"""
PNEUMOCOID-SR uses an **{model_metadata.get("model_type", "ExtraTreesClassifier")}** - an ensemble
machine learning algorithm - to predict whether a chemical compound is likely to cause pulmonary
toxicity, based solely on its molecular structure (given as a SMILES string).
""")

st.subheader("Why ExtraTrees?")
st.markdown("""
ExtraTrees (Extremely Randomized Trees) builds a large collection ("forest") of decision trees,
where each tree is trained on the data with an added layer of randomness in how it chooses split
points. This extra randomness typically makes ExtraTrees **less prone to overfitting** than a
standard Random Forest, especially on data like molecular fingerprints, which are high-dimensional
and sparse. During development, ExtraTrees was compared directly against several other algorithms
(including Random Forest, XGBoost, LightGBM, CatBoost, SVM, Logistic Regression, K-Nearest
Neighbors, and ensemble/stacking approaches) on the same dataset and features, and consistently
came out on top on the metrics that matter most for this task.
""")

st.divider()

# ===== Section 2: How the Model "Sees" a Molecule =====
st.header("How the Model 'Sees' a Molecule")
st.write("""
Machine learning models cannot interpret a chemical structure directly - a compound first has to
be converted into a fixed set of numbers (features) that capture its structural and physicochemical
properties. This model uses two complementary types of features:
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Morgan Fingerprints")
    st.markdown("""
    Also known as ECFP (Extended-Connectivity Fingerprints). Each molecule is broken down into
    overlapping substructures (radius = 2, meaning each atom's local neighborhood out to 2 bonds),
    and encoded as a **1024-bit binary vector** - each bit flags the presence or absence of a
    specific substructural pattern. This lets the model recognize toxicity-associated chemical
    motifs it has seen in training.
    """)
with col2:
    st.subheader("2. RDKit Molecular Descriptors")
    st.markdown("""
    A set of roughly **217 calculated physicochemical properties** - such as molecular weight,
    LogP (lipophilicity), topological polar surface area, hydrogen bond donor/acceptor counts, and
    ring counts. These give the model direct access to whole-molecule properties that complement
    the substructure-level information from the fingerprint.
    """)

st.info("Together, these two feature types give the model roughly **1,241 numerical features** per compound to learn from.")

st.divider()

# ===== Section 3: How the Model Was Trained & Validated =====
st.header("How the Model Was Trained and Validated")
st.markdown("""
- **Data cleaning:** invalid structures removed, salts/mixtures standardized to their main
  fragment, duplicate molecules and conflicting labels resolved
- **Class balancing:** the model uses class-weighting during training to avoid bias toward the
  more common class in the dataset
- **Scaffold split:** rather than a simple random split, compounds were split into training,
  test, and external validation sets **by chemical scaffold** - ensuring structurally similar
  molecules don't appear in both the training and evaluation sets. This gives a far more honest
  measure of how the model performs on genuinely new chemical structures, rather than ones it has
  effectively already seen
- **Cross-validation:** performance was additionally verified with 5-fold, scaffold-aware
  cross-validation to confirm results were stable and not dependent on one lucky split
- **Hyperparameter tuning:** a systematic search was run to check whether adjusting the model's
  internal settings could improve performance
- **Probability calibration:** the model's raw confidence scores were recalibrated (Platt/sigmoid
  scaling) so that a stated probability - e.g., "80% likely toxic" - more accurately reflects the
  true observed likelihood
""")

st.divider()

# ===== Section 4: Performance Metrics (live from model_metadata.json) =====
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
Note: this model prioritizes catching truly toxic compounds (high toxic-class recall) somewhat
more than avoiding false alarms on non-toxic compounds - a deliberate, safety-conscious trade-off
appropriate for an early-stage screening tool.
""")

st.divider()

# ===== Section 5: Applicability Domain =====
st.header("Applicability Domain")
st.write(f"""
Not every prediction should be trusted equally. This model includes an **Applicability Domain
(AD)** check - it measures how structurally similar a query compound is to the molecules the
model was actually trained on (using distance to its {ad_metadata.get("k_neighbors", 5)} nearest
neighbors in the training set). If a compound is too structurally different from anything in the
training data, the prediction is flagged as **"outside the applicability domain"** and should be
treated with extra caution, since the model is essentially extrapolating beyond what it has
learned.
""")

st.divider()

# ===== Section 6: Known Limitations =====
st.header("Known Limitations")
st.warning(model_metadata.get("notes", "See model documentation for known limitations."))
