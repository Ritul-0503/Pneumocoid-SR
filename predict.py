"""
Example usage: load the model and predict pulmonary toxicity for new SMILES.
"""
import joblib
import numpy as np
from featurize import featurize_smiles

model = joblib.load('pulmonary_toxicity_model.pkl')

def predict_toxicity(smiles):
    features = featurize_smiles(smiles)
    if features is None:
        return {"error": "Invalid SMILES string"}
    features = features.reshape(1, -1)
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    return {
        "smiles": smiles,
        "predicted_label": prediction,   # 1 = toxic, 0 = non-toxic
        "toxicity_probability": round(probability, 4)
    }

if __name__ == "__main__":
    example = predict_toxicity("CCO")  # ethanol, example
    print(example)
