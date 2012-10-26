import os
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from decode_signed_request import parse_signed_request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST' and request.form.get('submit', ''):
        if liked:
            return render_template('form.html')
        if not liked:
            return render_template('root.html', data=dict(liked=liked, first_visit=False))
    signed_request = request.form.get('signed_request', '')
    if signed_request:
        signed_request = parse_signed_request(signed_request)
        liked = signed_request['page']['liked']
    else:
        liked = False
    
    return render_template('root.html', data=dict(liked=liked, first_visit=True))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
