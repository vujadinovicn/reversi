from maps.map_element import MapElement

class Map(object):
    def __init__(self):
        self._data = []

    def __getitem__(self, key):
        for item in self._data:
            if key == item.key:
                return item.value

    def __setitem__(self, key, value):
        for item in self._data:
            if key == item.key:
                item.value = value
                return
        self._data.append(MapElement(key, value))

    def __delitem__(self, key):
        length = len(self._data)
        for i in range(length):
            if key == self._data[i].key:
                self._data.pop(i)
                return

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        for item in self._data:
            if key == item.key:
                return True
        return False

    def __iter__(self):
        for item in self._data:
            yield item.key

    def items(self):
        for item in self._data:
            yield item.key, item.value