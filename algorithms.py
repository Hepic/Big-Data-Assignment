from distances import *
import time


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


def minhash(set_info):
    prime_numbers, MOD, K = [101, 6151, 12289, 49157, 393241, 786433, 1572869, 25165843, 100663319, 201326611], 1000000007, 50
    list_info = [] 
    
    for pr_num in prime_numbers:
        list_info_hash = []

        for (day, hour, ip) in set_info:
            hash_val = ((day * pr_num) % MOD + ((hour * pr_num) % MOD * pr_num) % MOD) % MOD
            hash_val = (hash_val + (((ip * pr_num) % MOD * pr_num) % MOD * pr_num) % MOD) % MOD

            list_info_hash.append((hash_val, (day, hour, ip)))

        list_info_hash.sort()

        for i in range(min(K / len(prime_numbers), len(list_info_hash))):
            info = list_info_hash[i][1]
            list_info.append(info)
    
    return list_info


def LSH(data):
    LSH_B, ALL_DAYS = 50, 50 
    mac_info, minhash_info, parents, ranks, families,  = dict(), dict(), dict(), dict(), dict() 
    hashtables_lsh = [dict() for i in range(LSH_B + 5)]

    start = time.time()
    
    # retrieve mac addresses information
    for day, hour, ip, mac in zip(data['Day'], data['Hour'], data['IP'], data['MAC']):
        info = (day, hour, ip)
        
        # do not include working hours
        if day % 7 >= 1 and day % 7 <= 5 and hour >= 7 and hour <= 16:
            continue 

        if mac not in mac_info:
            mac_info[mac] = set()
            parents[mac] = mac
            ranks[mac] = 0

        mac_info[mac].add(info)
        
        # shift data by few hours to help jaccard distance
        for i in range(-2, 3, 1):
            info = (day, (hour + i + 24) % 24, ip)
            mac_info[mac].add(info)

    end = time.time()
    print 'Get mac info: ', end - start
    
    start = time.time()
    
    # minhashing for every mac address
    for key, value in mac_info.iteritems():
        minhash_info[key] = minhash(mac_info[key])

    end = time.time()
    print 'Minhashing: ', end - start
    
    start = time.time()

    # insert mac information in the lsh hashtables
    for key, value in minhash_info.iteritems():
        ind = 0 
 
        for elem in value:
            if elem not in hashtables_lsh[ind]:
                hashtables_lsh[ind][elem] = [key]
            else:
                hashtables_lsh[ind][elem].append(key)
            
            ind += 1
    
    end = time.time()
    print 'Insert to hashtables: ', end - start
    start = time.time()

    # retrieve candidate pairs from lsh hashtables
    # union find on these pairs with jaccard distance
    for i in range(LSH_B):
        for ind, bucket in hashtables_lsh[i].iteritems():
            for j in range(len(bucket)):
                for k in range(j + 1, len(bucket)):
                    mac1, mac2 = bucket[j], bucket[k]
 
                    value1, value2 = mac_info[mac1], mac_info[mac2]
                    dist = jaccard_distance(value1, value2)

                    if dist <= 0.88:
                        par1, par2 = find_par(parents, mac1), find_par(parents, mac2)

                        if par1 != par2:
                            union_par(parents, ranks, par1, par2)
    
    end = time.time()
    print 'Search in hashtables: ', end - start
    
    # retrieve families from the union-find structure
    for key, value in parents.iteritems():
        par = find_par(parents, key)

        if par not in families:
            families[par] = [key]
        else:
            families[par].append(key) 
    
    # remove some families based on some criteria
    keyRemove = [key for key, value in families.iteritems() if len(value) <= 2]
    
    # remove families with few changes in their ips per day
    for key, family_members in families.iteritems():
        days_ips = [set() for i in range(ALL_DAYS)]
        
        for mac_num in family_members:
            for (day, hour, ip) in mac_info[mac_num]:
                days_ips[day].add(ip)

        sums, cnt = 0, 0

        for i in range(ALL_DAYS):
            if len(days_ips[i]):
                sums += len(days_ips[i])
                cnt += 1

        avg = float(sums) / float(cnt)

        if avg <= 4.0:
            keyRemove.append(key)

    for elem in keyRemove:
        if elem in families:
            del families[elem]
    
    # convert families to sorted lists
    families = [sorted(value) for key, value in families.iteritems()]
    
    return families
