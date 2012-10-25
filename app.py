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
        if signed_request:
            signed_request = parse_signed_request(signed_request)
        else:
            return "signed request not available"
        page = signed_request['page']
        submit = request.form.get('submit', '')
        if submit and page['liked']:
            return render_template('form.html')
        if submit and not page['liked']:
            return render_template('root.html', liked=False)
        return render_template('root.html', liked=False)
    return render_template('root.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
