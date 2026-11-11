from src.claw.tools.supervisor_tools import supervisor_tools
from src.claw.models.llm_models import llm
from src.claw.domain.agent_state import AgentState
from src.claw.prompt.supervisor_prompt import SUPERVISOR_SYSTEM_MESSAGE, TOOLS_NODE, AGENT_NODE
from langchain_core.messages import AIMessage
from langgraph.constants import START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph


class SupervisorWorkflow:

    def __init__(self):
        self.tools = supervisor_tools
        self.llm = llm.bind_tools(
            self.tools,
            parallel_tool_calls=False
        )

    async def _agent_node(self, state: AgentState):
        messages = [
                       SUPERVISOR_SYSTEM_MESSAGE
                   ] + list(state["messages"])

        response = await self.llm.ainvoke(messages)

        if response.tool_calls:
            for call in response.tool_calls:
                print(
                    f"Agent: {call['name']} "
                    f"| Arguments: {call['args']}"
                )
        else:
            print("Supervisor:", response.content)

        return {"messages": [response]}

    def _should_continue(self, state: AgentState):
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return TOOLS_NODE
        return END

    def get_agent(self):
        graph = StateGraph(AgentState)
        graph.add_node(
            AGENT_NODE,
            self._agent_node
        )

        graph.add_node(
            TOOLS_NODE,
            ToolNode(tools=self.tools)
        )

        graph.add_edge(START, AGENT_NODE)
        graph.add_conditional_edges(
            AGENT_NODE,
            self._should_continue,
            {
                TOOLS_NODE: TOOLS_NODE,
                END: END
            }
        )
        graph.add_edge(TOOLS_NODE, AGENT_NODE)
        return graph.compile()
