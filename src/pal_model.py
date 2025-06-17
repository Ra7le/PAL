import numpy as np
import pandas as pd
import argparse

class PAL:
    """Project Approval Law (PAL) model for institutional decision-making."""
    
    def __init__(self, weights=None, alpha=1.5, beta=0.5, t0=12.0):
        """
        Initialize PAL with weights and hyperparameters.
        
        Args:
            weights (dict): Weights for V and S components (default: equal weights 1/3).
            alpha (float): Resistance suppression factor (default: 1.5, Weber-Fechner).
            beta (float): Value suppression factor (default: 0.5).
            t0 (float): Base timeline in months (default: 12).
        """
        self.alpha = alpha
        self.beta = beta
        self.t0 = t0
        self.weights = weights if weights else {
            'v_innov': 1/3, 'v_impact': 1/3, 'v_fin': 1/3,
            's_reg': 1/3, 's_risk': 1/3, 's_skep': 1/3
        }

    def evaluate(self, project_data):
        """
        Evaluate a project and return approval probability, timeline, and deal value.
        
        Args:
            project_data (dict): Project parameters including:
                - v_innov, v_impact, v_fin: Value components [0,1]
                - s_reg, s_risk, s_skep: Resistance components [0,1]
                - c: Contextual complexity [0,1]
                - v_market: Market value in USD
                
        Returns:
            tuple: (p_approval, t_months, s_deal, decision)
        """
        # Extract parameters
        v = np.array([project_data['v_innov'], project_data['v_impact'], project_data['v_fin']])
        s = np.array([project_data['s_reg'], project_data['s_risk'], project_data['s_skep']])
        c = project_data['c']
        v_market = project_data['v_market']
        
        # Compute weighted V and S
        w = np.array([self.weights['v_innov'], self.weights['v_impact'], self.weights['v_fin']])
        u = np.array([self.weights['s_reg'], self.weights['s_risk'], self.weights['s_skep']])
        v_total = np.dot(w, v) / np.sqrt(np.sum(w)**2 + c**2)
        s_total = np.dot(u, s) / np.sqrt(np.sum(u)**2 + c**2)
        
        # Effective value and resistance
        v_eff = v_total / (1 + self.alpha * s_total + c)
        s_eff = s_total / (1 + self.beta * v_total + c)
        
        # Approval energy and probability
        f = v_eff - s_eff
        p_approval = 1 / (1 + np.exp(-f))
        
        # Timeline and deal value
        t_months = self.t0 * s_eff / v_eff if v_eff > 0 else float('inf')
        s_deal = v_eff * v_market
        
        # Decision based on probability
        decision = 'PASS' if p_approval > 0.7 else 'FAIL' if p_approval < 0.3 else 'BORDERLINE'
        
        return p_approval, t_months, s_deal, decision

def main():
    parser = argparse.ArgumentParser(description='Run PAL on input data.')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    args = parser.parse_args()
    
    # Load data
    data = pd.read_csv(args.input)
    
    # Initialize PAL
    pal = PAL()
    
    # Evaluate projects
    results = []
    for _, row in data.iterrows():
        project_data = {
            'v_innov': row['v_innov'], 'v_impact': row['v_impact'], 'v_fin': row['v_fin'],
            's_reg': row['s_reg'], 's_risk': row['s_risk'], 's_skep': row['s_skep'],
            'c': row['c'], 'v_market': row['v_market']
        }
        p, t, s, decision = pal.evaluate(project_data)
        results.append({
            'project_id': row['project_id'], 'p_approval': p, 't_months': t,
            's_deal': s, 'decision': decision
        })
    
    # Save results
    pd.DataFrame(results).to_csv(args.output, index=False)
    print(f'Results saved to {args.output}')

if __name__ == '__main__':
    main()
