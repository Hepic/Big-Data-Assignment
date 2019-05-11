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
    mac_info, parents, ranks, families, mac_info_1, parents_1, ranks_1, works = dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()
    
    for ind, row in data.iterrows():
        mac = int(row['MAC'])
        info = (row['Day'], row['Hour'], row['IP'])
        
        if row['Day'] % 7 >= 1 and row['Day'] % 7 <= 5 and row['Hour'] >= 7 and row['Hour'] <= 16:
            if mac not in mac_info_1:
                mac_info_1[mac] = []
                parents_1[mac] = mac
                ranks_1[mac] = 0

            mac_info_1[mac].append(info)
        else:
            if mac not in mac_info:
                mac_info[mac] = []
                parents[mac] = mac
                ranks[mac] = 0

            mac_info[mac].append(info)
            
            for i in range(-2, 3, 1):
                info = (row['Day'], (row['Hour'] + i + 24) % 24, row['IP'])
                mac_info[mac].append(info)

    for key1, value1 in mac_info.iteritems():
        for key2, value2 in mac_info.iteritems():
            if key1 == key2:
                continue
            
            dist = distances.jaccard_distance(value1, value2)

            if dist <= 0.88:
                par1, par2 = find_par(parents, key1), find_par(parents, key2)

                if par1 != par2:
                    union_par(parents, ranks, par1, par2)

    for key, value in parents.iteritems():
        par = find_par(parents, key)

        if par not in families:
            families[par] = [key]
        else:
            families[par].append(key)
        
    ########################################
    
    for key1, value1 in mac_info_1.iteritems():
        for key2, value2 in mac_info_1.iteritems():
            if key1 == key2:
                continue
            
            dist = distances.jaccard_distance(value1, value2)

            if dist <= 0.6:
                par1, par2 = find_par(parents_1, key1), find_par(parents_1, key2)

                if par1 != par2:
                    union_par(parents_1, ranks_1, par1, par2)

    for key, value in parents_1.iteritems():
        par = find_par(parents_1, key)

        if par not in works:
            works[par] = [key]
        else:
            works[par].append(key)
    
    for key, value in works.iteritems():
        if len(value) >= 3:
            for elem in value:
                if elem in families:
                    del families[elem][:]

    #########################################

    return families
