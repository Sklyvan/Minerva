import unittest
from src.main.User import *
import glob, os

class UserTest(unittest.TestCase):
    def testImportExport(self):
        MyUser1 = User(1, "MyUser", [RSAKeys(fileName='EncKeys'), RSAKeys(fileName='SigKeys')],
                       "127.0.0.1", 'None', 'None', 'None', MessagesDB('Messages.db'))

        MyUser1.exportUser('User.json')

        MyUser2 = User(None, None, [None, None], None)
        MyUser2.importUser('User.json')

        self.assertEqual(MyUser1, MyUser2)

        for file in glob.glob("*.pem"): os.remove(file)
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.json"): os.remove(file)


if __name__ == '__main__':
    unittest.main()
