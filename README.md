# Blockchain-Cryptocurrency-Using-Python

This is POC of the Blockchain itself and some other protocols such as consensus in order to make sure all the node are synced properly.
Also within this POC there the implementation of proof of work.

This was built by using Python as the Backend Lnaguage and for the Frontend it uses HTML,CSS,Javascript


## How To Run The Block Chain Locally:

**In order to run both the blockchain and the client portal you need to follow these step individually**.

- First need to be Cloned to your local system
- Once it was cloned succesfully then you need to navigate to the folder using command line 

### How To Run The Blockchain Node
*THESE COMMANDS NEED TO BE RUN FROM COMMAND LINE*
*By Default The Port is 5001 But Can Be Changed to Any Port By Including The -P Flag*
- cd blockchain
- python blockchain.py
- Optionally you can pass a -p flag in order to specify the port as well
- navigate to your localost and the default port is 5001 but you can change this by using -p as it was mentioned eariler 


### How To Run The Client Dashboard

- if you are on the blockchain folder then you need to do cd ../ in order to go once step back
- once you were on the root of your folder then $ cd blockchain_client
- python blockchain_client.py
- navigate to your localost and port 8081 is the default port 
***Note: You Can Always type 127.0.0.1:portnumber instead of localhost because on each machine 127.0.0.1 is the local address***



