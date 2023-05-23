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
