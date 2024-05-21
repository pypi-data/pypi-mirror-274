import hashlib
import time
import rsa


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
        def __init__(self):
            self.chain = [self.create_genesis_block()]

        def create_genesis_block(self):
            return Block(0, "0", int(time.time()), "Genesis Block", self.calculate_hash(0, "0", int(time.time()), "Genesis Block"))

        def calculate_hash(self, index, previous_hash, timestamp, data):
            value = str(index) + str(previous_hash) + str(timestamp) + str(data)
            return hashlib.sha256(value.encode('utf-8')).hexdigest()

        def add_block(self, data):
            index = len(self.chain)
            timestamp = int(time.time())
            hash = self.calculate_hash(index, self.chain[-1].hash, timestamp, data)
            block = Block(index, self.chain[-1].hash, timestamp, data, hash)

            if self.is_valid_new_block(block, self.chain[-1]):
                self.chain.append(block)

        def is_valid_new_block(self, new_block, previous_block):
            if previous_block.index + 1 != new_block.index:
                return False
            elif previous_block.hash != new_block.previous_hash:
                return False
            elif self.calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data) != new_block.hash:
                return False
            else:
                return True

        def is_chain_valid(self):
            for i in range(1, len(self.chain)):
                if not self.is_valid_new_block(self.chain[i], self.chain[i - 1]):
                    return False
                return True
                    
        def new_address(self):
            (public_key, private_key) = rsa.newkeys(512)
            public_key_str = public_key.save_pkcs1().decode()
            address = hashlib.sha256(public_key_str.encode()).hexdigest()
            return address, private_key