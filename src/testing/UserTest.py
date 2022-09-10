import unittest
from src.main.User import *

class UserTest(unittest.TestCase):
    def testImportExport(self):
        MyUser1 = User(1, "MyUser", [RSAKeys(fileName='../keys/EncKeys'), RSAKeys(fileName='../keys/SigKeys')],
                       "127.0.0.1", 'None', 'None', 'None', MessagesDB('../data/Messages.db'))

        MyUser1.exportUser('../data/User.json')

        MyUser2 = User(None, None, [None, None], None)
        MyUser2.importUser('../data/User.json')

        self.assertEqual(MyUser1, MyUser2)


if __name__ == '__main__':
    unittest.main()
