import hashlib

def blake2(tin_nhan):
    blake2_hash = hashlib.blake2b(digest_size=64)  # Sửa 'kích thước tóm tắt' thành 'digest_size'
    blake2_hash.update(tin_nhan)
    return blake2_hash.digest()

def main():
    text = input("Nhập chuỗi văn bản: ").encode('utf-8')
    hashed_text = blake2(text)

    print("Chuỗi văn bản đã nhập:", text.decode('utf-8'))
    print("BLAKE2 Hash:", hashed_text.hex())

if __name__ == "__main__":
    main()
