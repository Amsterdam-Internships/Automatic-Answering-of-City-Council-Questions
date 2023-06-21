from irmetrics.topk import recall, ap, ndcg, precision, rr, precision
import warnings
import numpy as np 
from irmetrics.relevance import relevant_counts
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import corpus_bleu
from sklearn.metrics import f1_score
from nltk.translate.bleu_score import SmoothingFunction
from nltk import word_tokenize

def calculate_average_metrics_retrieval(results, k):
    recall_scores = []
    ndcg_scores = []
    rr_scores = []
    precision_scores = []

    for result in results:
        ranked = result['ranked_ids']
        relevant = result['true_passages']

        recall_k = recall(relevant, ranked, k)
        ndcg_k = calculate_ndcg(relevant, ranked, k)
        rr_k = rr(relevant, ranked, k)
        precision_k = precision(relevant, ranked, k)

        recall_scores.append(recall_k)
        ndcg_scores.append(ndcg_k)
        rr_scores.append(rr_k)
        precision_scores.append(precision_k)

    average_recall = sum(recall_scores) / len(recall_scores)
    average_ndcg = sum(ndcg_scores) / len(ndcg_scores)
    average_rr = sum(rr_scores) / len(rr_scores)
    average_precision = sum(precision_scores) / len(precision_scores)

    average_metrics = {
        'average_recall@{}'.format(k): average_recall,
        'average_ndcg@{}'.format(k): average_ndcg,
        'average_rr@{}'.format(k): average_rr,
        'average_precision@{}'.format(k): average_precision
    }

    return average_metrics


def calculate_ndcg(relevant, ranked, k):
    warnings.filterwarnings('ignore', 'invalid value encountered', RuntimeWarning)
    ndcg_k = ndcg(relevant, ranked, k)
    if np.isnan(ndcg_k) or np.isinf(ndcg_k):
        ndcg_k = 0.0
    return ndcg_k

#relevant_counts(relevant[:, np.newaxis], ranked[:, np.newaxis])


def calculate_metrics_answer_similarity(generated_answers, reference_answers):
    # Convert non-string elements to strings
    generated_answers = [str(answer) for answer in generated_answers]
    reference_answers = [str(answer) for answer in reference_answers]


    # Compute ROUGE scores
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    rouge_scores = []
    for generated_ans, reference_ans in zip(generated_answers, reference_answers):
        scores = scorer.score(generated_ans, reference_ans)
        rouge_scores.append(scores)

    # Compute BLEU score
    bleu_score = corpus_bleu([[ref.split()] for ref in reference_answers], [gen.split() for gen in generated_answers], smoothing_function=SmoothingFunction().method1)

    # Compute F1 score
    f1 = f1_score(reference_answers, generated_answers, average='micro')  # Adjust 'average' parameter as needed


    # Access the scores as needed
    metrics = {
        "ROUGE-1 (Average)": sum([score['rouge1'].fmeasure for score in rouge_scores]) / len(rouge_scores),
        "ROUGE-2 (Average)": sum([score['rouge2'].fmeasure for score in rouge_scores]) / len(rouge_scores),
        "ROUGE-L (Average)": sum([score['rougeL'].fmeasure for score in rouge_scores]) / len(rouge_scores),
        "BLEU Score": bleu_score,
        "F1 Score": f1
    }

    return metrics

def simulate_answer(list_passages):
    concatenated_string = ""  # Initialize the concatenated string
    for paragraph in list_passages:
        tokens = word_tokenize(paragraph)
        if len(word_tokenize(concatenated_string)) + len(tokens) <= 256:
            concatenated_string += " " + paragraph
        else:
            break  # Stop concatenating if the token count exceeds 256
    return concatenated_string

