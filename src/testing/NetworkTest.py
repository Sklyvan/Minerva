from src.main.App import *


def testSendReceiveMessage():
    threading.Thread(
        target=subprocess.call, args=(openWebSocket,), kwargs={"shell": True}
    ).start()

    args = ["$", "-n", "TestUser1"]
    User1 = initializeUser(args)
    User1Public = PublicUser(
        User1.userID,
        User1.userName,
        [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
        Circuit(),
    )
    args = ["$", "-n", "TestUser2"]
    User2 = initializeUser(args)
    User2Public = PublicUser(
        User2.userID,
        User2.userName,
        [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
        Circuit(),
    )

    User1.contacts.addContact(User2Public)
    User2.contacts.addContact(User1Public)
    Messages = []

    threading.Thread(target=messagesListener, args=(RECEIVED_MESSAGES,)).start()
    threading.Thread(target=readPipe, args=(RECEIVED_MESSAGES, Messages)).start()

    atPort = DEFAULT_PORT
    while isUsed(atPort):
        atPort = random.randint(8000, 9000)
    t = threading.Thread(
        target=subprocess.call, args=(startServer(atPort),), kwargs={"shell": True}
    ).start()

    # webbrowser.open(openBrowser(atPort), new=2)

    MSG = User1.createMessageToSent("Hello World!", User2.userName)
    netMSG = MSG.toNetworkMessage().asJSON().encode()

    asPacket = Packet(netMSG, User1.IP, User2.IP)
    asPacket.toNetworkLayer()

    while True:
        if len(Messages) > 0:
            break

    MSG_ = cleanData(Messages[0]["Data"].decode())
    MSG_ = User2.createMessageToReceive(MSG_)

    return MSG_.content.decode() == "Hello World!"


if __name__ == "__main__":
    if testSendReceiveMessage():
        print("Test Passed")
    else:
        print("Test Failed")
