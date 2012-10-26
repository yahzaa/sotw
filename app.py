import os
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from helpers import parse_signed_request
from helpers import allowed_file
from helpers import RegistrationSchema
from formencode import Invalid

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
    errors = {}
    likes = session.get('likes', None)
    if likes:
        if request.method in ('GET', 'POST') and not request.form.get('submit', ''):
            return render_template('form.html', errors=errors)
        if request.method == 'POST' and request.form.get('submit', ''):
            #validate form data
            schema = RegistrationSchema()
            appstruct = dict(
                first_name = request.form.get('first_name', ''),
                last_name = request.form.get('last_name', ''),
                email = request.form.get('email', ''),
                phone = request.form.get('phone', ''),
                location = request.form.get('location', ''),
                tnc = request.form.get('tnc', ''),
                image = request.form.get('image', ''),
                )
            try:
                cstruct = schema.to_python(appstruct)
            except Invalid, e:
                return render_template('form.html', errors=e.error_dict)
            '''user = User(form.first_name.data, form.last_name.data,
                        form.email.data, form.phone.data,
                        form.location.data, image_name)
            db_session.add(user)
            flash('Thanks for registering')'''
            return "Thanks for registering"
        return render_template('form.html', errors=errors)
    else:
        return "You are not a Fan"

app.secret_key = 'seecreet'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
