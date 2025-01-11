# from langgraph import Node, Graph
from agents.keyword_extraction_agent import KeywordExtractionAgent
from agents.rag_agent import RetrievalAgent
from agents.question_answering_agent import QuestionAnsweringAgent
from agents.manager_agent import ManagerAgent

def main_workflow(query: str) -> str:
    # # Define agent nodes
    # manager_node = Node(name="Manager",function=ManagerAgent.manage)
    # keyword_extraction_node = Node(name="Keyword Extraction", function=KeywordExtractionAgent.extract_keywords)
    # retrieval_node = Node(name="Rag", function=RetrievalAgent.retrieve_documents)
    # qa_node = Node(name="Q&A", function=QuestionAnsweringAgent.answer_question)

    # # Build agent graph
    # graph = Graph()
    # graph.add_node(manager_node)
    # graph.add_node(keyword_extraction_node)
    # graph.add_node(rag_node)
    # graph.add_node(qa_node)

    # # Edges
    # graph.add_edge(manager_node, keyword_extraction_node)
    # graph.add_edge(manager_node, rag_node)
    # graph.add_edge(manager_node, qa_node)
    # graph.add_edge(keyword_extraction_node, rag_node)


    # # Run workflow
    # result = graph.run(input_data=query)
    # return result
    return "Done"
