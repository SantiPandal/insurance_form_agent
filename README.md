# Insurance Form Agent

Browser agent POC for automated insurance quotes.

## Setup

```bash
# Install
uv pip install -r requirements.txt

# Configure (.env file)
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key

# Run
streamlit run app.py
```

## Usage

1. Enter vehicle: Brand, Model, Year, ZIP
2. Click "Cotizar"
3. Get PDF quote

## Files

- `app.py` - UI
- `quote_agent.py` - Core automation
- `scripts/` - CLI versions
