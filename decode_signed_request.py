import hmac
import json

from base64 import urlsafe_b64decode
from hashlib import sha256

def parse_signed_request(signed_request):
    [encoded_sig, payload] = signed_request.split('.')

    # decode data
    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    return data

def base64_url_decode(input):
    input += '=' * (4 - (len(input) % 4))
    return urlsafe_b64decode(input.encode('utf-8'))
