import numpy as np
import pandas as pd

def pal(vi, vp, vf, sr, sk, ss, ct, vm):
    w = u = np.array([1/3, 1/3, 1/3])
    v = np.dot(w, [vi, vp, vf]) / np.sqrt(np.sum(w**2) + ct**2)
    s = np.dot(u, [sr, sk, ss]) / np.sqrt(np.sum(u**2) + ct**2)
    alpha, beta = 1.5, 0.5
    v_eff = v / (1 + alpha * s + ct)
    s_eff = s / (1 + beta * v + ct)
    f = v_eff - s_eff
    pt = 1 / (1 + np.exp(-f))
    tt = 12 * s_eff / v_eff
    sd = v_eff * vm
    return pt, tt, sd

# Load dataset
data = pd.read_csv('pal_dataset.csv')
data[['pt', 'tt', 'sd']] = data.apply(
    lambda row: pal(row['vi'], row['vp'], row['vf'], row['sr'], row['sk'], row['ss'], row['ct'], row['vm']),
    axis=1, result_type='expand'
)
data['out'] = data['pt'].apply(lambda x: 'A' if x > 0.5 else 'R')
data.to_csv('pal_dataset_verified.csv', index=False)
