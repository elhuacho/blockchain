from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok
from blockchain import Blockchain

# Crear una aplicación web
app = Flask(__name__)
# run_with_ngrok(app)

# Si se obtiene un error 500, actualizar flask y ejecutar la siguiente línea
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creación de la Blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    """ Minado de un nuevo bloque """

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message' : '¡Enhorabuena, has minado un nuevo bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    """ Obtención de la Blockchain """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    """ Comprobación si la Blockchain es válida """

    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': '¡La cadena de bloques es válida!'}
    else:
        response = {'message': '¡La cadena de bloques NO es válida!'}
    return jsonify(response), 200

app.run(host='127.0.0.1', port=5000)