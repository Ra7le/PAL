 PAL-Dataset

A dataset for the Project Approval Law (PAL) framework, comprising 550 case studies across infrastructure, ESG (Environmental, Social, and Governance), AI/biotech, fintech, and public policy domains.

   Fields

- `id`: Unique identifier for each case.
- `dom`: Domain (`inf`=infrastructure, `esg`=ESG, `ai`=AI/biotech, `fin`=fintech, `pol`=public policy).
- `jur`: Jurisdiction (ISO 3166-1 alpha-3 code or regional code).
- `vi`, `vp`, `vf`: Project value metrics (innovation, impact, financial).
- `sr`, `sk`, `ss`: Systemic resistance metrics (regulatory, risk, skepticism).
- `ct`: Contextual complexity.
- `vm`: Market value ($M).
- `pt`, `tt`, `sd`: Approval probability, timeline (months), and deal value ($M).
- `out`: Outcome (`A`=Approved, `R`=Rejected).
- `src`: Data sources (`PB`=PitchBook, `WB`=World Bank, `GN`=Google News, `ESG`=S&P ESG, `WIPO`=Google Patents/WIPO).

  Usage

To use the dataset and calculate PAL metrics, install the required dependencies and run the provided script:

```bash
pip install pandas numpy
python pal_calculator.py
