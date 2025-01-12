from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from schemas.agents import AgentState

class ManagerAgent:
    @staticmethod
    def manage(state: AgentState) -> Command[Literal["KEA", "RA", "QAA", END]]:
        print("Manager Agent Running",state)
        if not state.keywords:
            return Command(goto="KEA")
        elif not state.documents:
            return Command(goto="RA")
        elif not state.answer:
            return Command(goto="QAA")
        else:
            return Command(goto=END)
