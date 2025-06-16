import random
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def generate_otp():
    """
    Generate a random 4-digit OTP.
    """
    return random.randint(1000, 9999)


def enc_uname(username):
    """
    Encode the username to a URL-safe base64 string.
    """
    return urlsafe_base64_encode(force_bytes(username))


def dec_uname(encoded_username):
    """
    Decode the URL-safe base64 string back to the original username.
    """
    try:
        return force_str(urlsafe_base64_decode(encoded_username))
    except (ValueError, TypeError):
        return None  # Return None if decoding fails
    
    