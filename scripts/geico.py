#!/usr/bin/env python
"""Direct Geico insurance quote automation - no abstractions."""

import asyncio
import os
from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# The complete task for Geico
GEICO_TASK = """
Navigate to Geico's auto insurance website (https://www.geico.com) and get a quote:

1. Click on "Start a quote" or similar button
2. Enter ZIP code: 12345
3. Select that you want auto insurance
4. Enter vehicle information: 2022 Toyota Camry
5. Enter driver birth date: 01/15/1985
6. Complete the quote form with these defaults if asked:
   - Currently insured: Yes
   - Own or lease: Own
   - Primary use: Commute
   - Annual mileage: 12,000
7. Get to the quote results page
8. Take a screenshot of the final quote

Note: Use reasonable defaults for any additional required fields.
"""

async def main():
    print("Starting Geico insurance quote automation...")
    print("-" * 50)

    # Create the Browser Use agent
    agent = Agent(
        task=GEICO_TASK,
        llm=ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    )

    # Run the automation
    result = await agent.run(max_steps=100)

    print("-" * 50)
    print("Automation complete!")
    print(f"Result: {result}")

    return result

if __name__ == "__main__":
    asyncio.run(main())