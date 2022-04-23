from uuid import uuid4
from urllib.parse import urlparse
import requests
import base64
import io
from flask import Flask, jsonify, request
from blockchain import BlockChain
from helper import create_key_pair,encode_decode_img
from time import time
import numpy as np
from env import mydb
from cryptography.fernet import Fernet
from PIL import Image

mycursor = mydb.cursor()
# initiate the node
app = Flask(__name__)
# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# initiate the Blockchain
blockchain = BlockChain()

@app.route('/mine', methods=['GET'])
def mine():
    try:
        # first we need to run the proof of work algorithm to calculate the new proof..
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
    
        # we must recieve reward for finding the proof in form of receiving 1 Coin
        blockchain.new_transaction(
            sender=0,
            recipient=node_identifier,
            amount=str(1),
        )
    
        # forge the new block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
    
        response = {
            'message': "Forged new blockchain.",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response, 200)
    except Exception as err:
        return jsonify(err, 400)

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    try:
        # print(request.json)      
        if not request.json or 'image' not in request.json: 
            abort(400)
                
        # get the base64 encoded string
        
        values = request.get_json()
        required = ['sender', 'recipient', 'image','message']
    
        if not all(k in values for k in required):
            return 'Missing values.', 400
        #mysql query
        mycursor = mydb.cursor()
        print('hi')
        sql = "select *from user_info where email="+"'"+values['sender']+"'"
        mycursor.execute(sql)
        res=mycursor.fetchall()
        if not res:
            return "user address not found",400
     
        fernet = Fernet(res[0][1])
        key= fernet.decrypt(values['message'].encode()).decode()
        img_arr=encode_decode_img(bytearray(values['image'].encode()), key)
        # create a new transaction
        index = blockchain.new_transaction(
            sender = values['sender'],
            recipient = values['recipient'],
            amount = str(img_arr)
        )
       
        response = {
            'message': f'Transaction will be added to the Block {index}',
        }
        return jsonify(response, 200)
    except Exception as err:
        return err,400

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    print('values',values)
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    # register each newly added node
    for node in nodes: blockchain.register_node(node)

    response = {
        'message': "New nodes have been added",
        'all_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 201

@app.route('/register/user', methods=['POST'])
def register_user():
    values = request.get_json()

    print('values',values)
    user= values.get('user')
    if user is None:
        return "no user_name given", 400

    # register new user
    try:
        response=create_key_pair(user)
        return jsonify(response), 201
    except Exception as err:
        return jsonify(err),400

@app.route('/nodes/resolve', methods=['POST'])
def consensus():
    # an attempt to resolve conflicts to reach the consensus
    conflicts = blockchain.resolve_conflicts()
    
    if(conflicts):
        response = {
            'message': 'Our chain was replaced.',
            'new_chain': blockchain.chain,
        }
        return jsonify(response), 200
    
    response = {
        'message': 'Our chain is authoritative.',
        'chain': blockchain.chain,
    }
    return jsonify(response), 200
import traceback
@app.route("/test", methods=['POST'])
def test_method():         
    try:
        # print(request.json)      
        if not request.json or 'image' not in request.json: 
            abort(400)
                
        # get the base64 encoded string
        
        values = request.get_json()
        required = ['sender', 'recipient', 'image','message']
    
        if not all(k in values for k in required):
            return 'Missing values.', 400
        #mysql query
        mycursor = mydb.cursor()
        print('hi')
        sql = "select *from user_info where email="+"'"+values['sender']+"'"
        mycursor.execute(sql)
        res=mycursor.fetchall()
        if not res:
            return "user address not found",400
     
        fernet = Fernet(res[0][1])
        key= fernet.decrypt(values['message'].encode()).decode()
        img_arr=encode_decode_img(bytearray(values['image'].encode()), key)
        # create a new transaction
        index = blockchain.new_transaction(
            sender = values['sender'],
            recipient = values['recipient'],
            amount = str(img_arr)
        )
       
        response = {
            'message': f'Transaction will be added to the Block {index}',
        }
        return jsonify(response, 200)
    except Exception as err:
        return err,400

if __name__ == '__main__':
    app.run(host='0.0.0.0')