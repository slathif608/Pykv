# filename: core/lru_cache.py

# A simple Node for the Doubly-Linked List
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    Implements the Least Recently Used (LRU) caching policy.
    Uses a dictionary for O(1) key lookup and a doubly-linked list
    to maintain the usage order.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity [cite: 43]
        # { key -> Node } mapping for O(1) access [cite: 45]
        self.cache = {} 
        self.size = 0

        # Dummy head and tail nodes to simplify operations [cite: 46, 48]
        self.head = Node() 
        self.tail = Node() 

        # Link head and tail [cite: 50, 51]
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- Internal Doubly-Linked List Helpers (O(1) operations) ---
    def _add_node_to_head(self, node: Node):
        """Adds a node right after the dummy head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        """Removes an existing node."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node):
        """Moves an existing node to the most recently used position (head)."""
        self._remove_node(node)
        self._add_node_to_head(node)

    # --- Core Cache Methods ---

    def get(self, key: str):
        """Retrieve value by key (O(1)) [cite: 37]"""
        if key in self.cache:
            node = self.cache[key]
            # Update usage: move the accessed node to the head [cite: 34]
            self._move_to_head(node)
            return node.value
        return None

    def put(self, key: str, value):
        """Store key-value pair and manage capacity [cite: 38]"""
        if key in self.cache:
            # Key exists: update value and move to head
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # New key: create node, add to head, and store in cache
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node_to_head(new_node)
            self.size += 1

            # Check capacity and evict if full [cite: 35]
            if self.size > self.capacity:
                self.evict() # Remove least recently used item [cite: 40]

    def delete(self, key: str):
        """Remove key-value pair [cite: 39]"""
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
            self.size -= 1
            return True
        return False
        
    def evict(self):
        """Removes the Least Recently Used item (the node before the dummy tail)."""
        # The node right before the tail is the LRU item
        lru_node = self.tail.prev 
        if lru_node is not self.head:
            self._remove_node(lru_node)
            del self.cache[lru_node.key]
            self.size -= 1
            return lru_node.key
        return None

    def list_keys(self):
        """Helper to list all keys currently in the cache."""
        return list(self.cache.keys())