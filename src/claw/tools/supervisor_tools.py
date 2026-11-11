from langchain_core.tools import tool

from src.claw.workflow.browser_workflow import BrowserWorkflow
from src.claw.workflow.mouse_workflow import MouseWorkflow

browser_agent = BrowserWorkflow().get_browser_agent()
mouse_agent = MouseWorkflow().get_mouse_agent()


@tool
async def browser_specialist(task: str) -> str:
    """
    Delegate website and browser operations to the Browser Agent.

    Use this for opening websites, inspecting pages,
    clicking HTML elements, typing and creating documents.
    """

    result = await browser_agent.ainvoke({
        "messages": [
            {"role": "user", "content": task}
        ]
    })

    return str(result["messages"][-1].content)


@tool
async def mouse_specialist(task: str) -> str:
    """
    Delegate visual mouse operations to the Mouse Agent.

    Use this for mouse movement, clicking, dragging,
    drawing and interacting with visual interfaces.
    """

    result = await mouse_agent.ainvoke({
        "messages": [
            {"role": "user", "content": task}
        ]
    })

    return str(result["messages"][-1].content)


supervisor_tools = [
    browser_specialist,
    mouse_specialist
]
