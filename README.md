# 1) set up once
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

# 2) run module-1
python -m src.main module-1 --name Alice --times 3