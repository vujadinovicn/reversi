import random
from maps.map import Map, MapElement

class ChainedHashMap(object):
    def __init__(self, capacity=8):
        self._data = capacity * [None]
        self._capacity = capacity
        self._size = 0
        self.prime = 18409
        self._a = 1 + random.randint(1, self.prime-1)
        self._black = random.randint(1,257)
        self._white = random.randint(1,342)
        self._random_table = [[random.randint(1, self._a) for _ in range(8)] for _ in range(8)]

    def __len__(self):
        return self._size

    def _hash(self, key):
        hashed_value = 0
        for i in range(8):
            for j in range(8):
                if key.black_state.board & (1 << (63-8*i-j)) > 0:
                    empty_fill_black_state = 1
                else:
                    empty_fill_black_state = 0

                if key.white_state.board & (1 << (63-8*i-j)) > 0:
                    empty_fill_white_state = 1
                else:
                    empty_fill_white_state = 0

                hashed_value += self._random_table[i][j] * self._black * empty_fill_black_state
                hashed_value += self._random_table[i][j] * self._black * empty_fill_white_state

        compressed = hashed_value % self._capacity
        return compressed

    def __getitem__(self, key):
        bucket_index = self._hash(key)
        return self._bucket_getitem(bucket_index, key)

    def __setitem__(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_setitem(bucket_index, key, value)

    def _bucket_getitem(self, i, key):
        bucket = self._data[i]
        if bucket is None:
            return None
        return bucket[key]

    def _bucket_setitem(self, bucket_index, key, value):
        bucket = self._data[bucket_index]
        if bucket is None:
            self._data[bucket_index] = Map()
        current_size = len(self._data[bucket_index])
        self._data[bucket_index][key] = value
        if len(self._data[bucket_index]) > current_size:
            self._size += 1

    def add(self, board, value):
        index = self._hash(board)
        self._bucket_setitem(index, board, value)

    def __contains__(self, key):
        index = self._hash(key)
        if self._data[index] != None:
            bucket = self._data[index]
            if key in bucket:
                return True
        return False