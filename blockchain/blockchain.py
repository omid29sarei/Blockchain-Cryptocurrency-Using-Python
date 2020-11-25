from flask import Flask,render_template
import time from time
class Blockchain:


    def __init__(self):
        """
        this is the init function to initialize 
        Blockchain class
        """
        self.transaction = []
        self.chain = []
        #creating the genesis block
        self.create_block(0,'00')
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
        
#initialize the Blockchain Class
blockchain = Blockchain()

#initialize the Node
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p','--port',default=5001, type=int, help='Port to Listen to')
    args = parser.parse_args()
    port  = args.port

    app.run(host='127.0.0.1',port=port,debug=True)

