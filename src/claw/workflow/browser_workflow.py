from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from domain.agent_state import AgentState
from prompt.browser_prompt import BROWSER_SYSTEM_MESSAGE
from models.llm_models import llm
from langchain_core.messages import AIMessage
from tools.browser_tools import (
    browser_open_url,
    browser_inspect_page,
    browser_click_element,
    browser_type_into_element,
    browser_press_btn,
)

AGENT_NODE = 'AGENT_NODE'
TOOLS_NODE = 'tools'


class BrowserWorkflow:
    def __init__(self):
        self.browser_tools = [
            browser_open_url,
            browser_inspect_page,
            browser_click_element,
            browser_type_into_element,
            browser_press_btn,
        ]
        self.llm = llm

    async def _browser_agent_node(self, state: AgentState):
        print(state)
        messages = [BROWSER_SYSTEM_MESSAGE] + list(state["messages"])
        response = await self.llm.invoke(messages)

        if response.tool_calls:
            for call in response.tool_calls:
                print(
                    f"AI requested tool: {call['name']} "
                    f"| arguments: {call['args']}"
                )
        else:
            print("AI:", response.content)

        return {"messages": [response]}

    def _browser_should_continue(self, state: AgentState):
        """Run tools if requested; otherwise finish this task."""
        last_message = state["messages"][-1]

        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return TOOLS_NODE
        return END

    def get_browser_agent(self):
        # Build the graph
        graph = StateGraph(AgentState)

        graph.add_node(AGENT_NODE, self._browser_agent_node)
        graph.add_node(TOOLS_NODE, ToolNode(tools=self.browser_tools))

        graph.add_edge(START, AGENT_NODE)

        graph.add_conditional_edges(
            AGENT_NODE, self._browser_should_continue,
            {
                TOOLS_NODE: TOOLS_NODE,
                END: END,
            }
        )
        graph.add_edge(TOOLS_NODE, AGENT_NODE)

        return graph.compile()
