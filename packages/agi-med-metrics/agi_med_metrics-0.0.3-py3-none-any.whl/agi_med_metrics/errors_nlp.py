from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from typing import List

import evaluate

bleu = evaluate.load('bleu')
rouge = evaluate.load('rouge')
encoder = SentenceTransformer('multi-qa-distilbert-cos-v1')


def bleu_score(predictions, references):
    return bleu.compute(predictions=predictions, references=references)['bleu']


def rouge_score(predictions, references, metric='rouge1'):
    return rouge.compute(predictions=predictions, references=references)[metric]


def cosine_similarity_score(predictions: List[str], references: List[str]) -> list:
    assert isinstance(predictions, list) and isinstance(references, list), 'Wrong input format!'
    embs_true = encoder.encode(references)
    embs_pred = encoder.encode(predictions)
    return cos_sim(embs_true, embs_pred).diagonal().tolist()
