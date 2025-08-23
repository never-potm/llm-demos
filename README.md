# 1) set up once
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

# 2) run summary module

python -m main ai_company_summary --name Antropic --url https://www.anthropic.com 