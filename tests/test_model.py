import pytest
import numpy as np
from src.pal_model import PAL

def test_pal_evaluation():
    pal = PAL()
    project_data = {
        'v_innov': 0.95, 'v_impact': 0.92, 'v_fin': 0.85,
        's_reg': 0.10, 's_risk': 0.15, 's_skep': 0.05,
        'c': 0.28, 'v_market': 100000000
    }
    
    p, t, s, decision = pal.evaluate(project_data)
    
    assert 0 <= p <= 1, "Probability must be in [0,1]"
    assert t >= 0, "Timeline must be non-negative"
    assert s >= 0, "Deal value must be non-negative"
    assert decision in ['PASS', 'FAIL', 'BORDERLINE'], "Invalid decision"
    assert abs(p - 0.93) < 0.1, "Probability mismatch for ESG case"

def test_pal_extreme_case():
    pal = PAL()
    project_data = {
        'v_innov': 0.0, 'v_impact': 0.0, 'v_fin': 0.0,
        's_reg': 1.0, 's_risk': 1.0, 's_skep': 1.0,
        'c': 1.0, 'v_market': 100000000
    }
    
    p, t, s, decision = pal.evaluate(project_data)
    
    assert p < 0.1, "Probability should be low for extreme resistance"
    assert t > 100, "Timeline should be large for extreme resistance"
    assert decision == 'FAIL', "Decision should be FAIL"
