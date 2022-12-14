import os

AES_KEY_SIZE = 32
AES_NONCE_SIZE = 15

DFH_CURVE = "SECP384R1"
DFH_HASH = "SHA256"
DFH_SALT_SIZE = 32

RSA_KEY_SIZE = 2048
RSA_KEYS_NAME = "RSAKeys"

RSA_KEY_GEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RSA.bin")

RSA_KEY_EXTENSION = "pem"
DFH_KEY_EXTENSION = "dfh"
AES_KEY_EXTENSION = "aes"
