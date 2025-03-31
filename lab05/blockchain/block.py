import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (str(self.index) + 
                str(self.previous_hash) + 
                str(self.timestamp) + 
                str(self.transactions) + 
                str(self.proof))
        return hashlib.sha256(data.encode()).hexdigest()

# Ví dụ tạo một khối mới
if __name__ == "__main__":
    transactions = [{"sender": "Alice", "receiver": "Bob", "amount": 10}]
    new_block = Block(index=1, previous_hash="0", timestamp=time.time(), transactions=transactions, proof=100)
    
    print("Block Hash:", new_block.hash)
