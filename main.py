import pandas, csv
from help_functions import *
from algorithms import *


def main():
    start = time.time()
    
    data = pandas.read_csv('datasets/recordings_example.csv', header=0, names=['Day', 'Hour', 'IP', 'MAC'])
    dataSol = pandas.read_csv('datasets/solution_1a_example.csv', header=None, sep='|')[0]

    predFamilies = LSH(data)
    print 'Accuracy: ', accuracy_evaluation(data, dataSol, predFamilies)

    with open('datasets/solution_1a.csv', 'w') as f:
        wr = csv.writer(f, delimiter=',')
        
        for elem in predFamilies:
            wr.writerow(elem)

    ''' For testing purposes
    trueFamilies = [sorted(map(int, mac_str.split(','))) for mac_str in dataSol]
    print

    for elem in trueFamilies:
        if elem not in predFamilies:
            print elem

    print '----------------------------------------'

    for elem in predFamilies:
        if elem not in trueFamilies:
            print elem
    '''

    end = time.time()
    print 'Total time: ', end - start


if __name__ == '__main__':
    main()

