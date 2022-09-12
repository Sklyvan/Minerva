import unittest
import random, glob, os
from src.cryp.RSAKeys import *


class RSATesting(unittest.TestCase):
    def testEncryptionDecryption1024(self):
        keys = RSAKeys(1024, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "1024 Encryption/Decryption failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testSigningVerification1024(self):
        keys = RSAKeys(1024, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "1024 Signing/Verification failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testEncryptionDecryption2048(self):
        keys = RSAKeys(2048, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "2048 Encryption/Decryption failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testSigningVerification2048(self):
        keys = RSAKeys(2048, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "2048 Signing/Verification failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testEncryptionDecryption4096(self):
        keys = RSAKeys(4096, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "4096 Encryption/Decryption failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testSigningVerification4096(self):
        keys = RSAKeys(4096, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "4096 Signing/Verification failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testEncryptionDecryption8192(self):
        keys = RSAKeys(8192, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(keys.decrypt(cipher), text,
                         "8192 Encryption/Decryption failed.")
        for file in glob.glob("TestKey*"): os.remove(file)

    def testSigningVerification8192(self):
        keys = RSAKeys(8192, fileName='TestKey')
        # Generate a random text
        text = (''.join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        signature = keys.sign(text)
        self.assertTrue(keys.verify(text, signature, keys.publicKey),
                        "8192 Signing/Verification failed.")
        for file in glob.glob("TestKey*"): os.remove(file)


    def testImportExport(self):
        Keys1 = RSAKeys(fileName='TestKey')
        Keys2 = RSAKeys(fileName='TestKey', toImport=True)

        Keys1.exportKeys("TestKey")
        Keys2.importKeys("TestKey")

        self.assertTrue(Keys1 == Keys2, "Import/Export failed.")
        for file in glob.glob("TestKey*"): os.remove(file)


if __name__ == '__main__':
    unittest.main()
