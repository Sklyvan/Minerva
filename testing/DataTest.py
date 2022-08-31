import unittest
from src.data.MessagesDB import *
from src.main.User import *

class MessageTest(unittest.TestCase):
    def testMessageSecurity(self):
        User1 = User(1, "User1", [RSAKeys(), RSAKeys()], "127.0.0.1", ForwardingTable(), Queue(), {}, MessagesDB())
        User1Public = PublicUser(1, "User1", [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
                                      Circuit())
        User2 = User(2, "User2", [RSAKeys(), RSAKeys()], "127.0.0.2", ForwardingTable(), Queue(), {}, MessagesDB())
        User2Public = PublicUser(2, "User2", [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
                                      Circuit())

        Message1U1 = Message(1, b"Hello World!", b"", Circuit(), User1, User2Public, time()) # Create a sample message
        # Initially, the message is not encrypted or signed. We encrypt for User 2 and sign as User 1.
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(1, Message1U1.content, Message1U1.signature, Circuit(), User1Public, User2,
                             Message1U1.timeSent, time(), True, True) # Simulate the message being sent to User 2
        self.assertTrue(Message1U2.verify(), "Verification failed.") # Verify the signature
        Message1U2.decrypt() # Decrypt the message
        self.assertEqual(Message1U2.content, b"Hello World!", "Decryption failed.")

if __name__ == '__main__':
    unittest.main()
