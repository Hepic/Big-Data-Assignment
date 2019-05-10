def jaccard_similarity(set1, set2):
    set1, set2 = set(set1), set(set2)
    inter, union = len(set1.intersection(set2)), len(set1.union(set2))

    if union == 0:
        return 1.0

    sim = float(inter) / float(union)
    return sim


def jaccard_distance(set1, set2):
    return 1 - jaccard_similarity(set1, set2)
