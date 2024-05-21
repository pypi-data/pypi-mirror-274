from flask import Flask, render_template
from Blockchain import Blockchain, Block

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html')
            
if __name__ == '__main__':
    app.run(host="127.0.0.127", port=8008, debug=True)
