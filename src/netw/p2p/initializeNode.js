const [HOST, PORT] = socketInformation('../SocketsInformation.xml');

async function obtainNodeID()
{
    // The function waits until the nodeID is obtained from the INST file.
    return new Promise((resolve, reject) =>
    {
        let interval = setInterval(() =>
        {
            if (document.getElementById('nodeID').value !== "")
            {
                clearInterval(interval);
                resolve(document.getElementById('nodeID').value);
            }
        }, 100);
    });
}
const NODEID = await obtainNodeID();

const SOCKET = createSocket(HOST, PORT);
const NODE = new p2pNode(NODEID, SOCKET);
window.NODE = NODE;

SOCKET.onopen = () =>
{
    NODE.start(true);
    NODE.node.on('open', function (id) // Do not use the NODE until is ready.
    {
        SOCKET.onmessage = function(event)
        {
            /*
            When the Front-End Socket receives a message, it is because the Back-End sent a message.
            This message is a pyPacket, so we are going to send it to the p2pNode.
            The p2pNode is going to transform this packet into an InternetPacket and send it to the other node.
             */
            cleanData(event.data).then((pyPacket) =>
            {
                if (pyPacket.toSend)
                {
                    NODE.send(pyPacket);
                    // let confirmationPacket = {toSend: false, toReceive: true, confirmation: true, ID: pyPacket.ID};
                    // SOCKET.send(JSON.stringify(confirmationPacket));
                }
            });
        }
    });
}

function closeWebSocketServer()
{
    SOCKET.send(JSON.stringify({'close': true}));
    SOCKET.close();
}
