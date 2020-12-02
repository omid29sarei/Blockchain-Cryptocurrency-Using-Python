from flask import Flask,render_template,jsonify,request
from time import time
from flask_cors import CORS
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from collections import OrderedDict
import binascii
from uuid import uuid4
import json
import hashlib
import requests
from urllib.parse import urlparse


MINING_SENDER = 'The Blockchain'
MINING_REWARD = 1
MINING_DIFFICULTY = 2

class Blockchain:


    def __init__(self):
        """
        this is the init function to initialize 
        Blockchain class
        """
        self.transaction = []
        self.chain = []
        self.nodes = set()
        self.node_id = str(uuid4()).replace('-','')
        #creating the genesis block
        self.create_block(0,'00')

    def register_node(self,node_url):
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')



    def create_block(self,nonce,previous_hash):
        """
        Add a block of trancsaction to the blockchain
        """
        block ={"block_number":len(self.chain) + 1,
                "timestampt":time(),
                "transaction":self.transaction,
                "nonce":nonce,
                "previous_hash":previous_hash
                }
        # Reset the transaction
        self.transaction =[]
        self.chain.append(block)
        return block
    
    def verify_transaction_signature(self,sender_public_key,signature,transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        hashed_public_key = SHA.new(str(transaction).encode('utf-8'))
        try:
            verifier.verify(hashed_public_key,binascii.unhexlify(signature))
            return True
        except ValueError:
            return False

    def submit_transaction(self,sender_public_key,recipient_pubic_key,signature,amount):
    
        transaction = OrderedDict({
            'sender_public_key':sender_public_key,
            'recipient_public_key':recipient_pubic_key,
            'amount':amount
        })

         #TODO: Reward The Miner
        #reward the mining
        if(sender_public_key == MINING_SENDER):
            self.transaction.append(transaction)
            return len(self.chain) + 1
        else:
            #TODO: Signature Validation

            #transaction from wallet to wallet
            signature_verification = self.verify_transaction_signature(sender_public_key,signature,transaction)
            if(signature_verification):
                self.transaction.append(transaction)
                return len(self.chain) + 1
            else:
                return False

    @staticmethod
    def valid_proof(transaction,last_hash,nonce,difficulty=MINING_DIFFICULTY):
        guess = (str(transaction) + str(last_hash) + str(nonce)).encode('utf8')
        h = hashlib.new('sha256')
        h.update(guess)
        guess_hashed = h.hexdigest()
        return guess_hashed[:difficulty] == '0' * difficulty

    def proof_of_work(self):
        last_block = blockchain.chain[-1]
        nonce = 0 
        last_hash = self.hash(last_block)
        while(self.valid_proof(self.transaction,last_hash,nonce)) is False:
            nonce += 1

        return nonce
    
    @staticmethod
    def hash(block):
        # We Must To Ensure The Dictionary is Ordered, Otherwise we will get inconsistant hash
        block_string = json.dumps(block,sort_keys=True).encode('utf8')
        h = hashlib.new('sha256')
        h.update(block_string)
        result = h.hexdigest()
        return result

    def valid_chain(self,chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            transactions = block['transactions'][:-1]
            transaction_elements = ['sender_public_key','recipient_public_key','amount']
            transaction = [OrderedDict((k, transaction[k]) for k in transaction_elements) for transaction in transactions]
            if not self.valid_proof(transaction,block['previous_hash'],block['nonce'],MINING_DIFFICULTY):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get('http://' + node + '/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    

        
#initialize the Blockchain Class
blockchain = Blockchain()

#initialize the Node
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/configure')
def configure():
    return render_template('./configure.html')


@app.route('/transactions/get',methods=['GET'])
def get_transaction():
    transaction = blockchain.transaction
    response = {'transactions':transaction}
    return jsonify(response),200


@app.route('/mine',methods=['GET'])
def mine():
    #We Run The Proof Of Work Algorithm 
    nonce = blockchain.proof_of_work()

    blockchain.submit_transaction(sender_public_key=MINING_SENDER,
                                  recipient_pubic_key=blockchain.node_id,
                                  signature= '',
                                  amount= MINING_REWARD )

    last_block = blockchain.chain[-1]
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce,previous_hash)
    response = {
                'message': 'New Block Created',
                'block_number':block['block_number'],
                'transactions':block['transaction'],
                'nonce':block['nonce'],
                'previous_hash':block['previous_hash']

            }
    return jsonify(response),200


@app.route('/chain',methods=['GET'])
def get_chain():

    response ={
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
     }
    return jsonify(response),200


@app.route('/nodes/get',methods=['GET'])
def get_nodes():

    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}

    return jsonify(response),200


@app.route('/nodes/resolve',methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message':'Our Chain Was Replaces',
            'new_chain':blockchain.chain
        }
    else:
        response = {
            'message':'Our Chain is Authoritative',
            'chain':blockchain.chain
        }
    return jsonify(response),200

@app.route('/nodes/register',methods=['POST'])
def register_node():
    values = request.form
    nodes = values.get('nodes').replace(' ','').split(',')

    if nodes is None:
        return 'This is an Error. Please Supplu a valid list of nodes', 400
    for node in nodes:
        blockchain.register_node(node)

    response ={
        'message':'Nodes Have Been Added',
        'total_nodes': [node for node in blockchain.nodes]
    }

    return jsonify(response),200

@app.route('/transaction/new',methods=['POST'])
def new_transaction():
    values = request.form

    #check the vrequired field
    required_attr = ['confirmation_sender_public_key','confirmation_recipient_public_key','transaction_signature','confirmation_amount']
    if not all(k in values for k in required_attr):
        return 'Missing Values',400

    transaction_result = blockchain.submit_transaction(values['confirmation_sender_public_key'],
                                                       values['confirmation_recipient_public_key'],
                                                       values['transaction_signature'],
                                                       values['confirmation_amount'])

    if(transaction_result == False):
        response = {'message':'Invalid Transaction!!'}
        return jsonify(response), 406
    else:
        response = {'message':'Transaction Will Be Added To The Block' + str(transaction_result)}
        return jsonify(response), 201

    


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p','--port',default=5001, type=int, help='Port to Listen to')
    args = parser.parse_args()
    port  = args.port

    app.run(host='127.0.0.1',port=port,debug=True)

