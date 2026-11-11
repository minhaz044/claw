import asyncio
from workflow.supervisor_workflow import SupervisorWorkflow
from langchain_core.messages import HumanMessage

superior_workflow = SupervisorWorkflow()


async def run_agent():
    agent = superior_workflow.get_agent()
    try:
        while True:
            user_input = input(
                "\nWhat would you like me to do? "
                "(type 'exit' to quit): "
            ).strip()

            if user_input.lower() in {"exit", "quit"}:
                break

            if not user_input:
                continue

            try:
                await agent.ainvoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config={"recursion_limit": 50},
                )
            except Exception as error:
                print(f"Agent error: {error}")

    finally:
        print("Application exited.")


if __name__ == "__main__":
    asyncio.run(run_agent())
