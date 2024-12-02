from typing import Optional
from dataclasses import dataclass
import math

@dataclass
class Node:
    key: str
    next: Optional['Node'] = None
    collisions: int = 0

class HashTable:
    def __init__(self, size: int = 16):
        """Initialize hash table
        
        Args:
            size: Table size (must be power of 2)
        """
        if not math.log2(size).is_integer():
            raise ValueError("Table size must be power of 2")
        
        self.size = size
        self.table = [None] * size
        # Constant for multiplication method ((√5-1)/2)
        self.A = (math.sqrt(5) - 1) / 2

    def string_to_int(self, key: str) -> int:
        """Convert string key to integer"""
        return sum(ord(c) * (31 ** i) for i, c in enumerate(key))

    def hash_function(self, key: str) -> int:
        """Multiplication method for hashing
        h(k) = trunk(M{k*A}), where M = 2^m, A = (√5-1)/2
        """
        k = self.string_to_int(key)
        product = k * self.A
        fractional = product - math.floor(product)
        return math.floor(self.size * fractional)

    def insert(self, key: str) -> bool:
        """Insert key into hash table"""
        hash_value = self.hash_function(key)
        
        new_node = Node(key)
        
        # If cell is empty
        if self.table[hash_value] is None:
            self.table[hash_value] = new_node
            return True
            
        # If collision - add to chain
        current = self.table[hash_value]
        while current.next:
            if current.key == key:
                return False  # Key already exists
            current = current.next
            new_node.collisions += 1
            
        current.next = new_node
        return True

    def search(self, key: str) -> tuple[Optional[int], Optional[Node]]:
        """Search for key in hash table
        
        Returns:
            tuple[int, Node]: (table index, found node) or (None, None) if not found
        """
        hash_value = self.hash_function(key)
        
        current = self.table[hash_value]
        while current:
            if current.key == key:
                return hash_value, current
            current = current.next
            
        return None, None

    def print_table(self):
        """Print hash table"""
        print("\nHash Table:")
        print("N\tHash Value\tKey\t\tCollisions")
        print("-" * 50)
        
        for i in range(self.size):
            current = self.table[i]
            while current:
                print(f"{i}\t{i}\t\t{current.key}\t\t{current.collisions}")
                current = current.next

def main():
    # Create hash table with size 16 (2^4)
    hash_table = HashTable(16)
    
    # Demonstration of inserting keys
    test_keys = ["apple", "banana", "cherry", "date", "elderberry", 
                 "fig", "grape", "apple", "honeydew", "banana"]
    
    print("Inserting keys...")
    for key in test_keys:
        result = hash_table.insert(key)
        print(f"Inserting '{key}': {'Success' if result else 'Already exists'}")
    
    # Show the final table
    hash_table.print_table()
    
    # Demonstration of searching
    print("\nSearching for keys...")
    search_keys = ["apple", "banana", "kiwi"]
    for key in search_keys:
        index, node = hash_table.search(key)
        if node:
            print(f"Key '{key}' found at index {index}, collisions: {node.collisions}")
        else:
            print(f"Key '{key}' not found")

if __name__ == "__main__":
    main()
