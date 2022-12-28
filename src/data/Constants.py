import os

TABLE_CREATION = "TablesCreation.sql"
TABLE_CREATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sqls", TABLE_CREATION
)

INSERT_MESSAGE = "InsertMessage.sql"
INSERT_MESSAGE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sqls", INSERT_MESSAGE
)

DELETE_MESSAGE = "DeleteMessage.sql"
DELETE_MESSAGE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sqls", DELETE_MESSAGE
)

GET_MESSAGE = "GetMessage.sql"
GET_MESSAGE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sqls", GET_MESSAGE
)

INITIALIZE_METADATA = "InitializeMetadata.sql"
INITIALIZE_METADATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sqls", INITIALIZE_METADATA
)

DATABASE_NAME = "Messages.db"
