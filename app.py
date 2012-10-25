import base64
import os
import json
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
        signed_request = parse_signed_request(signed_request)
        page = signed_request['page']
        if page:
            return render_template('root.html', data=page)
        return "no page param"
    return "Root"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
