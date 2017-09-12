import math
import operator
from collections import Counter


def create_data_set():
    lines = open('dt-data.txt', 'r').read().split('\n')
    labels = lines[0][1:-1].split(', ')
    labels = labels[0:-1]
    examples = lines[2:-1]
    data_set = [example[3:-1].split(', ') for example in examples]
    return data_set, labels

def calc_ent(data_set):
    data_num = len(data_set)
    res_list = [ins[-1] for ins in data_set]
    res_count_dict = Counter(res_list)
    # print(res_count_dict)
    ent = 0.0
    for value in res_count_dict.values():
        prob = value / data_num
        ent -= prob * math.log(prob, 2)
        # print(ent)
    return ent

def calc_gain(data_set, column):
    data_num = len(data_set)
    res_list = [ins[column] for ins in data_set]
    res_count_dict = Counter(res_list)
    # print(res_count_dict)
    whole_ent = calc_ent(data_set)
    # print(whole_ent)
    d_ent = 0.0
    for key in res_count_dict.keys():
        prob = res_count_dict[key] / data_num
        new_set = []
        for data in data_set:
            if data[column] == key:
                new_set.append(data)
        ent = calc_ent(new_set)
        # print(ent)
        d_ent += prob * ent
        # print(d_ent)
    gain = whole_ent - d_ent
    return gain

def calc_max_gain(data_set, labels):
    gain_dict = {}
    gain = 0.0
    columns = len(data_set[0])
    feature_num = columns - 1
    for var in range(0, feature_num):
        gain = calc_gain(data_set, var)
        gain_dict[labels[var]] = gain
    max_gain = -1
    index = 100
    # print(max_gain)
    for k, v in gain_dict.items():
        if v > max_gain:
            max_gain = v
            index = labels.index(k)
        elif v == max_gain:
            index1 = labels.index(k)
            index2 = index
            index = min(index1, index2)
            # print(k, "judge", index1, index2)
    # print(index)
    return index


def split_data_set(data_set, best_label_index, value):
    new_data_set = []
    for item in data_set:
        if item[best_label_index]==value:
            split_set = item[:best_label_index]
            split_set.extend(item[best_label_index+1:])
            new_data_set.append(split_set)
    return new_data_set

def get_label_values(key):
    data_set, labels = create_data_set()
    label_values = {}
    # label_values = set([item[index] for item in data_set])
    i = 0
    for label in labels:
        item = set([item[i] for item in data_set])
        label_values[label] = item
        i += 1
    # print(label_values[key])
    return list(label_values[key])



def create_tree(data_set, labels):
    cur_set = [item[-1] for item in data_set]
    if len(data_set) == 0:
        # print("tie")
        return 'tie'
    if cur_set.count(cur_set[0]) == len(cur_set):
        return cur_set[0]
    if (len(data_set[0]) == 1):
        return 'tie'
    best_label_index = calc_max_gain(data_set, labels)
    best_label = labels[best_label_index]
    decision_tree = {best_label:{}}
    del(labels[best_label_index])
    # label_values = set([item[best_label_index] for item in data_set])
    label_values = get_label_values(best_label)
    for value in label_values:
        sub_labels = labels[:]
        decision_tree[best_label][value] = create_tree(split_data_set(data_set, best_label_index,value), sub_labels)

    return decision_tree

# data_set, labels = create_data_set()
# print(data_set[0][0])
data_set, labels = create_data_set()
# print(data_set)
# calc_ent(data_set, 0)
# calc_gain(data_set, labels)
#del_label(data_set, 1)
my_tree = create_tree(data_set, labels)
print(my_tree)
# calc_d_ent(data_set, 0)
# get_label_values("VIP")