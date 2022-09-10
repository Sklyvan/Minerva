CREATE TABLE IF NOT EXISTS 'Metadata'
(
    CreationDate INTEGER NOT NULL, -- Unix timestamp
    LastUpdate INTEGER NOT NULL, -- Unix timestamp
    NumberMessages INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (CreationDate)
);

CREATE TABLE IF NOT EXISTS 'Messages'
(
    ID INTEGER NOT NULL,
    FromUser INTEGER NOT NULL,
    ToUser INTEGER NOT NULL,
    SentDate INTEGER NOT NULL,
    ReceivedDate INTEGER DEFAULT NULL,
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

CREATE TRIGGER IF NOT EXISTS addMessage
AFTER INSERT ON 'Messages'
BEGIN
    -- Set the LastUpdate to the current date and add one to the number of messages.
    UPDATE 'Metadata' SET LastUpdate = strftime('%s', datetime('now')),
                          NumberMessages = NumberMessages + 1;
END;

CREATE TRIGGER IF NOT EXISTS deleteMessage
AFTER DELETE ON 'Messages'
BEGIN
    -- Set the LastUpdate to the current date and subtract one from the number of messages.
    UPDATE 'Metadata' SET LastUpdate = strftime('%s', datetime('now')),
                          NumberMessages = NumberMessages - 1;
END;