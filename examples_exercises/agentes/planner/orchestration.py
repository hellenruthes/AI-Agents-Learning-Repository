from agents import Runner
from agent_planner import planner_agent
from agent_exec import executor_agent
import asyncio

async def main():
    user_request = "Analyze the sprint backlog and identify risks and recommendations"

    plan_result = await Runner.run(
        planner_agent,
        f"Create a plan for this request: {user_request}"
    )

    plan = plan_result.final_output
    print("\nGENERATED PLAN:\n")
    print(plan)

    exec_result = await Runner.run(
        executor_agent,
        f"""
        User request: {user_request}

        Generated plan:
        {plan}

        Now execute the analysis based on the backlog.
        """
    )

    print("\nFINAL RESPONSE:\n")
    print(exec_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())