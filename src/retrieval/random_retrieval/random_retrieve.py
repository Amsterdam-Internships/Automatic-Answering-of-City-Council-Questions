import random

def retrieve_document(collection, k):
    shuffled_collection = collection[:]  # Create a copy of the collection
    random.shuffle(shuffled_collection)
    return shuffled_collection[:k]  # Return only the first k documents


def perform_random_search(queries, collection, k):
    """
    Perform Random search for each query in a list of queries.
    Input:
        queries - a list of queries
        collection: a list of tuples (document_id, document_content)
        k: the number of documents to retrieve for each query
    Output: a dictionary where the key is the query and the value is a list of (document_id, score) tuples
    """
    search_results = {}

    for query in queries:
        results = retrieve_document(collection, k)
        search_results[query] = results

    return search_results
