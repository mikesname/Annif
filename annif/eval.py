"""Evaluation metrics for Annif"""

import collections
import functools
import statistics
import warnings
import numpy
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import precision_score, recall_score, f1_score


def sklearn_metric_score(selected, relevant, metric_fn):
    """call a sklearn metric function, converting the selected and relevant
       subjects into the multilabel indicator arrays expected by sklearn"""
    mlb = MultiLabelBinarizer()
    mlb.fit(list(relevant) + list(selected))
    y_true = mlb.transform(relevant)
    y_pred = mlb.transform(selected)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return metric_fn(y_true, y_pred, average='samples')


def precision(selected, relevant, at_k=None):
    """return the precision, i.e. the fraction of selected instances that
    are relevant"""
    if at_k is not None:
        selected = [subjs[:at_k] for subjs in selected]
    return sklearn_metric_score(selected, relevant, precision_score)


def recall(selected, relevant):
    """return the recall, i.e. the fraction of relevant instances that were
    selected"""
    return sklearn_metric_score(selected, relevant, recall_score)


def f_measure(selected, relevant):
    """return the F-measure similarity of two sets"""
    return sklearn_metric_score(selected, relevant, f1_score)


def true_positives(selected, relevant):
    """return the number of true positives, i.e. how many selected instances
    were relevant"""
    count = 0
    for ssubj, rsubj in zip(selected, relevant):
        sel = set(ssubj)
        rel = set(rsubj)
        count += len(sel & rel)
    return count


def false_positives(selected, relevant):
    """return the number of false positives, i.e. how many selected instances
    were not relevant"""
    count = 0
    for ssubj, rsubj in zip(selected, relevant):
        sel = set(ssubj)
        rel = set(rsubj)
        count += len(sel - rel)
    return count


def false_negatives(selected, relevant):
    """return the number of false negaives, i.e. how many relevant instances
    were not selected"""
    count = 0
    for ssubj, rsubj in zip(selected, relevant):
        sel = set(ssubj)
        rel = set(rsubj)
        count += len(rel - sel)
    return count


def dcg(selected, relevant, at_k):
    """return the discounted cumulative gain (DCG) score for the selected
    instances vs. relevant instances"""
    if len(selected) == 0 or len(relevant) == 0:
        return 0.0
    scores = numpy.array([int(item in relevant)
                          for item in list(selected)[:at_k]])
    weights = numpy.log2(numpy.arange(2, scores.size + 2))
    return numpy.sum(scores / weights)


def normalized_dcg(selected, relevant, at_k):
    """return the normalized discounted cumulative gain (nDCG) score for the
    selected instances vs. relevant instances"""

    scores = []
    for ssubj, rsubj in zip(selected, relevant):
        dcg_val = dcg(ssubj, rsubj, at_k)
        dcg_max = dcg(rsubj, rsubj, at_k)
        if dcg_max == 0.0:
            scores.append(0.0)
        else:
            scores.append(dcg_val / dcg_max)
    return statistics.mean(scores)


def evaluate(samples):
    """evaluate a set of selected subject against a gold standard using
    different metrics"""

    metrics = [
        ('Precision', precision),
        ('Recall', recall),
        ('F-measure', f_measure),
        ('NDCG@5', functools.partial(normalized_dcg, at_k=5)),
        ('NDCG@10', functools.partial(normalized_dcg, at_k=10)),
        ('Precision@1', functools.partial(precision, at_k=1)),
        ('Precision@3', functools.partial(precision, at_k=3)),
        ('Precision@5', functools.partial(precision, at_k=5)),
        ('True positives', true_positives),
        ('False positives', false_positives),
        ('False negatives', false_negatives)
    ]

    results = collections.OrderedDict()
    for metric_name, metric_fn in metrics:
        hits, gold_subjects = zip(*samples)
        results[metric_name] = metric_fn(hits, gold_subjects)
    return results


def transform_sample(sample):
    """transform a single document (sample) with predicted and gold standard
       subjects into either sequences of URIs (if available) or sequences of
       labels"""
    hits, gold_subjects = sample
    if gold_subjects.has_uris():
        selected = [hit.uri for hit in hits]
        gold_set = gold_subjects.subject_uris
    else:
        selected = [hit.label for hit in hits]
        gold_set = gold_subjects.subject_labels
    return (selected, gold_set)


class EvaluationBatch:
    """A class for evaluating batches of results using all available metrics.
    The evaluate() method is called once per document in the batch.
    Final results can be queried using the results() method."""

    def __init__(self):
        self._samples = []

    def evaluate(self, hits, gold_subjects):
        self._samples.append((hits, gold_subjects))

    def results(self):
        transformed_samples = [transform_sample(sample)
                               for sample in self._samples]
        return evaluate(transformed_samples)
