"""
Featurization function for the Pulmonary Toxicity model.
Converts a SMILES string into the exact feature vector the model expects:
Morgan fingerprint (radius=2, nBits=1024) + full RDKit descriptor set.
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

descriptor_names = [name for name, _ in Descriptors._descList]

def featurize_smiles(smiles, radius=2, n_bits=1024):
    """
    Converts a single SMILES string into a combined feature vector.
    Returns None if the SMILES is invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Morgan fingerprint
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    fp_array = np.array(fp)

    # RDKit descriptors
    desc_values = []
    for name, func in Descriptors._descList:
        try:
            desc_values.append(func(mol))
        except Exception:
            desc_values.append(np.nan)
    desc_array = np.array(desc_values)

    # Handle any NaN/inf in descriptors (fallback: replace with 0)
    desc_array[np.isinf(desc_array)] = np.nan
    desc_array = np.nan_to_num(desc_array, nan=0.0)

    return np.hstack([fp_array, desc_array])
