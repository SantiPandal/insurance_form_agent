"""
Insurance Quote Generator - Streamlit UI
OpenAI-inspired minimal design
"""
import streamlit as st
import asyncio
import base64
from pathlib import Path
from quote_agent import run_quote

# Page config
st.set_page_config(
    page_title="Insurance Quote Generator",
    page_icon="🚗",
    layout="centered"
)

# Load and encode images
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image("public/bg_image_logo.png")
logo_svg = get_base64_image("public/LOGOBROVE_255x75.svg")

# Custom CSS - OpenAI style
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Hide Streamlit toolbar for MVP */
    [data-testid="stToolbar"] {{
        display: none !important;
    }}

    header {{
        visibility: hidden;
    }}

    .stApp {{
        background-image: url('data:image/png;base64,{bg_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: white;
    }}

    .logo {{
        position: fixed;
        top: 1.5rem;
        left: 1.5rem;
        width: 180px;
        height: auto;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.9);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    .main {{
        max-width: 650px;
        margin: 0 auto;
        padding: 2rem 1rem 4rem 1rem;
    }}

    .block-container {{
        padding: 0 !important;
        background: transparent !important;
        padding-top: 2rem !important;
    }}

    h1 {{
        text-align: center;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
        color: #111827;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 12px rgba(255, 255, 255, 0.95),
                     0 4px 24px rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.7);
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }}

    .subtitle {{
        text-align: center;
        color: #4b5563;
        font-size: 1.125rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
        background: rgba(255, 255, 255, 0.7);
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }}

    .stForm {{
        background: white !important;
        padding: 2.5rem 2rem !important;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
        margin: 2rem 0;
    }}

    .stFormSubmitButton>button {{
        border: 2px solid #7ed321 !important;
    }}

    .stFormSubmitButton>button:hover {{
        background-color: #7ed321 !important;
        border-color: #7ed321 !important;
        box-shadow: 0 0 0 3px rgba(126, 211, 33, 0.2) !important;
    }}

    .stTextInput>div>div>input {{
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        padding: 0.875rem 1rem;
        font-size: 15px;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        background: white;
    }}

    .stTextInput>div>div>input:focus {{
        border-color: #10a37f;
        box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1);
    }}

    .stTextInput>label {{
        font-size: 14px;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }}

    h1 {{
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #111827;
        letter-spacing: -0.02em;
    }}

    .subtitle {{
        color: #6b7280;
        font-size: 1.125rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }}

    /* Progress container - solid white background like form */
    .progress-container {{
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
        margin: 1rem 0 2rem 0;
    }}

    /* Progress bar styling - fully opaque */
    .stProgress > div > div > div > div {{
        background-color: #10a37f !important;
        opacity: 1 !important;
    }}

    .stProgress > div > div {{
        background-color: #e5e7eb !important;
        opacity: 1 !important;
    }}

    .phase-container {{
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }}

    .phase-item {{
        display: flex;
        align-items: center;
        padding: 0.75rem 0;
        font-size: 15px;
    }}

    .phase-icon {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 14px;
        font-weight: 600;
    }}

    .phase-pending {{
        background: #f3f4f6;
        color: #9ca3af;
    }}

    .phase-active {{
        background: #10a37f;
        color: white;
    }}

    .phase-complete {{
        background: #059669;
        color: white;
    }}

    .phase-text {{
        color: #374151;
        font-weight: 500;
    }}

    footer {{
        text-align: center;
        color: #6b7280;
        font-size: 0.875rem;
        margin-top: 2rem;
        padding: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# Logo
st.markdown(f'<img src="data:image/svg+xml;base64,{logo_svg}" class="logo">', unsafe_allow_html=True)

# Header
st.title("Generador de Cotizaciones")
st.markdown('<p class="subtitle">Obtén cotizaciones instantáneas con automatización IA</p>', unsafe_allow_html=True)

# Input form
with st.form("vehicle_form"):
    col1, col2 = st.columns(2)

    with col1:
        brand = st.text_input("Marca", placeholder="e.g., AUDI", value="AUDI")
        year = st.text_input("Año", placeholder="e.g., 2020", value="2020")

    with col2:
        model = st.text_input("Modelo", placeholder="e.g., Q3 S LINE SPORT BACK", value="Q3 S LINE SPORT BACK")
        zip_code = st.text_input("Código Postal", placeholder="e.g., 05100", value="05100")

    submitted = st.form_submit_button("Cotizar")

# Process form
if submitted:
    if not brand or not model or not year:
        st.error("Please fill in all required fields")
    else:
        # Prepare vehicle info
        vehicle_info = {
            "brand": brand.upper(),
            "model": model.upper(),
            "year": year,
            "zip_code": zip_code,
            "engine": "L4 2.0T",
            "doors": "5 puertas"
        }

        # Three main phases (Extract merged into Select)
        phase_labels = [
            "🚀 Navigation",
            "🎯 Select Vehicle",
            "✅ Complete Form"
        ]

        # Progress container with solid background
        with st.container():
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            progress_bar = st.progress(0)
            status_text = st.empty()
            st.markdown('</div>', unsafe_allow_html=True)

        def update_progress(phase: int, message: str):
            """Update progress display with simple progress bar"""
            if phase == -1:
                st.error(f"❌ {message}")
                return

            # Calculate progress percentage (0-100)
            if phase == 0:
                progress_value = 0
                phase_name = "Initializing..."
            elif phase == 1:
                progress_value = 33
                phase_name = phase_labels[0]
            elif phase == 2:
                progress_value = 66
                phase_name = phase_labels[1]
            elif phase >= 3:
                progress_value = 100
                phase_name = phase_labels[2]
            else:
                progress_value = 0
                phase_name = message

            # Update progress bar and status
            progress_bar.progress(progress_value)
            status_text.info(f"**{phase_name}** - {message}")

        # Initial state
        status_text.info("🔄 Ready to start automation...")

        # Run automation
        try:
            result = asyncio.run(run_quote(vehicle_info, update_progress))

            if result["status"] == "success":
                progress_bar.progress(100)
                status_text.success("✅ Quote generated successfully!")
                st.balloons()
            else:
                st.error(f"Error: {result['message']}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
