import math
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn import preprocessing


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
    for key, value in predFamilies.iteritems():
        for mac_num in value:
            pos = le.transform([mac_num])[0]
            predLabels[pos] = famInd

        famInd += 1

    print adjusted_rand_score(trueLabels, predLabels)
