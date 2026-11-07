from typing import TypedDict, Annotated, Sequence
from langgraph.graph import add_messages

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
