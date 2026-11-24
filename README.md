# Afficionado Coffee Roasters — Sales Analysis
## Dataset
Worksheet: Transactions | Records: 149,116 | Columns: 11 | Year: 2025
Stores: 3 | Categories: 9 | Product details: 80
## Important limitation
There is no transaction date field in the supplied workbook. Weekday, daily and monthly trends cannot be calculated reliably. Do not invent dates. The dashboard analyses time-of-day, products and store locations. Request a date-level file from Unified Mentor if weekday/month analysis is compulsory.
## Headline results
- Transactions: 149,116
- Units sold: 214,470
- Calculated sales value: $698,812.33 (currency not specified in workbook)
- Average transaction value: $4.69
- Highest category by sales value: Coffee
- Highest store by sales value: Hell's Kitchen
- Highest time band by sales value: Morning (6–10)
- Highest single hour by sales value: 10:00
## Run locally
Install Python 3.10+, open this folder in VS Code, then run:
1. `python -m venv .venv`
2. Windows: `.venv\\Scripts\\activate` | macOS/Linux: `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `streamlit run app.py`
## Files
`app.py` dashboard | `analysis.py` exports summaries | `research_paper.pdf` report | original Excel dataset | `requirements.txt`
