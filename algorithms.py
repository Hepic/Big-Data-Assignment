import distances


def find_par(parents, ind):
    if parents[ind] != ind:
        parents[ind] = find_par(parents, parents[ind])
    
    return parents[ind]


def union_par(parents, ranks, ind1, ind2):
    if ranks[ind1] > ranks[ind2]:
        parents[ind2] = ind1
        ranks[ind1] += ranks[ind2]
    else:
        parents[ind1] = ind2
        ranks[ind2] += ranks[ind1]


def slow_algorithm(data):
    all_mac = len(set(data.MAC))
    mac_info, parents, ranks, families = dict(), dict(), dict(), dict()
    
    for ind, row in data.iterrows():
        mac = row['MAC']
        info = (row['Day'], row['Hour'], row['IP'])
        
        if mac not in mac_info:
            mac_info[mac] = []
            parents[mac] = mac
            ranks[mac] = 0

        mac_info[mac].append(info)
   
    for key1, value1 in mac_info.iteritems():
        for key2, value2 in mac_info.iteritems():
            if key1 == key2:
                continue
            
            dist = distances.jaccard_distance(value1, value2)

            if dist <= 0.9:
                par1, par2 = find_par(parents, key1), find_par(parents, key2)

                if par1 != par2:
                    union_par(parents, ranks, par1, par2)

    for key, value in parents.iteritems():
        par = find_par(parents, key)

        if par not in families:
            families[par] = [key]
        else:
            families[par].append(key)
        
    print families
