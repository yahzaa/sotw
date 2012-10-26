# Helper Methods

import hmac
import json
from base64 import urlsafe_b64decode
from hashlib import sha256

## Parse and decode Facebook signed request
def parse_signed_request(signed_request):
    [encoded_sig, payload] = signed_request.split('.')

    # decode data
    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    return data

def base64_url_decode(input):
    input += '=' * (4 - (len(input) % 4))
    return urlsafe_b64decode(input.encode('utf-8'))

## Return true if the filename is allowed (name and extension)
ALLOWED_EXTENSIONS = ('jpg', 'gif', 'jpeg', 'bmp',)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

## Submit form schema and validations
from wtforms import Form, BooleanField, TextField, FileField, IntegerField, validators

class RegistrationForm(Form):
    first_name = TextField('First Name', [validators.required(), validators.Length(min=4, max=50)])
    last_name = TextField('Last Name', [validators.optional(), validators.Length(min=4, max=50)])
    email = TextField('Email', [validators.required(), validators.Length(min=6, max=50)])
    location = TextField('Location', [validators.required(), validators.Length(min=2, max=50)])
    phone = IntegerField('Phone', [validators.required(), validators.Length(min=10, max=10)])
    image = FileField('Select an image', [validators.required()])
    accept_tnc = BooleanField('I accept the Terms and Conditions', [validators.required()])
