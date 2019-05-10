import pandas, math, algorithms
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn import preprocessing


def accuracy_evaluation(data, dataSol):
    macs = list(set(data.MAC))
    le = preprocessing.LabelEncoder()
    le.fit(macs)
    
    trueLabels, predLabels = [-1 for i in range(len(macs))], [-1 for i in range(len(macs))]
    famInd = 0
    
    for key, value in dataSol.iterrows():
        for macNum in key:
            if not math.isnan(macNum):
                macNum = int(macNum)
                pos = le.transform([macNum])[0]
                trueLabels[pos] = famInd
        
        famInd += 1

    predFamilies = algorithms.slow_algorithm(data)
    famInd = 0

    for key, value in predFamilies.iteritems():
        for macNum in value:
            pos = le.transform([macNum])[0]
            predLabels[pos] = famInd

        famInd += 1

    print trueLabels
    print predLabels
    print adjusted_rand_score(trueLabels, predLabels)


def main():
    data = pandas.read_csv('datasets/recordings_example.csv', header=0, names=['Day', 'Hour', 'IP', 'MAC'])
    data = data.sort_values(by=['Day', 'Hour'])
    dataSol = pandas.read_csv('datasets/solution_1a_example.csv', header=None, names=[])
    
    accuracy_evaluation(data, dataSol) 


if __name__ == '__main__':
    main()

