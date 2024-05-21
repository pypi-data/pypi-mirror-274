import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from agi_med_metrics.errors_nlp import cosine_similarity_score, bleu_score, rouge_score

refs = ['Тестовая строка', 'Тестовая строка', 'Тестовая строка']
preds = ['Тестовая строка', '', 'Тестовая']


def test_cosine_similarity_score():
    out = cosine_similarity_score(preds, refs)
    assert len(out) == len(refs)
    assert isinstance(out[0], float)
    assert int(round(out[0])) == 1
    assert int(round(out[1])) == 0
    assert all(0 <= item <= 1 for item in out)


def test_bleu_score():
    out = bleu_score(predictions=preds, references=refs)
    assert isinstance(out, float)
    assert 0 <= out <= 1
    
    
def test_rouge_score():
    out = rouge_score(predictions=preds, references=refs)
    assert isinstance(out, float)
    assert 0 <= out <= 1
    