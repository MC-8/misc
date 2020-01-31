class LRUCache:

    def __init__(self, capacity: int):
        self.dic          = {}
        self.capacity   = capacity

    def get(self, key: int) -> int:
        el = self.dic.pop(key, -1)
        if el >-1:
            self.dic[key] = el
        return el

    def put(self, key: int, value: int) -> None:
        self.dic.pop(key, -1)
        self.dic[key] = value
        if len(self.dic)>self.capacity: 
            self.dic.pop(next(iter(self.dic.keys())))

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
