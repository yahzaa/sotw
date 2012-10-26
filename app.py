import os
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from decode_signed_request import parse_signed_request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    signed_request = request.form.get('signed_request', '')
    if signed_request:
        decoded_request = parse_signed_request(signed_request)
        likes = decoded_request['page']['liked']
    else:
        likes = False
    session['likes'] = likes
    return render_template('root.html')

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    likes = session.get('likes', None)
    if likes:
        return render_template('form.html')
    else:
        return "You are not a Fan"

app.secret_key = 'seecreet'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
