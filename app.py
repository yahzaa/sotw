import os
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    return 'Hello World!'

@app.route('/hello')
def hello():
    return 'Hello'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
