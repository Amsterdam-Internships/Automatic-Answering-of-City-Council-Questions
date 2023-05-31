def precision_k(results, relevant_docs, k):
    """
        Compute Precision@K
        Input:
            results: A sorted list of 2-tuples (document_id, score),
                    with the most relevant document in the first position
            relevant_docs: A set of relevant documents.
            k: the cut-off
        Output: Precision@K
    """
    if k > len(results):
        k = len(results)

    relevant_count = 0
    for i in range(k):
        if results[i][0] in relevant_docs: # check if result is in relevant
            relevant_count += 1

    k_precision = relevant_count / k

    return k_precision


def recall_k(results, relevant_docs, k):
    """
        Compute Recall@K
        Input:
            results: A sorted list of 2-tuples (document_id, score), with the most relevant document in the first position
            relevant_docs: A set of relevant documents.
            k: the cut-off
        Output: Recall@K
    """

    if k > len(results):
        k = len(results)

    relevant_count = 0
    for i in range(k):
        if results[i][0] in relevant_docs: # check if result is in relevant
            relevant_count += 1

    k_recall = float(relevant_count)/float(len(relevant_docs))

    return k_recall

def get_k_urls(bm25_results):
    urls = []
    counter = 1
    for result in bm25_results:

        urls.append((result['url'], result['score']))
        counter+=1
    return urls

def calculate_recall_at_k(queries, search_results, relevant_docs, k_values, ranking_method):
    """
    Calculate Recall@K for a list of queries and specified values of k.
    Input:
        queries - a list of queries
        collection: a list of tuples (document_id, document_content)
        relevant_docs: a dictionary where the key is the query and the value is a set of relevant document IDs
        k_values: a list of k values for recall calculation
    Output: a dictionary where the key is the query and the value is a dictionary of recall values at each k
    """
    recall_results = {}

    for query in queries:
        if ranking_method=='bm25':
            results = get_k_urls(search_results[query][1])
        elif ranking_method=='tf-idf':
            results = search_results[query]
        relevant = relevant_docs[query]

        recall_values = {}
        for k in k_values:
            recall = recall_k(results, relevant, k)
            recall_values[k] = recall

        recall_results[query] = recall_values

    return recall_results


def calculate_average_recall(recall_results):
    """
    Calculate the average recall values per recall type from a dictionary of recall values.
    Input:
        recall_results: a dictionary where the key is the query and the value is a dictionary of recall values at each k
    Output: a dictionary where the key is the recall type and the value is the average recall value
    """
    average_recall = {}

    for query_recall in recall_results.values():
        for k, recall in query_recall.items():
            if k not in average_recall:
                average_recall[k] = 0.0
            average_recall[k] += recall

    query_count = len(recall_results)
    for k in average_recall:
        average_recall[k] /= query_count

    return average_recall


#########################################################################################

def write_trec_run(results, outfn, tag="trecrun"):
    with open(outfn, "wt") as outf:
        qids = sorted(results.keys())
        for qid in qids:
            rank = 1
            for docid, score in sorted(results[qid], key=lambda x: x[1], reverse=True):
                print(f"{qid} Q0 {docid} {rank} {score} {tag}", file=outf)
                rank += 1


def evaluate_search_fn(method_name, search_fn, metric_fns, dh, queries, qrels, index_set=None):
    # build a dict query_id -> query
    queries_by_id = dict((q[0], q[1]) for q in queries)

    metrics = {}
    for metric, metric_fn in metric_fns:
        metrics[metric] = np.zeros(len(qrels), dtype=np.float32)

    q_results = {}
    for i, (query_id, relevant_docs) in enumerate(qrels.items()):
        query = queries_by_id[query_id]
        if index_set:
            results = search_fn(query, dh, index_set)
        else:
            results = search_fn(query, dh)
        
        q_results[query_id] = results
        for metric, metric_fn in metric_fns:
            metrics[metric][i] = metric_fn(results, relevant_docs)

    write_trec_run(q_results, f'{method_name}_{index_set}.trec')

    final_dict = {}
    for metric, metric_vals in metrics.items():
        final_dict[metric] = metric_vals.mean()

    return final_dict
