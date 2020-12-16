
def f1_score(labels, preds):
    tp = 0
    for label in labels:
        if preds.__contains__(label):
            tp += 1

    if tp == 0:
        return 0

    recall = tp / len(labels)
    precision = tp / len(preds)

    f1 = 2 * recall * precision / (recall + precision)
    return f1


def rankscore(labels, preds, alpha=2):
    hits = []
    for idx, pred in enumerate(preds):
        if labels.__contains__(pred):
            hits.append(idx)

    p = 0
    max_ = 0
    for i, idx in enumerate(hits):
        p += 1 / (2 ** (idx / alpha))
        max_ += 1 / (2 ** (i / alpha))

    if max_ == 0:
        return 0

    return p / max_


def avg_precision(labels, preds):
    hits = []
    for idx, pred in enumerate(preds):
        if labels.__contains__(pred):
            hits.append(idx + 1)

    if len(hits) == 0:
        return 0

    ap = 0
    for i, idx in enumerate(hits):
        ap += (i + 1) / idx

    return ap / len(hits)
