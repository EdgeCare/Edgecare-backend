from pydantic import BaseModel
from typing import Optional
from schemas.agents import AgentState
from utils.openaiClient import retrieval_system

def retrieve_top_snippets(queries, retriever_name="MedCPT", corpus_name="Textbooks", db_dir="./rag/corpus", total_k=32, min_snippets_per_query=2):
    """
    Retrieve top snippets for multiple queries, ensuring at least a minimum number of snippets per query.

    Args:
        queries (List[str]): List of query strings.
        retriever_name (str): Name of the retriever system.
        corpus_name (str): Name of the corpus to search within.
        db_dir (str): Directory containing the database.
        total_k (int): Total number of snippets to retrieve across all queries.
        min_snippets_per_query (int): Minimum number of snippets to retrieve for each query.

    Returns:
        List[Dict]: Retrieved snippets sorted by score.
    """
    all_snippets = []
    query_snippets = []

    # Retrieve snippets for each query
    for query in queries:
        snippets, scores = retrieval_system.retrieve(query, k=total_k, rrf_k=100)
        
        # Combine snippets and scores into dictionaries
        all_snippets.extend([{"snippet": snippet, "score": score} for snippet, score in zip(snippets, scores)])
        query_snippets.extend(sorted([{"snippet": snippet, "score": score} for snippet, score in zip(snippets, scores)], 
                                     key=lambda x: x["score"], reverse=True)[:min_snippets_per_query])
    
    # Remove duplicates based on "id"
    unique_snippets = {}
    for snippet in all_snippets:
        unique_snippets[snippet["snippet"]["id"]] = snippet  # Use 'id' as the unique key
    all_snippets = list(unique_snippets.values())

    unique_snippets = {}
    for snippet in query_snippets:
        unique_snippets[snippet["snippet"]["id"]] = snippet  # Use 'id' as the unique key
    query_snippets = list(unique_snippets.values())

    # Subtract query_snippets from all_snippets
    ids_in_query_snippets = {snippet["snippet"]["id"] for snippet in query_snippets}
    all_snippets = [snippet for snippet in all_snippets if snippet["snippet"]["id"] not in ids_in_query_snippets]

    # Sort remaining snippets by score
    all_snippets = sorted(all_snippets, key=lambda x: x["score"], reverse=True)

    # Select top snippets
    top_snippets = all_snippets[:total_k - min_snippets_per_query * len(queries)]
    top_snippets = top_snippets + query_snippets

    return top_snippets


class RetrievalAgent:
    @staticmethod
    def retrieve_documents(state: AgentState) -> dict:
        print("🤖 Retrieval Agent Running")

        retrieved_snippets = retrieve_top_snippets(state.keywords)
        retrieved_snippets =  [entry['snippet']['content'] for entry in retrieved_snippets]
        # print(retrieved_snippets)
        
        return {"documents": retrieved_snippets}

