# BlendMAS

This repo is to demonstrate the implementation of [BlenMAS](https://ieeexplore.ieee.org/document/8946177) A Blockchain-Enabled Decentralized Microservices Architecture for Smart Public Safety. It proposed to offer a decentralized, scalable and secured data sharing and access control to distributed IoT based SPS , using edge-fog computaion. 

Edge device capture the ununsual activities , and perform edge computation and image processing on fog devices , thus it can reduce the server load and server can work on blockchain compuation to store these images and maintain secure immutable storage using consensus algo.

- hog_edge.py : It has Hog feature selection script which can replicate on edge device for initial computation.
- fog.py : It performs edge detection using Open-CV for image send by edge device(hog_edge.py)
- helper.py: It performs assymetric encryption for key that is used to encode and decode image using XOR operations.

> Instead of edge device, we can run them on local system for quick execution.

### RUN on Local System

- Create python virtual environment
- [RUN]: pip install -r requirements.txt
- Create table in sql, with col email and private_key varchar(512) , add its configuration to env.py file
- [RUN]: export FLASK_APP=app.py  && flask run —port=”give your port number”.
- Call '/register/user', methods=['POST'] API , to register new users in order to create new transactions.
> For body refer to blockhain_api.json 
- [RUN]: python hog_edge.py “path to image”, give path to image which need to be sent into blockchain.
- [RUN]: python fog.py  ,   enter the number to encrypt the image with a username that is used to register the user and port(replicate to which node we want to send data).

#### Block 
```
{
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
 }
```
#### Transaction
List of:
```
{
            "sender":sender,
            "recipient":recipient,
            "data":image,
}
```

For mining we have used proof of work to verify the block and puzzle for miners.
- **Proof of work** :  It is a method that requires members of a network to expend effort solving a puzzle to prevent anybody from altering the network.
  - Find a number p that when hashed with the previous block's solution a hash with 3 leading 0 is produced.

We've got a fully valid basic Blockchain that accepts transactions and allows us to mine a new block ,but  Blockchain needs to be decentralized, and do we ensure that all the data reflect the same chain.. , we can use consesus algo. We have use basic consensus method .
- **Consensus**:Each node on our network needs to keep a registry of other nodes on the network,thus conflict is when one node has a different chain to another node. To resolve this, we'll make the rule that the longest valid chain is authoritative .

We have successfully build basic blockchain to perform edge-fog architecture for computaion and save data over immutable secure network.

- One can use feature selection and edge detection script on *edge device* with trained object detection model to capture unusual activity and after image processing it can send over the blockchain network.




