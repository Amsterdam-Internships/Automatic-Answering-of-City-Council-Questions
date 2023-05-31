from elasticsearch import Elasticsearch


def set_index(mappings, es_client, collected):

    es_client.indices.delete(index="qa_attempt1", ignore=[400, 404])
    es_client.indices.create(index="qa_attempt1", mappings=mappings)

    for i, row in collected.iterrows():
        doc = {
            "url": row["URL"],
            "text": str(row["Textual_Content"])
        }
                
        es_client.index(index="qa_attempt1", id=i, document=doc)

    return es_client



def query_es_index(question, es_client, index_name="qa_attempt1", n_results=10, min_length=20):
    """
    Perform a search query on an Elasticsearch index based on a provided question.
    """
    q = question.lower()
    banned = [] #["how", "why", "what", "where", "which", "do", "does", "is", "?", "eli5", "eli5:"]
    #q = " ".join([w for w in q.split() if w not in banned])
    response = es_client.search(
        index=index_name,
        body={
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["url", "text"],
                    "type": "cross_fields",
                }
            },
            "size": 2 * n_results,
        },
    )
    hits = response["hits"]["hits"]
    support_doc = "<P> " + hits[0]["_source"]["text"] if hits else ""
    res_list = [
        {
            k: hit["_source"][k]
            for k in hit["_source"]
            if k != "passage_text"
        }
        for hit in hits
    ]
    for r, hit in zip(res_list, hits):
        r["passage_id"] = hit["_id"]
        r["score"] = hit["_score"]
        r["passage_text"] = hit["_source"]["text"]
    res_list = [
        res
        for res in res_list
        if len(res["passage_text"].split()) > min_length
    ][:n_results]
    return support_doc, res_list

def get_result_tuples(es_client, questions, index_name='qa_attempt1'):

    results = {}  # To store the results for all questions

    for question in questions:
        doc, res_list = query_es_index(question, es_client, index_name=index_name)
        results[question] = (doc, res_list)  # it took 9 seconds to finish 
    
    return results

