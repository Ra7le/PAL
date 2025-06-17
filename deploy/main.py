import streamlit as st
import pandas as pd
from src.pal_model import PAL

st.title('Project Approval Law (PAL) Demo')

st.write('Evaluate a project using PAL parameters.')

# Input form
v_innov = st.slider('Innovation (V_innov)', 0.0, 1.0, 0.95)
v_impact = st.slider('Social Impact (V_impact)', 0.0, 1.0, 0.92)
v_fin = st.slider('Financial Attractiveness (V_fin)', 0.0, 1.0, 0.85)
s_reg = st.slider('Regulatory Constraints (S_reg)', 0.0, 1.0, 0.10)
s_risk = st.slider('Market Risks (S_risk)', 0.0, 1.0, 0.15)
s_skep = st.slider('Public Skepticism (S_skep)', 0.0, 1.0, 0.05)
c = st.slider('Contextual Complexity (C)', 0.0, 1.0, 0.28)
v_market = st.number_input('Market Value (USD)', min_value=0, value=100000000)

if st.button('Evaluate'):
    project_data = {
        'v_innov': v_innov, 'v_impact': v_impact, 'v_fin': v_fin,
        's_reg': s_reg, 's_risk': s_risk, 's_skep': s_skep,
        'c': c, 'v_market': v_market
    }
    
    pal = PAL()
    p, t, s, decision = pal.evaluate(project_data)
    
    st.write(f'**Approval Probability**: {p:.2f}')
    st.write(f'**Timeline**: {t:.1f} months')
    st.write(f'**Deal Value**: ${s:,.0f}')
    st.write(f'**Decision**: {decision}')
