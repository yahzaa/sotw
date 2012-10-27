import os
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    session,
    )
from werkzeug import secure_filename
from helpers import (
    parse_signed_request,
    allowed_file,
    RegistrationSchema,
    )
from formencode import Invalid
from flaskext.uploads import (
    UploadSet,
    configure_uploads,
    IMAGES,
    UploadNotAllowed,
    )
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

# DB Settings
localdb = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', localdb)
db = SQLAlchemy(app)

#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    mobile = db.Column(db.String(), unique=True)
    desc = db.Column(db.String())
    image = db.Column(db.String(200), unique=True)

# uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/', methods=['GET', 'POST'])
def root():
    signed_request = request.form.get('signed_request', '')
    if signed_request:
        decoded_request = parse_signed_request(signed_request)
        likes = decoded_request['page']['liked']
    else:
        likes = True # should be False doing it for local dev
    session['likes'] = likes
    css_url = url_for('static', filename='style.css')
    bg_url = url_for('static', filename='bg.gif')
    return render_template('root.html', data=dict(bg=bg_url, css=css_url, likes=likes))

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    errors = {}
    likes = session.get('likes', None)
    if likes:
        if request.method in ('GET', 'POST') and not request.form.get('submit_form', ''):
            return render_template('form.html', errors=errors)
        if request.method == 'POST' and request.form.get('submit_form', ''):
            #validate form data
            schema = RegistrationSchema()
            appstruct = dict(
                name = request.form.get('name', ''),
                email = request.form.get('email', ''),
                mobile = request.form.get('mobile', ''),
                desc = request.form.get('desc', ''),
                tnc = request.form.get('tnc', ''),
                )
            try:
                cstruct = schema.to_python(appstruct)
            except Invalid, e:
                return render_template('form.html', errors=e.error_dict)
            file = request.files.get('image', '')
            if not file:
                e = dict(image='please select an image')
                return render_template('form.html', errors=e)
            try:
                filename = photos.save(file)
            except UploadNotAllowed:
                e = dict(image="Please select an image file")
                return render_template('form.html', errors=e)
            user = User(
                name = cstruct['name'],
                email = cstruct['email'],
                mobile = cstruct['mobile'],
                desc = cstruct['desc'],
                image = filename,
                )
            db.session.add(user)
            try:
                db.session.commit()
            except OperationalError:
                e = dict(db='oops, something went wrong, please try again')
                return render_template('form.html', errors=e)
            except IntegrityError:
                e = dict(db='Someone with this email has already registered')
                return render_template('form.html', errors=e)
            return render_template('form.html', errors=dict(success=True))
    else:
        return "You are not a Fan!"

app.secret_key = 'seecreet'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
