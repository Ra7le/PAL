import pytest
import pandas as pd
from src.pal_model import PAL

def test_data_loader():
    data = pd.read_csv('data/input_sample.csv')
    
    assert data.shape[0] == 10, "Expected 10 projects"
    assert set(data.columns) == {
        'project_id', 'v_innov', 'v_impact', 'v_fin',
        's_reg', 's_risk', 's_skep', 'c', 'v_market'
    }, "Incorrect columns"
    
    assert all(0 <= data[col] <= 1 for col in [
        'v_innov', 'v_impact', 'v_fin', 's_reg', 's_risk', 's_skep', 'c'
    ]), "Values must be in [0,1]"
    assert all(data['v_market'] >= 0), "Market value must be non-negative"

def test_pal_with_data():
    pal = PAL()
    data = pd.read_csv('data/input_sample.csv')
    
    for _, row in data.iterrows():
        project_data = {
            'v_innov': row['v_innov'], 'v_impact': row['v_impact'], 'v_fin': row['v_fin'],
            's_reg': row['s_reg'], 's_risk': row['s_risk'], 's_skep': row['s_skep'],
            'c': row['c'], 'v_market': row['v_market']
        }
        p, _, _, _ = pal.evaluate(project_data)
        assert 0 <= p <= 1, f"Invalid probability for project {row['project_id']}"
