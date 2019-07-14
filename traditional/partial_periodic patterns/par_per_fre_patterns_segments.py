
import sys
from sys import getsizeof
import time
from out_data_modifier import modify_op

# In[112]:


class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children  # dictionary of children
        self.parent = None
        self.tids = set()
        self.freq = 0

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self



# In[113]:


class Tree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}

    def add_transaction(self, transaction, tid, freq):
        curr_node = self.root
        for i in range(len(transaction)):
            if transaction[i] not in curr_node.children:
                new_node = Node(transaction[i], {})
                curr_node.addChild(new_node)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(new_node)
                else:
                    self.summaries[transaction[i]] = [new_node]
                curr_node = new_node
            else:
                curr_node = curr_node.children[transaction[i]]
        curr_node.tids |= tid
        curr_node.freq += freq

    def get_condition_pattern(self, alpha):
        final_patterns = []
        final_sets = []
        final_freq = []
        for i in self.summaries[alpha]:
            set1 = i.tids
            loc_f = i.freq
            set2 = []
            while (i.parent.item != None):
                set2.insert(0, i.parent.item)
                i = i.parent
            if (len(set2) > 0):
                final_patterns.append(set2)
                final_freq.append(loc_f)
                final_sets.append(set1)
        return final_patterns, final_sets, final_freq

    def remove_node(self, node_val):
        for i in self.summaries[node_val]:
            i.parent.tids |= i.tids
            i.parent.freq += i.freq
            del i.parent.children[node_val]
            i = None

    def get_ts(self, alpha, per, min_pf, min_sup):
        tid_s = set()
        freq = 0
        per_fre = 0
        valid = 0
        for i in self.summaries[alpha]:
            tid_s |= i.tids
            freq += i.freq
        if freq > min_sup:
            per_fre = get_per_fre(tid_s, per)
            if (per_fre < min_pf):
                valid = 0
            else:
                valid=1
        return per_fre, freq, valid

    def generate_patterns(self, prefix, per, min_pf, min_sup, genelist):
        for i in sorted(self.summaries, reverse=True):
            #             print(genelist[i])
            per_fre, freq, valid = self.get_ts(i, per,min_pf, min_sup)
            if (valid == 1):
                pattern = prefix.copy()
                pattern.append(genelist[i])
                yield pattern, per_fre
                # print(pattern,per_fre)
                patterns, tid_summ, tid_pf = self.get_condition_pattern(i)
                conditional_tree = Tree()
                for pat in range(len(patterns)):
                    conditional_tree.add_transaction(patterns[pat], tid_summ[pat], tid_pf[pat])
                if (len(patterns) >= 1):
                    for li in conditional_tree.generate_patterns(pattern, per, min_pf, min_sup,genelist):
                        yield (li)
            self.remove_node(i)


# In[114]:


def build_tree(data):
    root_node = Tree()
    for i in range(len(data)):
        set1 = set()
        set1.add(data[i][0])
        root_node.add_transaction(data[i][1:], set1, 1)
    return root_node


# In[115]:


def get_per_fre(tids, per):
    tids = list(tids)
    tids.sort()
    cur = tids[0]
    pf = 0
    for j in range(1, len(tids)):
        if (tids[j] - cur <= per):
            pf += 1
        cur = tids[j]
    return pf


# In[116]:


def generate_dict(transactions, per_freq, min_sup, periodicity):
    data = {}
    # max_acc_per = x_fac * periodicity
    for tr in transactions:
        for i in range(1, len(tr)):
            if tr[i] not in data:
                data[tr[i]] = [int(tr[0]), 1, 0]
            else:
                if ((int(tr[0]) - data[tr[i]][0]) <= periodicity):
                    data[tr[i]][2] += 1
                data[tr[i]][0] = int(tr[0])
                data[tr[i]][1] += 1
    #     print(data)
    data = {k: v for k, v in data.items() if v[2] >= per_freq and v[1] >= min_sup }
    return data


# In[118]:


def update_transactions1(list_of_transactions, dict1, gene_li):
    rank = dict([(index, item) for (item, index) in enumerate(gene_li)])
    #     print(rank)
    list1 = []
    k = len(list_of_transactions)
    avg_tran_len = 0
    for tr in list_of_transactions:
        list2 = [int(tr[0])]
        for i in range(1, len(tr)):
            if tr[i] in dict1:
                list2.append(rank[tr[i]])
        if (len(list2) >= 2):
            basket = list2[1:]
            avg_tran_len += len(basket)
            # print(len(basket))
            basket.sort()
            list2[1:] = basket[0:]
            list1.append(list2)
    return list1, avg_tran_len / k


# In[146]:


def get_segments(transactions, length):
    t_start = 1
    seg_id = 1
    segments = []
    sub_segment = []
    sub_segment.append(str(seg_id))
    incr = 0
    for i in transactions:
        incr += 1
        if ((int(i[0]) - t_start) > length):
            segments.append(sub_segment)
            seg_id += int((int(i[0]) - t_start) / (length + 1))
            t_start = int(i[0])
            sub_segment = []
            sub_segment.append(str(seg_id))
            incr = 1

        for j in range(1, len(i)):
            item = i[j]  # +str(incr)
            sub_segment.append(item)
    if len(sub_segment) > 1:
        segments.append(sub_segment)
    return segments


# In[147]:


def main(path, per_freq, periodicity, min_sup):
    with open(path, 'r') as f:
        lno = 0
        list_of_transactions = []
        for line in f:
            li = line.split()
            list_of_transactions.append(li)
            lno = lno + 1
        f.close()

    # list_of_segments = get_segments(list_of_transactions, length)
    total_transactions = len(list_of_transactions)
    #     print(list_of_segments)
    per_freq = (per_freq * total_transactions) / 100

    min_sup = (min_sup * total_transactions) / 100
    per = (periodicity * total_transactions) / 100
    print(per_freq, per, min_sup)
    generated_dict = generate_dict(list_of_transactions, per_freq, min_sup, per)
    #     print(generated_dict)
    gene_list = [key for key, value in sorted(generated_dict.items(), key=lambda x: x[1][1], reverse=True)]
    #     rank = dict([(index,item) for (item,index) in enumerate(gene_list)])

    print("#########")
    print("NO of singleitems:", end='')
    print(len(gene_list))
    print("#########")
    updated_transactions1, k = update_transactions1(list_of_transactions, generated_dict, gene_list)
    print(gene_list)
    Tree = build_tree(updated_transactions1)
    q = Tree.generate_patterns([], per, per_freq, min_sup, gene_list)
    return q, gene_list


# In[148]:


if (__name__ == "__main__"):
    path = sys.argv[1]
    outfile = sys.argv[2]
    per_freq = float(sys.argv[3])
    periodicity_threshold = float(sys.argv[4])
    min_sup = float(sys.argv[5])
    k, gl = main(path, per_freq, periodicity_threshold, min_sup)
    with open(outfile, 'w') as f:
        for x in k:
            f.write('%s \n' % str(x))
    modify_op(outfile)
    print(len(gl))