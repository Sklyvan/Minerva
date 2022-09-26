const myPeer = new Peer('d8cd7bae-0b80-4a71-a7e5-22f728016311'); // TODO: Right now, everyone can impersonate anyone else. I have to implement the RSA signature verification.
var p2pConnection = null;
var isReady = false;

var xml = new XMLHttpRequest();
xml.open('GET', 'SocketsInformation.xml', false);
xml.send();
var HOST = xml.responseXML.getElementsByTagName('hostJStoHTML')[0].childNodes[0].nodeValue;
var PORT = xml.responseXML.getElementsByTagName('portJStoHTML')[0].childNodes[0].nodeValue;

function socketOpenReadClose()
{
    var ws = new WebSocket('ws://' + HOST + ':' + PORT);
    let isOpened = false;
    ws.onopen = function (event)
    {
        isOpened = true;
        ws.onmessage = function (event)
        {
            let data = JSON.parse(event.data);
            connectAndSend(data['toIP'], data['Data']);
        };
    };
    if (!isOpened)
    {
        setTimeout(() => socketOpenReadClose(), 750);
    }
}

myPeer.on('open', peerID =>
{
    console.log('ID: ' + peerID);
    isReady = true;
});

myPeer.on('connection', conn =>
{
    conn.on('data', data =>
    {
        console.log('Received: ' + data);
    });
});

function connectAndSend(peerID, data)
{
    if (!isReady)
    {
        setTimeout(() => connectAndSend(peerID, data), 500);
    }
    p2pConnection = myPeer.connect(peerID);
    p2pConnection.on('open', () =>
    {
        p2pConnection.send(data);
    });
}

setInterval(socketOpenReadClose, 1000);
