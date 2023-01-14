function cleanData(event)
{
    return new Promise((resolve, reject) =>
    {
        try
        {
            let asString = event.toString();
            let asJSON = JSON.parse(asString);
            resolve(asJSON);
        }
        catch (err)
        {
            reject(err);
        }
    });
}


function openXMLFile(filePath)
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
