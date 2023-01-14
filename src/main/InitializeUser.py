from src.main.User import *
import sys


def createUserID():
    return random.randint(0, 1000)


def createNetworkID():
    networkID = [
        os.urandom(4).hex(),
        os.urandom(2).hex(),
        os.urandom(2).hex(),
        os.urandom(2).hex(),
        os.urandom(6).hex(),
    ]
    networkID = "-".join(networkID)
    return networkID


def initializeUser(sysArgs: list) -> (User, str):
    """
    This file is called with the arguments -l <filename> or -n <username>.
    If the argument -l is used, the user will be loaded from the file <filename>.
    If the argument -n is used, a new user will be created with the username <username>.
    :param sysArgs: This comes from the sys.argv list, which contains the arguments passed to the script.
    :return: An instance of the User class, and the file path of the user file.
    """
    loadUser = False
    if len(sysArgs) == 3:
        if sysArgs[1] == "-l":  # We want to load a user from a JSON file.
            loadUser = True
            fileName = sysArgs[2]
            filePath = os.path.join(USER_PATH, fileName)
            if not os.path.exists(filePath):
                print("File does not exist")
                sys.exit(1)
            if not filePath.endswith(USERFILE_EXTENSION):
                print(f"File must be a {USERFILE_EXTENSION.upper()} file")
                sys.exit(1)
        elif sysArgs[1] == "-n":  # We want to create a new user.
            userName = sysArgs[2]
        else:
            print("Invalid command line arguments")
            sys.exit(1)
    else:
        print("Invalid command line arguments")
        sys.exit(1)

    if loadUser:
        myUser = User(None, None, [None, None], None)
        myUser.importUser(filePath)
    else:
        userID, networkID = (
            createUserID(),
            createNetworkID(),
        )  # TODO: This creations of the ID are temporary.
        myUser = createUser(userName, networkID, userID)
        exportName = USERFILE_NAME + userName + "." + USERFILE_EXTENSION
        myUser.exportUser(os.path.join(USER_PATH, exportName))

    return myUser, filePath
