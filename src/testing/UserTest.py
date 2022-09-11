import unittest
from src.main.User import *
import glob, os

class UserTest(unittest.TestCase):
    def testImportExportData(self):
        MyUser1 = User(1, "MyUser", [RSAKeys(fileName='EncKeys'), RSAKeys(fileName='SigKeys')],
                       "127.0.0.1", 'None', 'None', 'None', MessagesDB('Messages.db'))

        MyUser1.exportUser('User.json')

        MyUser2 = User(None, None, [None, None], None)
        MyUser2.importUser('User.json')

        self.assertEqual(MyUser1, MyUser2)

        for file in glob.glob("*.pem"): os.remove(file)
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.json"): os.remove(file)

    def testImportExportKeys(self):
        MyUser1 = User(1, 'User1', [RSAKeys(fileName='EncKeys'), RSAKeys(fileName='SigKeys')], "127.0.0.1")
        MyUser1.exportKeys('EncKeys.pem', 'SigKeys.pem')

        MyUser2 = User(2, 'User2', [RSAKeys(fileName='TempE', toImport=True), RSAKeys(fileName='TempS', toImport=True)], "127.0.0.2")
        MyUser2.importKeys('EncKeys.pem', 'SigKeys.pem')

        self.assertEqual(MyUser1.encryptionKeys, MyUser2.encryptionKeys, "Encryption keys are not equal.")
        self.assertEqual(MyUser1.signingKeys, MyUser2.signingKeys, "Signing keys are not equal.")
        self.assertTrue(MyUser1.checkKeys(), "Keys 1 are not valid.")
        self.assertTrue(MyUser2.checkKeys(), "Keys 2 are not valid.")

        for file in glob.glob("*.pem"): os.remove(file)
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.json"): os.remove(file)


if __name__ == '__main__':
    unittest.main()
