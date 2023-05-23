from elasticsearch import Elasticsearch

def bm25_elasticsearch(passages, queries):
    es = Elasticsearch(hosts=["http://localhost:9200"])

    # Index configuration
    index_name = "passages_index"

    # Check if the index already exists
    if not es.indices.exists(index=index_name):
        # Create the index with BM25 similarity
        es.indices.create(index=index_name, body={"settings": {"index": {"similarity": {"default": {"type": "BM25"}}}}})
    
        # Index the passages
        for i, passage in enumerate(passages):
            passage_id = f"{passage['id']}_{i}"  # Append a unique identifier to the ID
            es.index(index=index_name, id=passage_id, body={
                #"original_id": passage['id'],
                "content": passage['content']
            })

        # Refresh the index to make the documents searchable
        es.indices.refresh(index=index_name)

    results = []
    # Perform the search for each query
    for query in queries:
        # Formulate the search query
        search_body = {
            "query": {
                "match": {
                    "content": query
                }
            }
        }

        # Execute the search
        response = es.search(index=index_name, body=search_body)

        # Store the search results in a list of dictionaries
        for hit in response["hits"]["hits"]:
            score = hit["_score"]
            passage_id = hit["_id"]
            passage = hit["_source"]
            original_id = passage["original_id"]  # Retrieve the original passage ID
            results.append({"id": passage_id, "content": passage["content"], "score": score}) # "original_id": original_id

    return results





# Print the stored results
"""for result in results:
    print(f"Passage ID: {result['id']}")
    print(f"Original ID: {result['original_id']}")
    print(f"Content: {result['content']}")
    print(f"Score: {result['score']}\n") """
