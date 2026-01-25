import heapq
import time

class TTLHeap:
    def __init__(self):
        self.heap = []
        self.total_added = 0
        self.total_expired = 0

    def add(self, key, ttl_seconds):
        expiry = time.time() + ttl_seconds
        heapq.heappush(self.heap, (expiry, key))
        self.total_added += 1

    def get_expired_keys(self):
        now = time.time()
        expired = []

        while self.heap and self.heap[0][0] <= now:
            _, key = heapq.heappop(self.heap)
            expired.append(key)
            self.total_expired += 1

        return expired

    def clear(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)