from src.main.User import *

def initializeUser(sysArgs: list) -> User:
    loadUser = False
    if len(sysArgs) == 3:
        if sysArgs[1] == '-l':
            loadUser = True
            fileName = sysArgs[2]
            if not os.path.exists(fileName):
                print("File does not exist")
                sys.exit(1)
            if not fileName.endswith('.json'):
                print("File must be a json file")
                sys.exit(1)
        elif sysArgs[1] == '-n':
            userName = sysArgs[2]
        else:
            print("Invalid command line arguments")
            sys.exit(1)
    elif len(sysArgs) != 1:
        print("Invalid command line arguments")
        sys.exit(1)

    if loadUser:
        myUser = User(None, None, [None, None], None)
        myUser.importUser(fileName)
    else:
        userID = int(os.urandom(16).hex(), 16)
        networkID = [os.urandom(4).hex(),
                     os.urandom(2).hex(),
                     os.urandom(2).hex(),
                     os.urandom(2).hex(),
                     os.urandom(6).hex()]
        networkID = '-'.join(networkID)
        # TODO: This creation of the userID and networkID is temporary.

        t0 = int(time())
        myUser = User(userID, userName,
                      [RSAKeys(fileName=f'{userName}_EncKeys_{t0}'), RSAKeys(fileName=f'{userName}_SigKeys_{t0}')],
                      networkID, ForwardingTable(), Queue(), Contacts(), MessagesDB())
        myUser.exportUser(f'User_{userName}.json')
        
    return myUser
