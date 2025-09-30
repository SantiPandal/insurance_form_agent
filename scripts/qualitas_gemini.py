"""
Qualitas Insurance Quote Automation - Google Gemini Version
Four-phase automation using Gemini models
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatGoogle

load_dotenv()

# Model configuration - Gemini models
NAVIGATION_MODEL = os.getenv("NAVIGATION_MODEL", "gemini-2.5-flash")
EXTRACT_MODEL = os.getenv("EXTRACT_MODEL", "gemini-2.5-flash")
SELECT_MODEL = os.getenv("SELECT_MODEL", "gemini-2.5-flash")
COMPLETION_MODEL = os.getenv("COMPLETION_MODEL", "gemini-2.5-flash")

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
Type "AUDI Q3 2020" in the vehicle search box.
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

- Add the zip code of the city you are in (05100)
- Use the click_element action to select the zone depicted in the zip code. It should be a single option in a dropdown.

- Use the click_element action to select the "siguiente" button.

STOP after selecting the vehicle.
"""

# Phase 3: Completion Agent
COMPLETION_PROMPT = """
Complete the insurance quote form and download PDF.

STEPS:
1. Use scroll action to scroll down 2 pages to see all "Datos de cotización" options
2. Keep defaults in "Datos de cotización", use click_element to select "siguiente"
3. Use scroll action to scroll down 2 pages to view "Coberturas" section
4. Don't select any coverage options, use click_element to select "siguiente"
5. Use scroll action to scroll down 2 pages to locate "imprimir" button
6. Use click_element action to select "imprimir" - opens new tab with PDF

IMPORTANT:
- Use scroll action explicitly between each major step
- Wait 2-3 seconds after scrolling before clicking
- Scroll 2 pages = enough to see full form sections
"""


async def main():
    """
    Four-phase automation for Qualitas insurance quote using Gemini models
    """
    print("🚀 Starting Qualitas Insurance Automation - Google Gemini (4-Phase)")
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
            llm=ChatGoogle(model=NAVIGATION_MODEL)
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
            llm=ChatGoogle(model=EXTRACT_MODEL)
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
            llm=ChatGoogle(model=SELECT_MODEL)
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
            llm=ChatGoogle(model=COMPLETION_MODEL)
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