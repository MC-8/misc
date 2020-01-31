class LRUCache:
    def __init__(self, capacity: int):
        self.cache          = {}
        self.capacity   = capacity

    def get(self, key: int) -> int:
        el = self.cache.pop(key, -1)
        if el >-1:
            self.cache[key] = el
        return el

    def put(self, key: int, value: int) -> None:
        self.cache.pop(key, -1)
        self.cache[key] = value
        if len(self.cache)>self.capacity: 
            self.cache.pop(next(iter(self.cache.keys())))

from collections import OrderedDict
# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
# cache = LRUCache(2)
# cache.put(1, 1)
# cache.put(2, 2)
# print(cache.get(1))
# cache.put(3, 3)
# print(cache.get(2))
# cache.put(4, 4)
# print(cache.get(1))
# print(cache.get(3))
# print(cache.get(4))
cache = LRUCache(2)
cache.put(2, 1)
cache.put(1, 1)
cache.put(2, 3)
cache.put(4, 1)
print(cache.get(1))
print(cache.get(2))
