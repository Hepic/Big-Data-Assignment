import math, time
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


def read_macs(data, category, pred_families = [], pred_workers = []):
    mac_info, visited = dict(), dict()
    start = time.time()

    if category == 'hotels':
        # mark each mac that belongs either to a family or to a group of workers
        for family in pred_families:
            for member in family:
                visited[member] = True

        for workers in pred_workers:
            for member in workers:
                visited[member] = True
    
    # retrieve mac addresses information
    for day, hour, ip, mac in zip(data['Day'], data['Hour'], data['IP'], data['MAC']):
        info = (day, hour, ip)
        
        # avoid useless information 
        if (category == 'families' and (day % 7 >= 1 and day % 7 <= 5 and hour >= 7 and hour <= 16)) or \
        (category == 'workers' and (not (day % 7 >= 1 and day % 7 <= 5 and hour >= 7 and hour <= 16))) or \
        (category == 'hotels' and (mac in visited)):
            continue
        
        if mac not in mac_info:
            mac_info[mac] = set()

        mac_info[mac].add(info)
        
        # shift data by few hours to help jaccard distance
        for i in range(-2, 3, 1):
            info = (day, (hour + i + 24) % 24, ip)
            mac_info[mac].add(info)

    end = time.time()
    print '(Time) Get mac info for', category, ': ', end - start, 'secs'
    
    return mac_info


def accuracy_evaluation(data, data_sol, pred_families):
    macs = list(set(data.MAC))
    le = preprocessing.LabelEncoder()
    le.fit(macs)

    trueLabels, predLabels = [-1 for i in range(len(macs))], [-1 for i in range(len(macs))]
    ind = 0
    
    # labels of real solution
    for mac_str in data_sol:
        mac_list = map(int, mac_str.split(','))

        for mac_num in mac_list:
            pos = le.transform([mac_num])[0]
            trueLabels[pos] = ind 

        ind += 1

    ind = 0
    
    # labels of predicted solution
    for family_members in pred_families:
        for mac_num in family_members:
            pos = le.transform([mac_num])[0]
            predLabels[pos] = ind

        ind += 1

    return adjusted_rand_score(trueLabels, predLabels)
