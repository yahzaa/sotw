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

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

photos = UploadSet('photos', IMAGES)

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
        if request.method in ('GET', 'POST') and not request.form.get('submit_form', ''):
            return render_template('form.html', errors=errors)
        if request.method == 'POST' and request.form.get('submit_form', ''):
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
            file = request.files.get('image', '')
            if not file:
                e = dict(image='please select an image')
                return render_template('form.html', errors=e)
            if file:
                filename = photos.save(file)
                rec = Photo(filename=filename)
                rec.store()
                return "Thanks for registering"
            if not file:
                return "no file"
            if not allowed_file(file.filename):
                return "filename not allowed"
    else:
        return "You are not a Fan"

app.secret_key = 'seecreet'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
