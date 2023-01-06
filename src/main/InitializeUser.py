from src.main.User import *
import sys

"""
This file is called with the arguments -l <filename> or -n <username>.
If the argument -l is used, the user will be loaded from the file <filename>.
If the argument -n is used, a new user will be created with the username <username>.
"""


def initializeUser(sysArgs: list) -> User:
    loadUser = False
    if len(sysArgs) == 3:
        if sysArgs[1] == "-l":
            loadUser = True
            fileName = sysArgs[2]
            if not os.path.exists(fileName):
                print("File does not exist")
                sys.exit(1)
            if not fileName.endswith(USERFILE_EXTENSION):
                print(f"File must be a {USERFILE_EXTENSION.upper()} file")
                sys.exit(1)
        elif sysArgs[1] == "-n":
            userName = sysArgs[2]
        else:
            print("Invalid command line arguments")
            sys.exit(1)
    else:
        print("Invalid command line arguments")
        sys.exit(1)

    if loadUser:
        myUser = User(None, None, [None, None], None)
        myUser.importUser(fileName)
    else:
        networkID = [
            os.urandom(4).hex(),
            os.urandom(2).hex(),
            os.urandom(2).hex(),
            os.urandom(2).hex(),
            os.urandom(6).hex(),
        ]
        networkID = "-".join(networkID)

        userID = random.randint(0, 1000)
        # TODO: This creation of the userID and networkID is temporary.

        myUser = createUser(userName, networkID, userID)
        exportName = USERFILE_NAME + userName + "." + USERFILE_EXTENSION
        myUser.exportUser(os.path.join(USER_PATH, exportName))

    return myUser
