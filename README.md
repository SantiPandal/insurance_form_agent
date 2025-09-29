# Insurance Quote Automation POC

Simple proof-of-concept using Browser Use to automate insurance quote forms.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini  # optional, defaults to gpt-4o-mini
```

## Run

Get a quote from any insurer:

```bash
# Afirme
python scripts/afirme.py

# Geico
python scripts/geico.py

# Progressive
python scripts/progressive.py
```

## What it does

Each script will:
1. Open a browser (set `BROWSER_USE_HEADLESS=true` in .env for headless mode)
2. Navigate to the insurance website
3. Fill out the quote form with test data
4. Get to the results page
5. Take a screenshot

## Customize

Edit the `TASK` variable in any script to change the quote parameters.
