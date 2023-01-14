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


def initializeUser(
    userName: str, userKey: str = None, loadUser: bool = False, newUser: bool = False
) -> (User, str):
    """
    Initialize a user, depending on the case, we load a JSON file or we create a user from scratch.
    After creating the user, we save it to a JSON file.
    :param userName: Username of the user, from the name, we can get the file path.
    :param userKey: Password of the user, if not specified, the user does not have a password.
    :param loadUser: Boolean that indicates if we are loading a user.
    :param newUser: Boolean that indicates if we are creating a new user.
    :return: The user and the file path of the user.
    """
    fileName = USERFILE_NAME + userName + "." + USERFILE_EXTENSION
    publicUserFileName = PUBLICUSERFILE_NAME + userName + "." + PUBLICUSERFILE_EXTENSION

    filePath = os.path.join(USER_PATH, fileName)
    publicUserFilePath = os.path.join(USER_PATH, publicUserFileName)

    if loadUser and newUser:
        raise Exception("Cannot load and create a new user at the same time.")
    if not loadUser and not newUser:
        raise Exception("Must load or create a new user.")

    if loadUser:
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"The file {filePath} does not exist.")
        if not filePath.endswith(USERFILE_EXTENSION):
            raise Exception(f"File must be a {USERFILE_EXTENSION.upper()} file")
        myUser = User(None, None, [None, None], None)
        if not userKey:
            myUser.importUser(filePath)
        else:
            myUser.importEncryptedUser(filePath, userKey)

        return myUser, filePath

    if newUser:
        userID, networkID = (
            createUserID(),
            createNetworkID(),
        )  # TODO: This creations of the ID are temporary.
        myUser = createUser(userName, networkID, userID)
        if not userKey:
            myUser.exportUser(filePath)
        else:
            myUser.exportEncryptedUser(filePath, userKey)

        myUser.toPublicUser().exportUser(publicUserFilePath)

        return myUser, filePath
