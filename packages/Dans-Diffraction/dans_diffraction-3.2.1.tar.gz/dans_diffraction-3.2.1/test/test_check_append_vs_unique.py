"""
Test operation speed:
    append to list with check + count
    vs
    list, counts = np.unique(return_count=True)
16/08/2023
"""

import time
import numpy as np


class CountList:
    def __init__(self):
        self._array = np.empty([0, 3], dtype=int)
        self._count = np.empty([0], dtype=int)

    def append(self, array):
        array = np.reshape(array, [-1, 3])
        for vector in array:
            find_in_array = np.sum(np.square(self._array - vector), axis=1) == 0
            if np.any(find_in_array):
                self._count[find_in_array] += 1
            else:
                self._array = np.vstack([self._array, vector])
                self._count = np.append(self._count, 1)

    def __len__(self):
        return len(self._array)

    def __str__(self):
        return f"CountList(length: {self.__len__()}, max count: {max(self._count)})"


mylist = CountList()
biglist = np.empty([0, 3], dtype=int)
all_lists = [np.random.randint(0, 10, size=[np.random.randint(100), 3]) for n in range(10000)]

# using count list
t1 = time.time()
for ll in all_lists:
    mylist.append(ll)
t2 = time.time()
t_count_list = t2 - t1

# using unique
t1 = time.time()
for ll in all_lists:
    biglist = np.vstack([biglist, ll])
#biglist = np.vstack(all_lists)
mylist2, counts = np.unique(biglist, return_counts=True, axis=0)
t2 = time.time()
t_unique = t2 - t1

print(f'Count list time: {t_count_list: .4g}')
print(f'    Unique time: {t_unique: .4g}')
print(f' Count list len: {len(mylist)}')
print(f'     Unique len: {len(mylist2)}')
print(f' Count list max: {max(mylist._count)}')
print(f'     Unique max: {max(counts)}')

