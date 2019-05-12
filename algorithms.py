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
    mac_info, parents, ranks, families = dict(), dict(), dict(), dict()

    # retrieve mac addresses information
    for ind, row in data.iterrows():
        mac = int(row['MAC'])
        info = (row['Day'], row['Hour'], row['IP'])

        if row['Day'] % 7 >= 1 and row['Day'] % 7 <= 5 and row['Hour'] >= 7 and row['Hour'] <= 16:
            continue

        if mac not in mac_info:
            mac_info[mac] = []
            parents[mac] = mac
            ranks[mac] = 0

        mac_info[mac].append(info)

        for i in range(-2, 3, 1):
            info = (row['Day'], (row['Hour'] + i + 24) % 24, row['IP'])
            mac_info[mac].append(info)

    # union find on closests mac addresses with jaccard distance
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

    # remove some families based on some criteria
    keyRemove = [key for key, value in families.iteritems() if len(value) <= 2]

    for key, value in families.iteritems():
        days_ips = [set() for i in range(50)]

        for mac_num in value:
            for (day, hour, ip) in mac_info[mac_num]:
                days_ips[day].add(ip)

        sums, cnt = 0, 0

        for i in range(50):
            if len(days_ips[i]):
                sums += len(days_ips[i])
                cnt += 1

        avg = float(sums) / float(cnt)

        if avg <= 4.0:
            keyRemove.append(key)

    for elem in keyRemove:
        if elem in families:
            del families[elem]

    return families
