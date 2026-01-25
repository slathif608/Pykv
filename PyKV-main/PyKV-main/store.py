import time
from typing import Optional
from core.ttl_heap import TTLHeap
from core.lru_cache import LRUCache


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int = 5):
        self.capacity = capacity
        self.cache = {}  # key -> value
        self.ttl_heap = TTLHeap()

        # Dummy head & tail (not used currently, kept as-is)
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.order = []

        # 🔹 Stats
        self.hits = 0
        self.misses = 0
        self.set_ops = 0
        self.get_ops = 0
        self.delete_ops = 0

    # ---------------- TTL ADDITION ----------------
    def _evict_expired(self):
        expired_keys = self.ttl_heap.get_expired_keys()
        for key in expired_keys:
            if key in self.cache:
                self.order.remove(key)
                del self.cache[key]
                self.cache.pop(key, None)

    def get(self, key):
        self.get_ops += 1
        self._evict_expired()   # ✅ TTL enforcement

        if key not in self.cache:
            self.misses += 1
            return None

        self.hits += 1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def set(self, key, value, ttl=None):
        self.set_ops += 1
        self._evict_expired()   # ✅ TTL enforcement

        if ttl is not None:
            self.ttl_heap.add(key, ttl)   # ✅ TTL tracking

        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            lru = self.order.pop(0)
            del self.cache[lru]

        self.cache[key] = value
        self.order.append(key)

    def delete(self, key):
        self.delete_ops += 1
        if key in self.cache:
            self.order.remove(key)
            del self.cache[key]

    def keys(self):
        return list(self.cache.keys())

    def stats(self):
        return {
            "total_keys": len(self.cache),
            "capacity": self.capacity,
            "hits": self.hits,
            "misses": self.misses,
            "set_ops": self.set_ops,
            "get_ops": self.get_ops,
            "delete_ops": self.delete_ops,

            "ttl_set_ops": self.ttl_heap.total_added,
            "ttl_expired": self.ttl_heap.total_expired,
            "ttl_active": len(self.ttl_heap.heap)
        }

    def clear(self):
        self.cache = {}
        self.ttl_heap.clear()
        self.order = []
        self.hits = 0
        self.misses = 0
        self.set_ops = 0
        self.get_ops = 0
        self.delete_ops = 0