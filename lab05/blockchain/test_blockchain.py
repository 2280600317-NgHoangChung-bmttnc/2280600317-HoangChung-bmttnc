import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash="0")  # Khởi tạo khối Genesis

    def create_block(self, proof, previous_hash):
        block = Block(len(self.chain), time.time(), self.pending_transactions, proof, previous_hash)
        self.pending_transactions = []  # Reset danh sách giao dịch đang chờ xử lý
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_value = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_value[:4] == "0000":  # Điều kiện của thuật toán POW
                return new_proof
            new_proof += 1

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            prev_block = chain[i - 1]
            curr_block = chain[i]

            if curr_block.previous_hash != prev_block.hash:
                return False

            if curr_block.hash != curr_block.calculate_hash():
                return False

            if not curr_block.hash.startswith("0000"):  # Kiểm tra Proof of Work
                return False

        return True


# ====== CHƯƠNG TRÌNH CHÍNH ======
def main():
    my_blockchain = Blockchain()

    num_transactions = int(input("Nhập số lượng giao dịch bạn muốn thêm: "))
    for i in range(num_transactions):
        sender = input(f"Nhập tên người gửi cho giao dịch {i+1}: ")
        receiver = input(f"Nhập tên người nhận cho giao dịch {i+1}: ")
        amount = float(input(f"Nhập số tiền giao dịch {i+1}: "))
        my_blockchain.add_transaction(sender, receiver, amount)

    # Tiến hành đào block mới
    print("\n🔨 Đang thực hiện đào block...")
    previous_block = my_blockchain.get_previous_block()
    previous_proof = previous_block.proof
    new_proof = my_blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block.hash

    # Phần thưởng cho thợ đào
    miner_name = input("Nhập tên Miner: ")
    my_blockchain.add_transaction('Genesis', miner_name, 10)

    new_block = my_blockchain.create_block(new_proof, previous_hash)
    print("✅ Đào block thành công!")

    # Hiển thị blockchain
    print("\n===== 🔗 BLOCKCHAIN =====")
    for block in my_blockchain.chain:
        print(f"\n🟢 Block #{block.index}")
        print("📅 Timestamp:", block.timestamp)
        print("🔁 Transactions:", block.transactions)
        print("🔢 Proof:", block.proof)
        print("🔗 Previous Hash:", block.previous_hash)
        print("🔑 Hash:", block.hash)
        print("----------------------")

    # Kiểm tra tính hợp lệ của blockchain
    print("\n🔍 Kiểm tra tính hợp lệ của blockchain...")
    if my_blockchain.is_chain_valid(my_blockchain.chain):
        print("✅ Blockchain hợp lệ!")
    else:
        print("❌ Blockchain KHÔNG hợp lệ!")

if __name__ == "__main__":
    main()
