import hashlib
import time
from block import Block  # Đảm bảo có file block.py chứa class Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=1, previous_hash='0')  # Khởi tạo block genesis

    def create_block(self, proof, previous_hash):
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=time.time(),
            transactions=self.current_transactions,
            proof=proof
        )
        self.current_transactions = []  # Reset danh sách giao dịch
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]  # Lấy block cuối cùng trong chuỗi

    def proof_of_work(self, previous_proof):
        """Tìm số proof sao cho hash của nó có 4 số 0 đầu tiên."""
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":  # Điều kiện POW hợp lệ
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        """Thêm giao dịch vào danh sách chờ xử lý"""
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block().index + 1  # Trả về index của block chứa giao dịch này

    def is_chain_valid(self, chain):
        """Kiểm tra xem blockchain có hợp lệ không"""
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Kiểm tra nếu hash của block trước có khớp với previous_hash của block sau không
            if block.previous_hash != previous_block.hash:
                return False

            # Kiểm tra proof-of-work hợp lệ
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1
        return True