import base64
import os
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from decode_signed_request import parse_signed_request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        signed_request = request.form.get('signed_request', '')
        page = request.form.get('page', '')
        if signed_request:
            data = parse_signed_request(signed_request)
            return data
        return "no signed request"
    return "Root"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
