"""
Afirme Insurance Quote Automation
Two-agent architecture for navigating and filling insurance forms
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatOpenAI

load_dotenv()

# Model configuration - Easy to change for testing different models
NAVIGATION_MODEL = os.getenv("NAVIGATION_MODEL", "gpt-4.1-mini")  # Simpler model for navigation
FORM_FILLING_MODEL = os.getenv("FORM_FILLING_MODEL", "gpt-4.1-mini")  # More powerful model for form understanding

# Alternative model options to try:
# OpenAI: "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"
# Anthropic: "claude-3-opus", "claude-3-sonnet", "claude-3-haiku"
# Others: Check browser_use documentation for supported models

# Main Navigation Agent Prompt
MAIN_AGENT_PROMPT = """
You are an insurance quote automation agent for Afirme Seguros. Your task is to navigate through their web portal and obtain car insurance quotes.

CONTEXT:
- Website: https://www.afirmeseguros.com/cercania360/#/login
- Each action must wait for full page load before proceeding
- After clicking "Cotización Individual", a new tab opens that you must switch to

YOUR RESPONSIBILITIES:
1. Login with credentials: danos@brove.com.mx / Brove202
2. Select "AGT Emisión" role (NOT Siniestros or Cobranzas)
3. Click "Cotización y Emisión" from left menu 
4. Click "Cotización Individual" under Auto section, the button will redirect to the new tab. 
6. Wait for the new page to fully load (5-10 seconds)
7. STOP when you reach the vehicle information form
8. Report that you've reached the form and are ready for vehicle data entry

CRITICAL RULES:
- VERIFY each page loaded completely before proceeding
- **AFTER clicking any link, check if new tabs opened and switch to the correct tab**
- Use switch_tab action whenever you detect a new tab has opened
- If error occurs, retry from last successful step

TAB HANDLING:
- After clicking "Cotización Individual", a new tab typically opens
- Use switch_tab action to move to the new tab
- Verify you're on the correct page before proceeding ( the tab takes some time to load, so wait )
- The vehicle form should appear in the new tab

IMPORTANT: When you see the vehicle information form (Bienvenida al Cotizador de Automóviles),
STOP and report "VEHICLE_FORM_READY" so the vehicle data agent can take over.
"""


# Vehicle Data Agent Prompt
VEHICLE_AGENT_PROMPT = """
You are an intelligent form-filling agent specialized in vehicle insurance quotes. Your task is to complete the vehicle information form on the Afirme insurance website.

CONTEXT:
- You are on the vehicle information form page
- Insurance forms have interdependent fields (dropdowns that affect other dropdowns)
- Some fields auto-populate based on previous selections
- Forms may load data dynamically and require waiting

YOUR TASK:
1. Analyze the current form to understand its structure
2. Fill the form with this vehicle information:
   - Product Type: SP
   - Policy Duration: Anual (Annual)
   - Vehicle Make: General Motors
   - Vehicle Model: Chevrolet Brew
   - Sub-model: Activa
   - Year: 2022
   - Policy Type: Auto Individual
   - Usage: Select the only available option
   - Postal Code: 11000

3. Handle any dynamic behavior (waiting for dropdowns to load, auto-population)
4. After filling all fields, click "SIGUIENTE" to proceed
5. On the final page, click "IMPRIMIR" to generate the PDF quote

CRITICAL RULES:
- OBSERVE how the form behaves - some selections trigger other fields to populate
- WAIT for dynamic content to load after making selections (3-5 seconds between field changes)
- VERIFY that auto-filled fields contain correct data
- ADAPT to the specific form's requirements and flow

SUCCESS: PDF quote is generated and ready for download
"""


async def main():
    """
    Main function that orchestrates the two-agent flow for Afirme insurance quote
    """
    print("🚀 Starting Afirme Insurance Quote Automation")
    print("=" * 60)
    print(f"📊 Models: Navigation={NAVIGATION_MODEL}, Form={FORM_FILLING_MODEL}")
    print("=" * 60)

    # Initialize browser with keep_alive to maintain session between agents
    browser = Browser(keep_alive=True)

    try:
        # Start the browser session
        await browser.start()
        print("✅ Browser started successfully")
        print("-" * 60)

        # Phase 1: Navigation Agent
        print("📍 Phase 1: Navigation to Vehicle Form")
        print("Agent will: Login → Select Role → Navigate → Find Form")

        nav_agent = Agent(
            task=MAIN_AGENT_PROMPT,
            browser_session=browser,
            llm=ChatOpenAI(model=NAVIGATION_MODEL)
        )

        # Run navigation agent with sufficient steps for slow page loads
        result = await nav_agent.run(max_steps=15)

        print("\n✅ Navigation completed - Vehicle form reached")
        print("-" * 60)

        # Small delay to ensure form is fully loaded
        await asyncio.sleep(3)

        # Phase 2: Vehicle Data Agent
        print("📝 Phase 2: Filling Vehicle Information")
        print("Agent will: Analyze form → Fill data → Submit → Get quote")

        vehicle_agent = Agent(
            task=VEHICLE_AGENT_PROMPT,
            browser_session=browser,
            llm=ChatOpenAI(model=FORM_FILLING_MODEL)
        )

        # Run vehicle data agent to complete the form
        result = await vehicle_agent.run(max_steps=20)

        print("\n✅ Vehicle form completed - Quote generated")
        print("=" * 60)
        print("🎉 SUCCESS: Insurance quote process completed!")

        # Keep browser open for 10 seconds to review results
        print("\n⏰ Browser will remain open for 10 seconds...")
        await asyncio.sleep(10)

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("Please check the browser window for current state")

    finally:
        # Clean up browser session
        await browser.kill()
        print("\n🔒 Browser session closed")


if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())