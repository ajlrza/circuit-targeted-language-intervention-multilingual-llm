# CSI / M-index / I-index follow github.com/fxlrnrpt/language-steering-in-latent-space (MIT)
from collections import Counter


def csi(labels, target):
    return sum(l != target for l in labels) / len(labels) if labels else 0.0


def m_index(labels):
    if not labels:
        return 0.0
    counts = Counter(labels)
    if len(counts) <= 1:
        return 0.0
    n = len(labels)
    s = sum((c / n) ** 2 for c in counts.values())
    return (1 - s) / ((len(counts) - 1) * s)


def i_index(labels):
    if len(labels) <= 1:
        return 0.0
    return sum(labels[i] != labels[i - 1] for i in range(1, len(labels))) / (len(labels) - 1)


def first_switch(labels, target):
    return next((i for i, l in enumerate(labels) if l != target), None)


def repeated_ngram_rate(ids, n=4):
    grams = [tuple(ids[i:i + n]) for i in range(len(ids) - n + 1)]
    return 1 - len(set(grams)) / len(grams) if grams else 0.0


def summarize(labels, ids, target):
    return {
        "csi": csi(labels, target),
        "tlc": 1 - csi(labels, target),
        "m_index": m_index(labels),
        "i_index": i_index(labels),
        "first_switch": first_switch(labels, target),
        "rep4": repeated_ngram_rate(ids),
        "n_tokens": len(ids),
    }
