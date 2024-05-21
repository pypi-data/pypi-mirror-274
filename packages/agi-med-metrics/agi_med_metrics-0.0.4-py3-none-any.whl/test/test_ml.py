from agi_med_metrics.errors_ml import false_negative_rate_score, false_positive_rate_score

refs = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
preds = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0]


def test_fpr():
    out = false_positive_rate_score(y_pred=preds, y_true=refs)
    assert isinstance(out, float)
    assert 0 <= out <= 1
    assert round(out*len(refs)) == 2
    
def test_fnr():
    out = false_negative_rate_score(y_pred=preds, y_true=refs)
    assert isinstance(out, float)
    assert 0 <= out <= 1
    assert round(out*len(refs)) == 2
