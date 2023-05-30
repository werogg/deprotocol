""" Util class to handle different encryption operations """

import base64
import json

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from deprotocol.app.logger import Logger  # pylint: disable=import-error


def generate_keys():
    """ Generate a pair public,private key for data exchange encryption purposes """
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    Logger.get_logger().trace(f'crypto_funcs: Generated Private Key: \n{private_key.export_key().decode()}')
    Logger.get_logger().trace(f'crypto_funcs: Generated Public Key: \n{public_key.export_key().decode()}')

    return public_key, private_key


def encrypt_chunk(chunk, key):
    """ Encrypt a chunk of bytes using a key """
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(chunk)


def decrypt_chunk(chunk, key):
    """ Decrypt a chunk of bytes using a key """
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(chunk)


def encrypt(data, key, chunk_size=214):
    """ Encrypt bytes using a key in chunks """
    encrypted_chunks = []

    # Encrypt the bytes in chunks
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        encrypted_chunk = encrypt_chunk(chunk, key)
        encrypted_chunks.append(encrypted_chunk)

    # Concatenate the encrypted chunks and return as base64 encoded string
    encrypted_message = b''.join(encrypted_chunks)
    return base64.b64encode(encrypted_message)


def decrypt(data, key, chunk_size=256):
    """ Decrypt a base64 encoded encrypted message using a key in chunks """
    encrypted_message = base64.b64decode(data)
    decrypted_chunks = []

    # Decrypt the encrypted message in chunks
    for i in range(0, len(encrypted_message), chunk_size):
        chunk = encrypted_message[i:i + chunk_size]
        decrypted_chunk = decrypt_chunk(chunk, key)
        decrypted_chunks.append(decrypted_chunk)

    return b''.join(decrypted_chunks)


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
