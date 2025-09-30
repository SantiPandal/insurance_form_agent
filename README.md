# Insurance Form Agent

AI-powered insurance quote automation using browser agents and LLMs.

## Features

- **Automated Quote Generation**: Browser automation for Qualitas insurance portal
- **Multi-LLM Support**: Works with Anthropic Claude and Google Gemini
- **Streamlit UI**: Clean web interface for quote requests
- **4-Phase Automation**: Navigation → Extract → Select → Complete

## Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone <repo-url>
cd insurance_form_agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium --with-deps
```

### 2. Configure API Keys

Create `.env` file:

```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

### 3. Run the Application

```bash
# Launch Streamlit UI
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Usage

1. Enter vehicle details:
   - Marca (Brand): e.g., AUDI
   - Modelo (Model): e.g., Q3 S LINE SPORT BACK
   - Año (Year): e.g., 2020
   - Código Postal (ZIP): e.g., 05100

2. Click "Cotizar" button

3. Watch the 4-phase automation:
   - **Navigation**: Login and navigate to quote form
   - **Extract Options**: Get available vehicle variants
   - **Select Vehicle**: Choose best matching vehicle
   - **Complete Form**: Fill details and generate PDF

## Project Structure

```
insurance_form_agent/
├── app.py                      # Streamlit UI
├── quote_agent.py              # Core automation logic
├── scripts/
│   ├── qualitas_anthropic.py   # Anthropic Claude version
│   └── qualitas_gemini.py      # Google Gemini version
├── public/
│   ├── bg_image_logo.png       # Background image
│   └── LOGOBROVE_255x75.svg    # Logo
└── requirements.txt
```

## Technologies

- **Browser Automation**: browser-use library
- **LLMs**: Anthropic Claude, Google Gemini
- **UI Framework**: Streamlit
- **Browser**: Playwright (Chromium)

## Development

### Run CLI Scripts

```bash
# Anthropic version
python scripts/qualitas_anthropic.py

# Gemini version
python scripts/qualitas_gemini.py
```

### Models Used

- **Navigation**: claude-3-5-haiku-20241022
- **Extract**: claude-3-5-haiku-20241022
- **Select**: claude-sonnet-4-5-20250929
- **Complete**: claude-3-5-haiku-20241022

## License

Private - Brove Insurance
