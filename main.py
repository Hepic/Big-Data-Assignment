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
    
    predFamiliesList = [[] for i in range(len(macs))]
    predFamilies = algorithms.slow_algorithm(data)
    famInd = 0

    for key, value in predFamilies.iteritems():
        for macNum in value:
            pos = le.transform([macNum])[0]

            if len(value) >= 3:
                predLabels[pos] = famInd
                predFamiliesList[famInd].append(macNum)

        famInd += 1

    print adjusted_rand_score(trueLabels, predLabels)
   
    print trueLabels
    print
    print predLabels

    dataPred = pandas.DataFrame(predFamiliesList)
    dataPred = dataPred.fillna(-1)
    dataPred = dataPred.astype(int)
    dataPred.to_csv('datasets/solution_1a.csv', index=False, header=None)


def main():
    data = pandas.read_csv('datasets/recordings_example.csv', header=0, names=['Day', 'Hour', 'IP', 'MAC'])
    data = data.sort_values(by=['Day', 'Hour'])
    dataSol = pandas.read_csv('datasets/solution_1a_example.csv', header=None, names=[])
    
    accuracy_evaluation(data, dataSol)


if __name__ == '__main__':
    main()

