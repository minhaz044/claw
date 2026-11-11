from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from domain.agent_state import AgentState
from models.llm_models import llm

from prompt.mouse_prompt import MOUSE_SYSTEM_MESSAGE
from tools.mouse_controller_tools_tools import mouse_tools

from langchain_core.messages import AIMessage

AGENT_NODE = "AGENT_NODE"
TOOLS_NODE = "tools"


class MouseWorkflow:

    def __init__(self):

        self.mouse_tools = mouse_tools

        # Prevent multiple mouse operations from running in parallel.
        self.llm = llm.bind_tools(
            self.mouse_tools,
            parallel_tool_calls=False
        )

    async def _mouse_agent_node(self, state: AgentState):

        messages = [
                       MOUSE_SYSTEM_MESSAGE
                   ] + list(state["messages"])

        response = await self.llm.ainvoke(messages)

        if response.tool_calls:
            for call in response.tool_calls:
                print(
                    f"AI requested tool: {call['name']} "
                    f"| arguments: {call['args']}"
                )
        else:
            print("AI:", response.text)

        return {"messages": [response]}

    def _mouse_should_continue(self, state: AgentState):
        """Run mouse tools if requested; otherwise finish."""

        last_message = state["messages"][-1]

        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return TOOLS_NODE

        return END

    def get_mouse_agent(self):

        graph = StateGraph(AgentState)

        # Nodes
        graph.add_node(
            AGENT_NODE,
            self._mouse_agent_node
        )

        graph.add_node(
            TOOLS_NODE,
            ToolNode(tools=self.mouse_tools)
        )

        # Entry point
        graph.add_edge(START, AGENT_NODE)

        # Conditional execution
        graph.add_conditional_edges(
            AGENT_NODE,
            self._mouse_should_continue,
            {
                TOOLS_NODE: TOOLS_NODE,
                END: END
            }
        )

        # Return to LLM after tool execution
        graph.add_edge(TOOLS_NODE, AGENT_NODE)

        return graph.compile()
