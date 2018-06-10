import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4



class Blockchain(object):

    def __init__(self):
        self.current_transactions = []
        self.chain = []

    # Create the genesis block
        genesis_block = self.new_block(previous_hash=1, proof=100)
        self.chain.append(genesis_block)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.chain[-1]['hash']
            }

        # Calculate the hash of this new Block
        block['hash'] = self.hash(block)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        """

        block_string = json.dumps(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod # Hashing algo section
    def valid_proof(last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "ff"

    @staticmethod
    def proof_of_work(last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while True:
            guess = f'{last_proof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:2] == "ff":
                break

            proof += 1

        print(dedent(f'''
            New Proof found!
            
             New Proof: {proof}
            Last Proof: {last_proof}
                  Hash: {guess_hash}
        '''))
        return proof


"""
Copyright © 2018 FreeFlo . All rights reserved.
"""
