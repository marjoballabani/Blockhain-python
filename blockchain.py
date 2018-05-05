# CREATE A BLOCKCHAIN
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                    check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        i = 1
        
        while i < len(chain):
            block = chain[i]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = chain[i]
            i +=1
        
        return True
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def get_previous_block(self):
        return self.chain[-1]

            
# Create Web App

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    new_block = blockchain.create_block(proof, previous_hash)
    
    return jsonify(new_block), 200
    

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    return jsonify(blockchain.chain), 200

app.run(host = "0.0.0.0", port = 5000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    