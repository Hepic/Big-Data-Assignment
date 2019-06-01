import math
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn import preprocessing


def jaccard_similarity(set1, set2):
    inter, union = len(set1.intersection(set2)), len(set1.union(set2))

    if union == 0:
        return 1.0

    sim = float(inter) / float(union)
    return sim


def jaccard_distance(set1, set2):
    return 1 - jaccard_similarity(set1, set2)


def accuracy_evaluation(data, dataSol, predFamilies):
    macs = list(set(data.MAC))
    le = preprocessing.LabelEncoder()
    le.fit(macs)

    trueLabels, predLabels = [-1 for i in range(len(macs))], [-1 for i in range(len(macs))]
    famInd = 0
    
    # labels of real solution
    for mac_str in dataSol:
        mac_list = map(int, mac_str.split(','))

        for mac_num in mac_list:
            pos = le.transform([mac_num])[0]
            trueLabels[pos] = famInd

        famInd += 1

    famInd = 0
    
    # labels of predicted solution
    for family_members in predFamilies:
        for mac_num in family_members:
            pos = le.transform([mac_num])[0]
            predLabels[pos] = famInd

        famInd += 1

    return adjusted_rand_score(trueLabels, predLabels)
