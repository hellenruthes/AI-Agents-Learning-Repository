import asyncio
from dotenv import load_dotenv
from agents import Runner
from agent_react import react_agent

load_dotenv()

async def main():
    print("1. Entered main")
    print("2. Calling Runner")

    result = await Runner.run(
        react_agent,
        "Analyze ticket 1001"
    )

    print("3. Runner finished")
    print("\nFINAL RESPONSE:\n")
    print(result.final_output)

if __name__ == "__main__":
    print("0. Starting script")
    asyncio.run(main())