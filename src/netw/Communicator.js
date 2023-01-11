const FileSystem = require('fs'); // We need to access the file system to read the SocketsInformation.xml file.
const WebSocket = require("ws");

const workingPath = __dirname;
const socketsFile = workingPath + '/SocketsInformation.xml';

function openXMLFile(filePath, withEncoding='utf8')
{
    return FileSystem.readFileSync(filePath, withEncoding);
}

function readHost(fromXML)
{
    return fromXML.match(/<host>(.*)<\/host>/)[1];
}

function readPort(fromXML)
{
    return fromXML.match(/<port>(.*)<\/port>/)[1];
}

function socketInformation(fromFile)
{
    const xmlFile = openXMLFile(fromFile);
    return [readHost(xmlFile), readPort(xmlFile)];
}

class Communicator
{
    constructor(atHost, onPort, aliveMessageInterval=0)
    {
        this.connectionInfo = {host: atHost, port: onPort};
        this.webSocketServer = new WebSocket.Server(this.connectionInfo);
        this.aliveMessageInterval = aliveMessageInterval;
        this.isConnectionOpen = false;

        this.webSocketServer.on('error', function (error)
        {
            if (error.code === 'EADDRINUSE')
            {
                console.warn('The WebSocket was already open, not reopening.');
            }
            else
            {
                console.error(error);
            }
        });

        this.webSocketServer.on('connection', (ws) =>
        {
            this.isConnectionOpen = true;
            ws.on('message', (message) =>
            {
                let msgType = this.identifyPacketType(message.toString());
                if ((msgType === 'MessageResponse') || (msgType === 'MessageRequest'))
                {
                    this.webSocketServer.clients.forEach((client) =>
                    {
                        if (client.readyState === 1)
                        {
                            client.send(message.toString());
                        }
                    });
                }
                else if (msgType === 'CloseRequest')
                {
                    this.closeServer();
                }
            });
        });

        // Periodically, send an alive message to the Front-End and Back-End.
        if (this.aliveMessageInterval > 0)
        {
            setInterval(() => {if (this.isConnectionOpen) this.sendAliveMessage()}, this.aliveMessageInterval);
        }
    }

    isJSONParseable(str)
    {
        try
        {
            JSON.parse(str);
        }
        catch (e)
        {
            return false;
        }
        return true;
    }

    identifyPacketType(message)
    {
        if (this.isJSONParseable(message)) // Some packets are not parseable.
        {
            let msg = JSON.parse(message);
            if (msg.toSend)
                return 'MessageRequest';
            else if (msg.toReceive)
                return 'MessageResponse';
            else if (msg.alive)
                return 'AliveMessage';
            else if (msg.close)
                return 'CloseRequest';
        }
        else
        {
            if (message.includes("'toSend': 'true'"))
                return 'MessageRequest'; // This is a message sent by our user, should be sent to JS Front-End.
            else if (message.includes("'toReceive': 'true'"))
                return 'MessageResponse'; // This is a received message, should be sent to Python Back-End.
            else if (message.includes("'alive': 'true'"))
                return 'AliveMessage';
            else if (message.includes("'close': 'true'"))
                return 'CloseRequest'; // Close the WebSocket.
        }
        return undefined;
    }

    sendAliveMessage()
    {
        this.webSocketServer.clients.forEach((client) =>
        {
            const tt = new Date().getTime();
            if (client.readyState === 1) // UNIX Timestamp
                client.send(JSON.stringify(
                    {toSend: false, toReceive: false, alive: true, timeStamp: tt}));
        });
    }

    closeServer()
    {
        this.webSocketServer.close();
        this.isConnectionOpen = false;
        process.exit(0);
    }
}

[HOST, PORT] = socketInformation(socketsFile);
new Communicator(HOST, PORT); // Once the communicator is created, it starts automatically.