all_itemsets = []
bool_itemsets_dict = {}
d = open('fin_op#2', 'w')
with open('fin_op#', 'r') as l:
    lines = l.readlines()
    for row in lines:
        #r = row.strip().split(':')
        #utility = int(r[1])
        items = row.split(' ')
        number_of_items = len(items)
        items1 = items[0:number_of_items - 2]
        items1 = [int(item.split('\'', 1)[1].split('\'')[0]) for item in items1]
        items1.sort()
        all_itemsets.append(items1)
        bool_itemsets_dict[tuple(items1)] = True
    l.close()
delta = 1

# removing the itemsets which are subset of other itemsets in all_itemsets

for itemset in all_itemsets:
    itemset_set = set(itemset)
    for next_itemset in all_itemsets:
        if bool_itemsets_dict[tuple(next_itemset)]:
            next_itemset_set = set(next_itemset)
            if next_itemset_set == itemset_set:
                continue
            if itemset_set.issubset(next_itemset_set):
                bool_itemsets_dict[tuple(itemset)] = False
                break

non_subset_itemsets = []
bool_non_subset_itemsets = {}
for itemset in all_itemsets:
    if bool_itemsets_dict[tuple(itemset)]:
        non_subset_itemsets.append(itemset)
        bool_non_subset_itemsets[tuple(itemset)] = True

# remove the itemsets having the dissimilarity of delta and combine them
final_itemsets = []
for idx, itemset in enumerate(non_subset_itemsets):
    if bool_non_subset_itemsets[tuple(itemset)]:
        if len(itemset) <= delta:
            final_itemsets.append(itemset)
            continue
        temp_itemset = itemset[:]
        for id, next_itemset in enumerate(non_subset_itemsets):
            if id == idx:
                continue
            if bool_non_subset_itemsets[tuple(next_itemset)]:
                itemset_set = set(temp_itemset)
                next_itemset_set = set(next_itemset)
                diffa = itemset_set - next_itemset_set
                diffb = next_itemset_set - itemset_set
                if len(diffa) <= delta or len(diffb) <= delta:
                # combine them to form new set
                    temp_itemset = list(next_itemset_set | itemset_set)
                    bool_non_subset_itemsets[tuple(next_itemset)] = False
                    bool_non_subset_itemsets[tuple(itemset)] = False
        final_itemsets.append(temp_itemset)

i=0
for itemset in final_itemsets:
    for item in itemset:
        d.write('%s ' % item)
    print(i)
    i+=1
    d.write('\n')
d.close()
