import random

def retrieve_document(collection):
    random.seed(42)
    shuffled_collection = random.shuffle(collection)
    return shuffled_collection


