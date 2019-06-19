from help_functions import *
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
    prime_numbers, MOD, K = [1299187, 1572869, 25165843, 100663319, 201326611], 1000000007, 50
    list_info = [] 
    
    # Each hashfunction contributes 'K / number_of_hashfunctions' elements
    for pr_num in prime_numbers:
        list_info_hash = []
        
        for (day, hour, ip) in set_info:
            hash_val = ((((day * pr_num) % MOD * pr_num) % MOD * pr_num) % MOD) % MOD
            hash_val = (hash_val + (((hour * pr_num) % MOD * pr_num) % MOD * pr_num) % MOD) % MOD
            hash_val = (hash_val + (((ip * pr_num) % MOD * pr_num) % MOD * pr_num) % MOD) % MOD

            list_info_hash.append((hash_val, (day, hour, ip)))
        
        # sort the list, so as the get the 'K / number_of_hashfunctions' elements for that hash function
        list_info_hash.sort()

        for i in range(min(K / len(prime_numbers), len(list_info_hash))):
            info = list_info_hash[i][1]
            list_info.append(info)
    
    return list_info


def LSH(mac_info, category):
    LSH_B = 50 
    minhash_info, parents, ranks, groups = dict(), dict(), dict(), dict() 
    hashtables_lsh = [dict() for i in range(LSH_B + 5)]
    
    for mac in mac_info:
        parents[mac] = mac
        ranks[mac] = 0

    start = time.time()
    
    # minhashing for every mac address
    for key, value in mac_info.iteritems():
        minhash_info[key] = minhash(value)

    end = time.time()
    print '(Time) Minhashing: ', end - start, 'secs'
    
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
    print '(Time) Insert to hashtables: ', end - start, 'secs'
    start = time.time()

    # retrieve candidate pairs from lsh hashtables
    # union find on these pairs with jaccard distance
    thres = 0.7 if category == 'hotels' else 0.88

    for i in range(LSH_B):
        for ind, bucket in hashtables_lsh[i].iteritems():
            for j in range(len(bucket)):
                for k in range(j + 1, len(bucket)):
                    mac1, mac2 = bucket[j], bucket[k]
 
                    value1, value2 = mac_info[mac1], mac_info[mac2]
                    dist = jaccard_distance(value1, value2)

                    if dist <= thres:
                        par1, par2 = find_par(parents, mac1), find_par(parents, mac2)

                        if par1 != par2:
                            union_par(parents, ranks, par1, par2)
    
    end = time.time()
    print '(Time) Search in hashtables: ', end - start, 'secs'
    
    # retrieve groups from the union-find structure
    for key, value in parents.iteritems():
        par = find_par(parents, key)

        if par not in groups:
            groups[par] = [key]
        else:
            groups[par].append(key) 
    
    return groups


def remove_groups(mac_info, groups, category):
    ALL_DAYS, key_remove = 50, []
    
    # remove some groups based on some criteria
    if category == 'hotels':
        key_remove = [key for key, value in groups.iteritems() if len(value) <= 1]
    else:
        key_remove = [key for key, value in groups.iteritems() if len(value) <= 2]

    # remove groups based on their changes in their ips per day
    for key, members in groups.iteritems():
        days_ips = [set() for i in range(ALL_DAYS)]
        
        for mac_num in members:
            for (day, hour, ip) in mac_info[mac_num]:
                days_ips[day].add(ip)

        sums, cnt = 0, 0

        for i in range(ALL_DAYS):
            if len(days_ips[i]):
                sums += len(days_ips[i])
                cnt += 1

        avg = float(sums) / float(cnt)

        if (category == 'hotels' and avg >= 5) or (category != 'hotels' and avg <= 4.0):
            key_remove.append(key)

    for elem in key_remove:
        if elem in groups:
            del groups[elem]
    
    # convert groups to sorted lists
    groups = [sorted(value) for key, value in groups.iteritems()]
    
    return groups
