
import streamlit as st
import pandas as pd
from utils import (
    load_artifacts, predict_with_ad, add_to_history,
    generate_csv_report, generate_pdf_report, inject_custom_css, PUBCHEM_URL, show_disclaimer, render_header, get_confidence_tier, explain_invalid_smiles
)

st.set_page_config(page_title="PNEUMOCOID-SR", page_icon="🫁", layout="wide")
inject_custom_css()

render_header("PNEUMOCOID-SR", "Pulmonary Toxicity Prediction System")

model, ad_scaler, ad_nn_model, ad_metadata, model_metadata = load_artifacts()
ad_threshold = ad_metadata["ad_threshold"]

if "history" not in st.session_state:
    st.session_state.history = []

tab1, tab2, tab3 = st.tabs(["Single Prediction", "Batch Prediction", "History"])

with tab1:
    st.subheader("Predict Toxicity for a Single Compound")
    st.markdown(f"Don't have a SMILES string? Look it up on [PubChem]({PUBCHEM_URL}) by compound name.")
    def set_example(smiles):
        st.session_state["single_smiles"] = smiles

    example_compounds = {
        "Paraquat (herbicide)": "C[N+]1=CC=C(C=C1)C1=CC=[N+](C)C=C1",
        "Amiodarone (cardiac drug)": "CCCCC1=C(C2=CC=CC=C2O1)C(=O)C3=CC(=C(C(=C3)I)OCCN(CC)CC)I",
        "Ethanol (simple alcohol)": "CCO",
        "Aspirin (NSAID)": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "Paracetamol (analgesic)": "CC(=O)NC1=CC=C(O)C=C1",
        "Nicotine (alkaloid)": "CN1CCC[C@H]1C1=CC=CN=C1",
        "Benzene (industrial solvent)": "C1=CC=CC=C1",
    }
    st.markdown("**Try an example** - pick a compound, then press Predict:")
    ex_col1, ex_col2 = st.columns([3, 1])
    with ex_col1:
        chosen_example = st.selectbox("Example compounds", list(example_compounds.keys()),
                                       label_visibility="collapsed", key="example_select")
    with ex_col2:
        st.button("Load Example", key="load_example_btn", use_container_width=True,
                   on_click=set_example, args=(example_compounds[st.session_state.get("example_select", list(example_compounds.keys())[0])],))

    smiles_input = st.text_input("Enter a SMILES string", placeholder="e.g., CCO", key="single_smiles")

    if st.button("Predict", key="single_predict_btn"):
        if smiles_input.strip() == "":
            st.warning("Please enter a SMILES string.")
        else:
            result = predict_with_ad(smiles_input.strip(), model, ad_scaler, ad_nn_model, ad_threshold)
            if result is None:
                st.error(explain_invalid_smiles(smiles_input))
            else:
                add_to_history(result, source="Single Prediction")
                col1, col2 = st.columns([1, 2])
                with col1:
                    from rdkit.Chem import Draw
                    img = Draw.MolToImage(result["mol"], size=(250, 250))
                    st.image(img, caption="Molecule structure")
                with col2:
                    label = result["predicted_label"]
                    proba = result["toxicity_probability"]
                    tier = get_confidence_tier(proba, result["in_applicability_domain"])
                    if label == "Toxic":
                        st.error(f"Prediction: **{label}**")
                    else:
                        st.success(f"Prediction: **{label}**")
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        st.metric("Toxicity Probability", f"{proba:.1%}")
                    with metric_col2:
                        st.metric("Confidence", tier.replace(" (outside applicability domain)", "").replace(" (borderline)", ""))
                    if result["in_applicability_domain"]:
                        st.info(f"Within applicability domain - {tier.lower()}")
                    else:
                        st.warning(f"Outside applicability domain - {tier.lower()}, treat this prediction with caution")

                single_df = pd.DataFrame([{
                    "SMILES": result["smiles"], "Prediction": result["predicted_label"],
                    "Toxicity Probability": result["toxicity_probability"],
                    "In Applicability Domain": result["in_applicability_domain"],
                    "Confidence Tier": tier
                }])
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button("Download as CSV", generate_csv_report(single_df),
                                        "prediction_report.csv", "text/csv", key="single_csv_dl")
                with dl_col2:
                    st.download_button("Download as PDF", generate_pdf_report(single_df, "Single Compound Prediction Report"),
                                        "prediction_report.pdf", "application/pdf", key="single_pdf_dl")

with tab2:
    st.subheader("Predict Toxicity for Multiple Compounds")
    st.markdown(f"Upload a CSV with a column named **SMILES**. Need SMILES strings? Look them up on [PubChem]({PUBCHEM_URL}).")
    sample_csv = pd.DataFrame({"SMILES": list(example_compounds.values())}).to_csv(index=False).encode("utf-8")
    st.download_button("Download a sample CSV", sample_csv, "sample_smiles.csv", "text/csv", key="sample_csv_dl")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="batch_upload")

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        if "SMILES" not in batch_df.columns:
            st.error("CSV must contain a column named 'SMILES'.")
        else:
            if st.button("Run Batch Prediction", key="batch_predict_btn"):
                results_list = []
                progress = st.progress(0)
                for i, smiles in enumerate(batch_df["SMILES"]):
                    result = predict_with_ad(str(smiles), model, ad_scaler, ad_nn_model, ad_threshold)
                    if result is None:
                        results_list.append({"SMILES": smiles, "Prediction": "Invalid SMILES",
                                              "Toxicity Probability": None, "In Applicability Domain": None,
                                              "Confidence Tier": None})
                    else:
                        add_to_history(result, source="Batch Prediction")
                        results_list.append({
                            "SMILES": result["smiles"], "Prediction": result["predicted_label"],
                            "Toxicity Probability": result["toxicity_probability"],
                            "In Applicability Domain": result["in_applicability_domain"],
                            "Confidence Tier": get_confidence_tier(result["toxicity_probability"], result["in_applicability_domain"])
                        })
                    progress.progress((i + 1) / len(batch_df))

                results_df = pd.DataFrame(results_list)
                st.dataframe(results_df, use_container_width=True)
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button("Download Results as CSV", generate_csv_report(results_df),
                                        "batch_prediction_report.csv", "text/csv", key="batch_csv_dl")
                with dl_col2:
                    st.download_button("Download Results as PDF", generate_pdf_report(results_df, "Batch Prediction Report"),
                                        "batch_prediction_report.pdf", "application/pdf", key="batch_pdf_dl")

with tab3:
    st.subheader("Prediction History (this session)")
    if len(st.session_state.history) == 0:
        st.info("No predictions made yet in this session.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True)
        dl_col1, dl_col2, dl_col3 = st.columns(3)
        with dl_col1:
            st.download_button("Download History as CSV", generate_csv_report(history_df),
                                "prediction_history.csv", "text/csv", key="history_csv_dl")
        with dl_col2:
            st.download_button("Download History as PDF", generate_pdf_report(history_df, "Prediction History Report"),
                                "prediction_history.pdf", "application/pdf", key="history_pdf_dl")
        with dl_col3:
            if st.button("Clear History", key="clear_history_btn"):
                st.session_state.history = []
                st.rerun()

show_disclaimer()
st.caption("PNEUMOCOID-SR | ExtraTreesClassifier (calibrated) | Morgan fingerprints + RDKit descriptors")
