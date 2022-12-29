import os

emojiTick, emojiCross = "\u2705", "\u274C"

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

DB_PATH = os.path.dirname(FILE_DIR) + "/data/"
KEYS_PATH = os.path.dirname(FILE_DIR) + "/keys/"

DB_NAME = "Messages.db"
ENC_KEYS_NAME = "EncKeys"
SIG_KEYS_NAME = "SigKeys"
