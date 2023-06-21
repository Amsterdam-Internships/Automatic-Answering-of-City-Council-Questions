from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import random
from rank_bm25 import BM25Okapi
import heapq

#######################################################################

############################ TF-IDF ###################################

#######################################################################

def tfidf_search(query, vectorizer, matrix, collection, k):
    """
    Perform a search over all documents with the given query using tf-idf.
    Input:
        query - an (unprocessed) query
        vectorizer: a fitted TfidfVectorizer
        matrix: the document-term matrix obtained from the fitted vectorizer
        collection: a list of tuples (document_id, document_content)
        k: the number of top search results to retrieve
    Output: a list of (document_id, score, document_content), sorted in descending relevance to the given query
    """
    preprocessed_query = str(query['Preprocessed_Question'])

    true_documents = query['passages_ids']

    query_vector = vectorizer.transform([preprocessed_query])
    question_id = query['question_id']

    # NearestNeighbors to find the k nearest neighbors
    nn = NearestNeighbors(n_neighbors=k, metric='cosine')
    nn.fit(matrix)

    # find nearest neighbors
    distances, indices = nn.kneighbors(query_vector)

    results = []  

    for idx, distance in zip(indices[0], distances[0]):
        doc_id = collection[int(idx)]['id']
        document_content = collection[int(idx)]['Textual_Content']
        document_content_preprocessed = collection[int(idx)]['Preprocessed_Text']
        results.append((doc_id, distance, document_content_preprocessed, document_content))

    results.sort(key=lambda x: x[1])  # sort
    top_results = results[:k]

    cosine_scores = [result[1] for result in top_results]
    ranked_ids = [result[0] for result in top_results]
    ranked_preprocessed = [result[2] for result in top_results]
    ranked_text = [result[3] for result in top_results]

    # dictionary with search results
    search_results = {
        'question_id': question_id,
        'question': query['Question'],
        'ranked_ids': ranked_ids,
        'ranked_text_preprocessed': ranked_preprocessed,
        'ranked_text': ranked_text,
        'true_passages': true_documents,
        'cosine_scores': cosine_scores, 
        'answer': query['Answer'],
        'preprocessed_question': query['Preprocessed_Question'],
        'preprocessed_answer': query['Preprocessed_Answer']
    }

    return search_results 

def perform_tfidf_search(queries, collection, k):
    """
    Perform TF-IDF search for each query in a list of queries.
    Input:
        queries - questions of type Dataset
        collection: collection of type Dataset
        k: the number of top search results to retrieve
    Output: a list of dictionaries with the following keys: 
        {'question_id': question_id,
        'question': query['Question'],
        'ranked_ids': ranked_ids,
        'ranked_text_preprocessed': ranked_preprocessed,
        'ranked_text': ranked_text,
        'true_passages': true_documents,
        'cosine_scores': cosine_scores, 
        'answer': query['Answer'],
        'preprocessed_question': query['Preprocessed_Question'],
        'preprocessed_answer': query['Preprocessed_Answer']
    }
    """
    document_contents = [doc['Preprocessed_Text'] for doc in collection]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(document_contents) # vectorize collection

    search_results = []

    for query in queries: # rank for each query
        results = tfidf_search(query, vectorizer, matrix, collection, k=k) 
        search_results.append(results)

    return search_results

#######################################################################

############################ Random ###################################

#######################################################################

def random_search(query, collection, k):
    """
    Perform Random 'search' (sampling) for each query in a list of queries.
    Input:
        queries - questions of type Dataset
        collection: collection of type Dataset
        k: the number of top search results to retrieve
    Output: a list of dictionaries with the following keys: 
        {'question_id': question_id,
        'question': query['Question'],
        'ranked_ids': ranked_ids,
        'ranked_text_preprocessed': ranked_preprocessed,
        'ranked_text': ranked_text,
        'true_passages': true_documents,
        'cosine_scores': cosine_scores, 
        'answer': query['Answer'],
        'preprocessed_question': query['Preprocessed_Question'],
        'preprocessed_answer': query['Preprocessed_Answer']
    }
    """
    true_documents = query['passages_ids']

    # randomly select k documents from the collection
    random_results = random.sample(collection.to_list(), k)

    ranked_ids = [result['id'] for result in random_results]
    ranked_text = [result['Textual_Content'] for result in random_results]
    ranked_preprocessed = [result['Preprocessed_Text'] for result in random_results]
    scores = []  # Assign random scores for demonstration purposes

    # dictioanry with search results
    search_results = {
        'question_id': query['question_id'],
        'question': query['Question'],
        'ranked_ids': ranked_ids,
        'ranked_text_preprocessed': ranked_preprocessed,
        'ranked_text': ranked_text,
        'true_passages': true_documents,
        'scores': scores,
        'answer': query['Answer'],
        'preprocessed_question': query['Preprocessed_Question'],
        'preprocessed_answer': query['Preprocessed_Answer']
    }

    return search_results


def perform_random_search(queries, collection, k):
    """
    Perform random retrieval search for each query in a list of queries.
    Input:
        queries - a list of queries
        collection: a pandas DataFrame representing the collection
        k: the number of top search results to retrieve
    Output: a list of dictionaries containing the search results
    """
    search_results = []

    for query in queries:
        results = random_search(query, collection, k=k)
        search_results.append(results)

    return search_results


#######################################################################

############################# BM25 ####################################

#######################################################################

def bm25_search(query, corpus, bm25, k):
    """
    Perform a search over all documents with the given query using BM25 ranking.
    Input:
        query - an (unprocessed) query
        collection: a list of document contents
        bm25: initialized BM25Okapi object
        k: the number of top search results to retrieve
    Output: a list of (document_id, score, document_content), sorted in descending relevance to the given query
    """
    # Preprocess the query
    preprocessed_query = str(query['Preprocessed_Question'])
    query_tokens = preprocessed_query.split()

    scores = bm25.get_scores(query_tokens)

    results_heap = []

    # Iterate over the corpus and update the heap with the top-k results
    for i, doc in enumerate(corpus):
        doc_id = doc['id']
        score = scores[i]
        document_content = doc['Textual_Content']
        document_content_preprocessed = doc['Preprocessed_Text']
        heapq.heappush(results_heap, (score, doc_id, document_content, document_content_preprocessed))
        if len(results_heap) > k:
            heapq.heappop(results_heap)

    results_heap.sort(reverse=True)  # Sort descending
    top_results = results_heap[:k]

    bm25_scores = [result[0] for result in top_results]
    ranked_ids = [result[1] for result in top_results]
    ranked_text = [result[2] for result in top_results]
    ranked_preprocessed = [result[3] for result in top_results]

    # Create a dictionary containing the search results

    query_text = query['Question']
    true_documents = query['passages_ids']
    question_id = query['question_id']

    search_results = {
    'question_id': question_id,
    'question': query_text,
    'ranked_ids': ranked_ids,
    'ranked_text_preprocessed': ranked_preprocessed,
    'ranked_text': ranked_text,
    'true_passages': true_documents,
    'scores': bm25_scores, 
    'answer': query['Answer'],
    'preprocessed_question': query['Preprocessed_Question'],
    'preprocessed_answer': query['Preprocessed_Answer']
    }

    return search_results

def perform_bm25_search(queries, corpus, k):
    """
    Perform BM25 Okapi search for each query in a list of queries.
    Input:
        queries - questions of type Dataset
        collection: collection of type Dataset
        k: the number of top search results to retrieve
    Output: a list of dictionaries with the following keys: 
        {'question_id': question_id,
        'question': query['Question'],
        'ranked_ids': ranked_ids,
        'ranked_text_preprocessed': ranked_preprocessed,
        'ranked_text': ranked_text,
        'true_passages': true_documents,
        'cosine_scores': cosine_scores, 
        'answer': query['Answer'],
        'preprocessed_question': query['Preprocessed_Question'],
        'preprocessed_answer': query['Preprocessed_Answer']
    }
    """
    # tokenize corpus
    tokenized_corpus = [doc['Preprocessed_Text'].split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)

    search_results = []

    for query in queries:
        results = bm25_search(query, corpus, bm25, k=k)
        search_results.append(results)

    return search_results
