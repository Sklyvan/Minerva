function cleanData(event)
{
    let asString = event.toString();
    // asString = asString.replace(/{/g, '');
    // asString = asString.replace(/}/g, '');
    asString = asString.replace(/"/g, '');
    asString = asString.replace(/b'/g, '"');
    asString = asString.replace(/'/g, '"');
    asString = asString.replace(/ /g, '');
    return JSON.parse(asString.toString());
}

function openXMLFile(filePath, withEncoding='utf8')
{
    let xmlFileRequest = new XMLHttpRequest();
    xmlFileRequest.open("GET", filePath, false);
    xmlFileRequest.send();
    return xmlFileRequest.responseText;
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

function createSocket(socketHost, socketPort, retryConnection=1000)
{
    let mySocket = undefined;
    function loopCreateSocket()
    {
        mySocket = new WebSocket("ws://" + socketHost + ":" + socketPort);
        mySocket.onerror = function(event)
        {
            console.warn("Error connecting to the WebSocket Server. " +
                "Trying again in " + retryConnection + " miliseconds.");
            setTimeout(loopCreateSocket, retryConnection);
        };
    }
    loopCreateSocket();
    return mySocket
}
