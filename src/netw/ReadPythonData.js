var net = require('net');
var fs = require('fs');
var crypto = require('crypto');
var WebSocket = require('ws');
var dataHistory = {}; // dataHistory[SHA-256(data)] = true;

var xml = fs.readFileSync('SocketsInformation.xml', 'utf8');
const listenPort = xml.match(/<portPyToJS>(.*)<\/portPyToJS>/)[1];
const senderPort = xml.match(/<portJStoHTML>(.*)<\/portJStoHTML>/)[1];
const wss = new WebSocket.Server({ port: senderPort })

function readPythonData(port)
{
    var server = net.createServer(function(socket) {
        socket.on('data', function(data) {
            var asString = data.toString();
            // From the string remove: {, }, ", b' and '
            asString = asString.replace(/{/g, '');
            asString = asString.replace(/}/g, '');
            asString = asString.replace(/"/g, '');
            asString = asString.replace(/b'/g, '');
            asString = asString.replace(/'/g, '');
            asString = asString.replace(/ /g, '');
            // Split the string by comma
            var asArray = asString.split(',');
            // Create a new array
            var dictData = {};
            // Loop through the array
            for (var i = 0; i < asArray.length; i++)
            {
                // Split the array by colon
                var splitArray = asArray[i].split(':');
                // Add the split array to the new array
                dictData[splitArray[0]] = splitArray[1];
            }
            // Return the dictData without exiting the function
            console.log(dictData);
            let dataHash = crypto
                .createHash('sha256')
                .update(JSON.stringify(dictData))
                .digest('hex');
            dataHistory[dataHash] = false; // The data has not been sent.
            sendSocketData(senderPort, JSON.stringify(dictData));
        });
    });
    server.listen(port);
}

function sendSocketData(onPort, data)
{
    wss.on('connection', function connection(ws)
    {
        let dataHash = crypto.createHash('sha256').update(data).digest('hex');
        if (!dataHistory[dataHash])
        {
            ws.send(data); // The SHA-256 is unique because the data contains the timestamp.
            dataHistory[dataHash] = true; // The data has been sent.
        }
    });
}

readPythonData(listenPort);