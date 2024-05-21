from agi_med_metrics import *
from agi_med_metrics.errors_nlp import cosine_similarity_score, bleu_score, rouge_score

refs = ['Тестовая строка', 'Тестовая строка', 'Тестовая строка']
preds = ['Тестовая строка', '', 'Тестовая']


def test_cosine_similarity_score():
    print(cosine_similarity_score(preds, refs))


def test_bleu_score():
    print(bleu_score(predictions=preds, references=refs))
    
    
def test_rouge_score():
    print(rouge_score(predictions=preds, references=refs))
    
    
if __name__=='__main__':
    test_cosine_similarity_score()
    test_bleu_score()
    test_rouge_score()