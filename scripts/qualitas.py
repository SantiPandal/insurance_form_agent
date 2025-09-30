"""
Qualitas Insurance Quote Automation
Single agent architecture for logging in and navigating insurance portal
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatOpenAI

load_dotenv()

# Model configuration
NAVIGATION_MODEL = os.getenv("NAVIGATION_MODEL", "gpt-4.1-mini")
EXTRACT_MODEL = os.getenv("EXTRACT_MODEL", "gpt-4.1-mini")
SELECT_MODEL = os.getenv("SELECT_MODEL", "gpt-4.1-mini")
COMPLETION_MODEL = os.getenv("COMPLETION_MODEL", "gpt-4.1-mini")

# Phase 1: Navigation Agent
NAVIGATION_PROMPT = """
Navigate to the vehicle selection form on Qualitas Seguros portal.

STEPS:
1. Login at https://agentes360.qualitas.com.mx/web/guest/home
   Credentials: Clave: 53913, Cuenta: SCERVANTES, Contraseña: Sama2023

2. Click "Cotizar" button
   **CRITICAL**: This opens a NEW TAB - use switch_tab immediately

3. Select "Residente", click Next

4. Select "Autos", click Next

5. STOP when you see the vehicle search box

IMPORTANT:
- Wait 2-3 seconds after each action
- NEW TAB opens after Cotizar - must switch_tab
- Use scroll if needed
"""

# Phase 2A: Extract Dropdown Options
EXTRACT_OPTIONS_PROMPT = """
Type "AUDI Q3" in the vehicle search box.
Wait 2 seconds for the dropdown suggestions to appear.
Use extract_page_content action to get ALL visible dropdown options.
Return the complete list of available vehicles shown.

STOP after extracting the list.
"""

# Phase 2B: Semantic Vehicle Selection
SELECT_VEHICLE_PROMPT = """
From the dropdown list, select the vehicle that BEST matches these specifications:
- Brand: AUDI
- Model: Q3 S LINE SPORT BACK
- Year: 2020
- Engine: L4 2.0T (approximately 180 horsepower, 2.0 liter)
- Doors: 5 puertas

SELECTION CRITERIA:
- Prioritize: Year 2020, engine size ~2.0L, horsepower ~180hp
- The exact wording may differ (e.g., "180 CP" means 180hp)
- Focus on semantic matching, not exact string matching
- Use click_element action to select the best match

STOP after selecting the vehicle.
"""

# Phase 3: Completion Agent
COMPLETION_PROMPT = """
Complete the insurance quote form and download PDF.

STEPS:
1. Enter postal code: 5100, click Next
2. Continue through "Datos de cotización" (keep defaults), click Next
3. Continue through "Coberturas" (don't select anything), click Next
4. Download the PDF quote

IMPORTANT:
- Use scroll to find buttons
- Wait 2-3 seconds between steps
"""


async def main():
    """
    Four-phase automation for Qualitas insurance quote
    """
    print("🚀 Starting Qualitas Insurance Automation (4-Phase)")
    print("=" * 60)
    print(f"📊 Phase 1 - Navigation: {NAVIGATION_MODEL}")
    print(f"📋 Phase 2A - Extract Options: {EXTRACT_MODEL}")
    print(f"🎯 Phase 2B - Select Vehicle: {SELECT_MODEL}")
    print(f"✅ Phase 3 - Completion: {COMPLETION_MODEL}")
    print("=" * 60)

    # Initialize browser with keep_alive to maintain session across agents
    browser = Browser(keep_alive=True)

    try:
        # Start the browser session
        await browser.start()
        print("✅ Browser started successfully")
        print("-" * 60)

        # Phase 1: Navigation Agent
        print("📍 Phase 1: Navigation to Vehicle Search")
        nav_agent = Agent(
            task=NAVIGATION_PROMPT,
            browser_session=browser,
            llm=ChatOpenAI(model=NAVIGATION_MODEL)
        )
        await nav_agent.run(max_steps=20)
        print("✅ Phase 1 complete - Reached vehicle search box")
        await asyncio.sleep(2)
        print("-" * 60)

        # Phase 2A: Extract Dropdown Options
        print("📋 Phase 2A: Extract Vehicle Options from Dropdown")
        extract_agent = Agent(
            task=EXTRACT_OPTIONS_PROMPT,
            browser_session=browser,
            llm=ChatOpenAI(model=EXTRACT_MODEL)
        )
        await extract_agent.run(max_steps=10)
        print("✅ Phase 2A complete - Options extracted")
        await asyncio.sleep(2)
        print("-" * 60)

        # Phase 2B: Semantic Vehicle Selection
        print("🎯 Phase 2B: Select Best Matching Vehicle")
        select_agent = Agent(
            task=SELECT_VEHICLE_PROMPT,
            browser_session=browser,
            llm=ChatOpenAI(model=SELECT_MODEL)
        )
        await select_agent.run(max_steps=10)
        print("✅ Phase 2B complete - Vehicle selected")
        await asyncio.sleep(2)
        print("-" * 60)

        # Phase 3: Completion Agent
        print("📝 Phase 3: Form Completion & PDF Download")
        completion_agent = Agent(
            task=COMPLETION_PROMPT,
            browser_session=browser,
            llm=ChatOpenAI(model=COMPLETION_MODEL)
        )
        await completion_agent.run(max_steps=20)
        print("✅ Phase 3 complete - PDF downloaded")
        print("-" * 60)

        print("\n" + "=" * 60)
        print("🎉 SUCCESS: All phases completed!")
        print("=" * 60)

        # Keep browser open for review
        print("\n⏰ Browser will remain open for 15 seconds...")
        await asyncio.sleep(15)

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("Please check the browser window for current state")

    finally:
        # Clean up browser session
        await browser.kill()
        print("\n🔒 Browser session closed")


if __name__ == "__main__":
    asyncio.run(main())