"""
Insurance Quote Agent - Parameterized version
"""
import asyncio
import os
from typing import Callable, Optional
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatAnthropic, ChatOpenAI


load_dotenv()

# Model configuration - OpenAI, Sonnet, OpenAI
NAVIGATION_MODEL = os.getenv("NAVIGATION_MODEL", "gpt-4.1-mini")
SELECT_MODEL = os.getenv("SELECT_MODEL", "claude-sonnet-4-5-20250929")
COMPLETION_MODEL = os.getenv("COMPLETION_MODEL", "gpt-4.1-mini")


def build_prompts(vehicle_info: dict):
    """Build prompts with vehicle info"""

    navigation_prompt = """
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

    # Extract base model name (first word/alphanumeric part of model)
    base_model = vehicle_info['model'].split()[0] if ' ' in vehicle_info['model'] else vehicle_info['model']

    select_prompt = f"""
Type "{vehicle_info['brand']} {base_model} {vehicle_info['year']}" in the vehicle search box.
Wait 2 seconds for the dropdown suggestions to appear.

From the dropdown list, select the vehicle that BEST matches these specifications:
- Brand: {vehicle_info['brand']}
- Model: {vehicle_info['model']}
- Year: {vehicle_info['year']}
- Engine: {vehicle_info.get('engine', 'L4 2.0T')}
- Doors: {vehicle_info.get('doors', '5 puertas')}

SELECTION CRITERIA:
- Prioritize: Year {vehicle_info['year']}, semantic matching
- The exact wording may differ (e.g., "180 CP" means 180hp)
- Focus on semantic matching, not exact string matching
- Use click_element action to select the best match

- Scroll down to see the zip code text field.
- Add the zip code: {vehicle_info.get('zip_code', '05100')}
- Use the click_element action to select the zone depicted in the zip code. It should be a single option in a dropdown.

- Use the click_element action to select the "siguiente" button.

STOP after selecting the vehicle.
"""

    completion_prompt = """
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

    return navigation_prompt, select_prompt, completion_prompt


async def run_quote(vehicle_info: dict, progress_callback: Optional[Callable] = None):
    """
    Run insurance quote automation

    Args:
        vehicle_info: dict with keys: brand, model, year, engine (optional), doors (optional), zip_code (optional)
        progress_callback: function(phase: int, message: str) for progress updates

    Returns:
        dict with status and any error messages
    """
    def update_progress(phase: int, message: str):
        if progress_callback:
            progress_callback(phase, message)

    try:
        update_progress(0, "Building prompts...")
        nav_prompt, select_prompt, completion_prompt = build_prompts(vehicle_info)

        update_progress(0, "Starting browser...")
        browser = Browser(keep_alive=True)
        await browser.start()

        try:
            # Phase 1: Navigation (OpenAI)
            update_progress(1, "Navigating to quote form...")
            nav_agent = Agent(
                task=nav_prompt,
                browser_session=browser,
                llm=ChatOpenAI(model=NAVIGATION_MODEL)
            )
            await nav_agent.run(max_steps=20)
            await asyncio.sleep(2)

            # Phase 2: Select (Claude Sonnet - type and select vehicle)
            update_progress(2, "Selecting vehicle...")
            select_agent = Agent(
                task=select_prompt,
                browser_session=browser,
                llm=ChatAnthropic(model=SELECT_MODEL)
            )
            await select_agent.run(max_steps=15)
            await asyncio.sleep(2)

            # Phase 3: Complete (OpenAI)
            update_progress(3, "Completing quote form...")
            completion_agent = Agent(
                task=completion_prompt,
                browser_session=browser,
                llm=ChatOpenAI(model=COMPLETION_MODEL)
            )
            await completion_agent.run(max_steps=20)

            update_progress(4, "Quote completed successfully!")

            # Keep browser open briefly
            await asyncio.sleep(10)

            return {"status": "success", "message": "Quote generated successfully"}

        finally:
            await browser.kill()

    except Exception as e:
        update_progress(-1, f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}