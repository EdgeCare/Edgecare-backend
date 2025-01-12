from agents.keyword_extraction_agent import KeywordExtractionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.question_answering_agent import QuestionAnsweringAgent
from agents.manager_agent import ManagerAgent

from langgraph.graph import StateGraph, START, END
from schemas.agents import AgentState

# Initialize the StateGraph with the defined state schema
graph = StateGraph(AgentState)

# Add agent nodes
graph.add_node("Manager", ManagerAgent.manage)
graph.add_node("KEA", KeywordExtractionAgent.extract_keywords)
graph.add_node("RA", RetrievalAgent.retrieve_documents)
graph.add_node("QAA", QuestionAnsweringAgent.answer_question)

# Define edges to establish the workflow
graph.add_edge(START, "Manager")
graph.add_edge("Manager", "KEA")
graph.add_edge("KEA", "Manager")
graph.add_edge("Manager", "RA")
graph.add_edge("RA", "Manager")
graph.add_edge("Manager", "QAA")
graph.add_edge("QAA", "Manager")
graph.add_edge("Manager", END)

# graph.add_conditional_edges("QAA", needs_refinement)
print("main workflow Running")
# Compile the graph
compiled_graph = graph.compile()

