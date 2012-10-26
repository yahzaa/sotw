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

##  form schema and validations
import formencode
from formencode import validators 

class RegistrationSchema(formencode.Schema):
    first_name = validators.String(not_empty=True)
    last_name = validators.String()
    email = validators.Email(resolve_domain=True)
    location = validators.String(not_empty=True)
    phone = validators.Int(not_empty=True)
    image = validators.FieldStorageUploadConverter(not_empty=True)
    tnc = validators.StringBool(if_missing=False)
