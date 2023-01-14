from src.main.MainSystem import *
import argparse


def readArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--load",
        help="Load an existent user. The argument must be the username of the user.",
        type=str,
    )
    parser.add_argument(
        "-n",
        "--new",
        help="Create a new user. The argument must be the username of the new user.",
        type=str,
    )

    parser.add_argument(
        "-p",
        "--password",
        help="The password of the user. If not specified, the user does not have a password.",
        type=str,
    )

    parser.add_argument(
        "-u",
        "--user",
        help="The username of our user when we send a message.",
        type=str,
    )
    parser.add_argument(
        "-r",
        "--receiver",
        help="The username of the receiver when we send a message.",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--message",
        help="The message to send.",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--id",
        help="The id of the node to send the message to.",
        type=str,
    )
    args = parser.parse_args()
    return args


def waitForMessages():
    time.sleep(3)
    try:
        receiveMessages(myUser)
    except KeyboardInterrupt:
        browserEmulator.stopDriver()
        sys.exit(0)


if __name__ == "__main__":
    sysArgs = readArgs()
    isLoad, isCreate = sysArgs.load, sysArgs.new
    userKey = sysArgs.password

    if isLoad or isCreate:
        if isLoad:
            username = sysArgs.load
            myUser, browserEmulator = startSystem(username, userKey, loadUser=True)
            waitForMessages()
        if isCreate:
            username = sysArgs.new
            myUser, browserEmulator = startSystem(username, userKey, createUser=True)
            waitForMessages()
    else:
        """
        In this case, we are not starting the system, but sending a message.
        We need to extract the username, then initialize the user and send the message.
        """
        username = sysArgs.user
        userKey = sysArgs.password
        receiver = sysArgs.receiver
        message = sysArgs.message
        nodeID = sysArgs.id
        myUser, browserEmulator = startSystem(username, userKey, loadUser=True)
        sendMessage(message, myUser, myUser.getContact(receiver), nodeID)
