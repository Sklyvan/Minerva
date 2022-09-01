CREATE TABLE IF NOT EXISTS 'Metadata'
(
    CreationDate DATETIME NOT NULL,
    LastUpdate DATETIME NOT NULL,
    NumberMessages INTEGER NOT NULL,
    PRIMARY KEY (CreationDate)
);

CREATE TABLE IF NOT EXISTS 'Messages'
(
    ID INTEGER NOT NULL,
    FromUser INTEGER NOT NULL,
    ToUser INTEGER NOT NULL,
    SentDate DATETIME NOT NULL,
    ReceivedDate DATETIME,
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
    UPDATE Metadata SET LastUpdate = datetime('now', 'localtime'), NumberMessages = NumberMessages + 1;
END;