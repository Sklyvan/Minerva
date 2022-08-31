CREATE TABLE IF NOT EXISTS 'Metadata'
(
    CreationDate DATE NOT NULL,
    LastUpdate DATE NOT NULL,
    NumberMessages INTEGER NOT NULL,
    PRIMARY KEY (CreationDate)
);

CREATE TABLE IF NOT EXISTS 'Messages'
(
    ID INTEGER NOT NULL,
    FromUser INTEGER NOT NULL,
    ToUser INTEGER NOT NULL,
    SentDate DATE NOT NULL,
    ReceivedDate DATE NOT NULL,
    Content TEXT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (FromUser) REFERENCES Contacts(ID),
    FOREIGN KEY (ToUser) REFERENCES Contacts(ID)
);

CREATE TABLE IF NOT EXISTS 'Contacts'
(
    ID INTEGER NOT NULL,
    UserName TEXT NOT NULL,
    RSAPublicKey TEXT NOT NULL,
    CircuitID INTEGER NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TRIGGER IF NOT EXISTS UpdateMetadata
AFTER INSERT ON Messages
BEGIN
    -- Set the LastUpdate to the current date and add one to the number of messages.
    UPDATE Metadata SET LastUpdate = datetime('now'), NumberMessages = NumberMessages + 1;
END;