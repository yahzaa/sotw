import os
from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root(signed_request, page):
    return page


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
