import unittest
import random, glob, os
from src.cryp.RSAKeys import *


class RSATesting(unittest.TestCase):
    def testEncryptionDecryption1024(self):
        keys = RSAKeys(1024, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 50))])
        text = text.encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "1024 Encryption/Decryption failed.")

    def testSigningVerification1024(self):
        keys = RSAKeys(1024, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 50))])
        text = text.encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "1024 Signing/Verification failed.")

    def testEncryptionDecryption2048(self):
        keys = RSAKeys(2048, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 100))])
        text = text.encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "2048 Encryption/Decryption failed.")

    def testSigningVerification2048(self):
        keys = RSAKeys(2048, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 100))])
        text = text.encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "2048 Signing/Verification failed.")

    def testEncryptionDecryption4096(self):
        keys = RSAKeys(4096, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 100))])
        text = text.encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "4096 Encryption/Decryption failed.")

    def testSigningVerification4096(self):
        keys = RSAKeys(4096, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 100))])
        text = text.encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "4096 Signing/Verification failed.")

    def testEncryptionDecryption8192(self):
        keys = RSAKeys(8192, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 100))])
        text = text.encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "8192 Encryption/Decryption failed.")

    def testSigningVerification8192(self):
        keys = RSAKeys(8192, fileName='TestKey')
        # Generate a random text
        text = ''.join([chr(random.randint(0, 255)) for i in range(0, random.randint(0, 100))])
        text = text.encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "8192 Signing/Verification failed.")


    def testImportExport(self):
        Keys1 = RSAKeys(fileName='TestKey')
        Keys2 = RSAKeys(fileName='TestKey', toImport=True)

        Keys1.exportKeys("TestKey")
        Keys2.importKeys("TestKey")

        self.assertTrue(Keys1 == Keys2, "Import/Export failed.")


if __name__ == '__main__':
    unittest.main()