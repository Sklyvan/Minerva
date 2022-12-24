const fs = require('fs');
const WebSocket = require("ws");
// Get the current path
const currentPath = __dirname;
const socketsFile = currentPath + '/SocketsInformation.xml';

const xml = fs.readFileSync(socketsFile, 'utf8');
const port = xml.match(/<port>(.*)<\/port>/)[1];
const webSocketServer = new WebSocket.Server({ port: port })

function messageType(message)
{
    // If the message contains is in the form {...}, then is a messageRequest, otherwise is a messageResponse
    if (message.match(/{(.*)}/))
        return 'messageRequest'; // Send this data to JS to be sent to the internet.
    else
        return 'messageResponse'; // Send this data to Python to be decrypted.
}

webSocketServer.on('connection', (ws) =>
{
    ws.on('message', (message) =>
    {
        let msgString = message.toString();
        if (messageType(msgString) === 'messageResponse') // Send to Python this data to be decrypted.
        {
            webSocketServer.clients.forEach((client) =>
            {
                if (client.readyState === 1)
                    client.send(msgString);
            });
        }
        else // Send to JS this data to be sent to the internet.
        {
            webSocketServer.clients.forEach((client) =>
            {
                if (client.readyState === 1)
                    client.send(msgString);
            });
        }
    });
});
