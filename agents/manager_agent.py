from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from schemas.agents import AgentState

class ManagerAgent:
    @staticmethod
    def manageMainFlow(state: AgentState) -> Command[Literal["KEA", "RA", "QAA","Persona","FQA", END]]:
        if state.answer:
            print("\nProcess Complete!\n")
            return Command(goto=END)

        elif not state.keywords:
            print("\n🕵️ Invoking Keyword Extraction Agent")
            return Command(goto="KEA")
        
        elif not state.documents:
            print("\n🕵️ Invoking Retrieval Agent")
            return Command(goto="RA")
        
        elif not state.answer:
            print("\n🕵️ Invoking Question Answering Agent")
            return Command(goto="QAA")
        
        # not state.answer:
        print("\n🕵️ Invoking Question Answering Agent")
        return Command(goto="QAA")

    @staticmethod
    def manageMcqQuestions(state: AgentState) -> Command[Literal["KEA", "RA", "MCQA", END]]:
        if not state.keywords:
            print("\n🕵️ Invoking Keyword Extraction Agent")
            return Command(goto="KEA")
        elif not state.documents:
            print("\n🕵️ Invoking Retrieval Agent")
            return Command(goto="RA")
        elif not state.answer:
            print("\n🕵️ Invoking MCQ Question Answering Agent")
            return Command(goto="MCQA")
        else:
            print("\nProcess Complete!\n")
            # print("state =", state)
            return Command(goto=END)