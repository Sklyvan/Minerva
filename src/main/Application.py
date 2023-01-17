from src.main.MainSystem import *
import argparse


def readArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--load",
        help="Load an existent user. The argument must be the username of the user.",
        type=str,
    )
    parser.add_argument(
        "--new",
        help="Create a new user. The argument must be the username of the new user.",
        type=str,
    )

    parser.add_argument(
        "--password",
        help="The password of the user. If not specified, the user does not have a password.",
        type=str,
    )

    parser.add_argument(
        "--sender",
        help="The username of the sender.",
        type=str,
    )
    parser.add_argument(
        "--receiver",
        help="The username of the receiver when we send a message.",
        type=str,
    )
    parser.add_argument(
        "--message",
        help="The message to send.",
        type=str,
    )
    parser.add_argument(
        "--nodeid",
        help="The id of the node to send the message to.",
        type=str,
    )
    args = parser.parse_args()
    return args


def anyArgument(args):
    return (
        args.load
        or args.new
        or args.sender
        or args.receiver
        or args.message
        or args.nodeid
    )


def waitForMessages():
    time.sleep(3)
    try:
        for msg in receiveMessages(myUser):
            msgContent = msg.content
            fromUser = msg.sender
            print(f"Received message from {fromUser.userName}: {msgContent}")
    except KeyboardInterrupt:
        browserEmulator.stopDriver()
        sys.exit(0)


if __name__ == "__main__":
    sysArgs = readArgs()
    isLoad, isCreate = sysArgs.load, sysArgs.new
    userKey = sysArgs.password

    if anyArgument(sysArgs):
        if isLoad or isCreate:
            if isLoad:
                userName = sysArgs.load
                myUser, userPath, browserEmulator = startSystem(
                    userName, userKey, loadUser=True
                )
                waitForMessages()
            if isCreate:
                userName = sysArgs.new
                myUser, userPath, browserEmulator = startSystem(
                    userName, userKey, createUser=True
                )
                waitForMessages()
        else:
            """
            In this case, we are not starting the system, but sending a message.
            We need to extract the username, then initialize the user and send the message.
            """
            sender = sysArgs.sender
            receiver = sysArgs.receiver
            message = sysArgs.message
            myUser, _ = initializeUser(sender, userKey, loadUser=True)
            sendMessage(message, myUser, myUser.getContact(receiver), sysArgs.nodeid)
    else:
        sys.exit(1)
