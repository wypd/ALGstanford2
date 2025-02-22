# data format
# weight, length
#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import sys
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

class Solution():
    
    def solverDP(self, items, capacity):
        items = sorted(items, key=lambda x: x.value / float(x.weight), reverse = True)
        
        min_weight = [item.weight for item in items]
        for idx in range(len(min_weight) - 2, -1, -1):
            min_weight[idx] = min(min_weight[idx], min_weight[idx + 1])
        
        valueTrack = {0: 0}
        takenTrack = {0: []}
        
        slope = -1
        
        for (idx, item) in enumerate(items):
            if slope >= 0 and item.value < slope * item.weight:
                break
            new_valueTrack = {}
            new_takenTrack = {}
            for w in valueTrack:
                new_valueTrack[w] = valueTrack[w]
                new_takenTrack[w] = takenTrack[w]
                new_w = w + item.weight
                if new_w <= capacity and (not new_w in new_valueTrack or new_valueTrack[new_w] < valueTrack[w] + item.value): 
                    new_valueTrack[new_w] = valueTrack[w] + item.value
                    new_takenTrack[new_w] = takenTrack[w] + [item.index]
            threshold = -1
            for w in sorted(new_valueTrack):
                if new_valueTrack[w] > threshold:
                    threshold = new_valueTrack[w]
                else:
                    del new_valueTrack[w]
                    del new_takenTrack[w]
            valueTrack = copy.deepcopy(new_valueTrack)
            takenTrack = copy.deepcopy(new_takenTrack)
            
            max_w = max(valueTrack)
            if max_w + min_weight[idx] > capacity:
                second_max_w = max(w for w in valueTrack if w < capacity - min_weight[idx])
                slope = (valueTrack[max_w] - valueTrack[second_max_w]) / float(capacity - second_max_w)
        
        value = valueTrack[max(valueTrack)]
        taken = [0] * len(items)
        for i in takenTrack[max(takenTrack)]:
            taken[i] = 1
        return (value, taken)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    capacity = int(firstLine[0])
    item_count = int(firstLine[1])
    
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    ## My code
    sol = Solution()
    (value, taken) = sol.solverDP(items, capacity)
    
    ## End of my code
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

if __name__ == '__main__':
    file_location = "knapsack_big.txt"
    input_data_file = open(file_location, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    print solve_it(input_data)