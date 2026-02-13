# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from sklearn.preprocessing import StandardScaler



# ================================================================
# 1. Section: IO
# ================================================================
def get_data_ready(syllables: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # 1. Builds the data
    data = []
    meta = []
    for syl in syllables:
        data.append(syl.counts)
        meta.append(syl.metadata)

    return (np.array(data), np.array(meta))



# ================================================================
# 2. Section: Operations
# ================================================================
def numerical_stabilization(data: np.ndarray, value: float = 1e-8) -> np.ndarray:
    return data + value

def log_norm_center(data: np.ndarray) -> np.ndarray:
    # 1. Logs the data
    log_data = np.log(data)

    # 2. Center by the mean
    return log_data - log_data.mean(axis=1, keepdims=True)

def scaling(data: np.ndarray) -> np.ndarray:
    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    return np.array(data)
