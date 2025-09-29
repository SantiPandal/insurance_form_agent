#!/usr/bin/env python
"""Direct Progressive insurance quote automation - no abstractions."""

import asyncio
import os
from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# The complete task for Progressive
PROGRESSIVE_TASK = """
Navigate to Progressive's auto insurance website (https://www.progressive.com) and get a quote:

1. Click "Get a Quote" or "Quote auto"
2. Enter ZIP code: 12345
3. Enter personal information:
   - First name: John
   - Last name: Smith
   - Birth date: 01/15/1985
   - Email: test@example.com
4. Enter vehicle details:
   - Year: 2022
   - Make: Toyota
   - Model: Camry
   - Own or lease: Own
5. Answer additional questions with these defaults:
   - Currently insured: Yes
   - Any accidents/violations: No
   - Primary use: Commute to work
   - Miles per year: 12,000
6. Get to the quote results page showing the premium
7. Take a screenshot of the final quote

Note: Use reasonable defaults for any additional required fields.
"""

async def main():
    print("Starting Progressive insurance quote automation...")
    print("-" * 50)

    # Create the Browser Use agent
    agent = Agent(
        task=PROGRESSIVE_TASK,
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