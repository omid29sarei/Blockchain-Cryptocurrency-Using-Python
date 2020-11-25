from flask import Flask

class Blockchain:


    def __init__(self):
        """
        this is the init function to initialize 
        Blockchain class
        """
        self.transaction = []
        self.chain = []
        
#initialize the Blockchain Class
blockchain = Blockchain()

#initialize the Node
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p','--port',default=5001, type=int, help='Port to Listen to')
    args = parser.parse_args()
    port  = args.port

    app.run(host='127.0.0.1',port=port,debug=True)