import pandas, csv, sys
from help_functions import *
from algorithms import *


def main():
    start = time.time()
    data = pandas.read_csv(sys.argv[1], header=0, names=['Day', 'Hour', 'IP', 'MAC'])
    
    print '\nSearching Families'
    mac_info_fam = read_macs(data, 'families')
    pred_families = LSH(mac_info_fam)
    pred_families = remove_groups(mac_info_fam, pred_families, 'families')

    print '\nSearching Workers'
    mac_info_work = read_macs(data, 'workers')
    pred_workers = LSH(mac_info_work)
    pred_workers = remove_groups(mac_info_work, pred_workers, 'workers')
    
    print '\nSearching Hotels'
    mac_info_hotel = read_macs(data, 'hotels', pred_families, pred_workers) 
    pred_hotels = LSH(mac_info_hotel)
    pred_hotels = remove_groups(mac_info_hotel, pred_hotels, 'hotels')
    
    if (len(sys.argv) == 3):
        data_sol = pandas.read_csv(sys.argv[2], header=None, sep='|')[0]
        print '\nAccuracy for families: ', accuracy_evaluation_families(data, data_sol, pred_families)
    
    predictions = [pred_families, pred_workers, pred_hotels]
    output_paths = ['datasets/solution_1a.csv', 'datasets/solution_1b.csv', 'datasets/solution_2.csv']

    # print the predicted groups in the files
    for i in range(3):
        with open(output_paths[i], 'w') as f:
            wr = csv.writer(f, delimiter=',')
            
            for elem in predictions[i]:
                wr.writerow(elem)

    end = time.time()
    print '\nTotal time: ', end - start, 'secs'


if __name__ == '__main__':
    main()

