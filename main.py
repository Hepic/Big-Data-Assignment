import pandas
from help_functions import *
from algorithms import *


def main():
    data = pandas.read_csv('datasets/recordings_example.csv', header=0, names=['Day', 'Hour', 'IP', 'MAC'])
    dataSol = pandas.read_csv('datasets/solution_1a_example.csv', header=None, sep='|')[0]

    # data = data.sort_values(by=['Day', 'Hour'])
    # print data[(data.MAC == 712) | (data.MAC == 598) | (data.MAC == 380)].to_string()

    #predFamilies = slow_algorithm(data)
    predFamilies = LSH(data)
    accuracy_evaluation(data, dataSol, predFamilies)

    predFamiliesList = [value for key, value in predFamilies.iteritems()]

    dataPred = pandas.DataFrame(predFamiliesList)
    dataPred = dataPred.fillna(-1)
    dataPred = dataPred.astype(int)
    dataPred.to_csv('datasets/solution_1a.csv', index=False, header=None)

    ################################
    trueL, predL = [sorted(map(int, mac_str.split(','))) for mac_str in dataSol], [sorted(value) for key, value in predFamilies.iteritems()]
    print

    for elem in trueL:
        if elem not in predL:
            print elem

    print '----------------------------------------'

    for elem in predL:
        if elem not in trueL:
            print elem


if __name__ == '__main__':
    main()

