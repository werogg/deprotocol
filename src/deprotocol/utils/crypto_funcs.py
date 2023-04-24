""" Util class to handle different encryption operations """

import base64
import json

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from deprotocol.logger.logger import Logger  # pylint: disable=import-error


def generate_keys():
    """ Generate a pair public,private key for data exchange encryption purposes """
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()
    Logger.get_logger().trace(f'crypto_funcs: Generated Private Key: \n{private_key.export_key().decode()}')
    Logger.get_logger().trace(f'crypto_funcs: Generated Public Key: \n{public_key.export_key().decode()}')

    return public_key, private_key


def encrypt(message, key):
    """ Encrypt a str message using a key """
    message = json.dumps(message).encode("utf-8")
    cipher = PKCS1_OAEP.new(key)
    return base64.b64encode(cipher.encrypt(message)).decode("utf-8")


def decrypt(message, key):
    """ Decrypt a str message using a key"""
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(base64.b64decode(message))
    return json.loads(message)


def load_key(key):
    """ Load an existing KEY"""
    key = base64.b64decode(key)
    return RSA.importKey(key)


def serialize_key(key):
    """ Serialize a key """
    key = base64.b64encode(key.exportKey("DER")).decode("utf-8")
    return key


def get_digest(message):
    digest = SHA256.new()
    digest.update(str(message).encode("utf-8"))
    return digest


def sign(message, private_key):
    """ Write a signature using a private key """
    digest = get_digest(message)
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)

    return base64.b64encode(sig).decode("utf-8")


def verify(message, sig, key):
    """ Verify a signature using a public key """
    digest = get_digest(message)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(digest, base64.b64decode(sig))
