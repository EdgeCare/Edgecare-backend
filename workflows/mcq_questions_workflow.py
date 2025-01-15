from agents.keyword_extraction_agent import KeywordExtractionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.mcq_answer_generation_agent import McqAnswerGenerationAgent
from agents.manager_agent import ManagerAgent

from langgraph.graph import StateGraph, START
from schemas.agents import AgentState

# Initialize the StateGraph with the defined state schema
graph = StateGraph(AgentState)

# Add agent nodes
graph.add_node("Manager", ManagerAgent.manageMcqQuestions)
graph.add_node("KEA", KeywordExtractionAgent.extract_keywords)
graph.add_node("RA", RetrievalAgent.retrieve_documents)
graph.add_node("MCQA", McqAnswerGenerationAgent.generate_mcq_answer)

# Define edges to establish the workflow
graph.add_edge(START, "Manager")
graph.add_edge("KEA", "Manager")
graph.add_edge("RA", "Manager")
graph.add_edge("MCQA", "Manager")

print("main workflow Running")

# Compile the graph
compiled_mcq_answer_graph = graph.compile()

