class p2pNode
{
    constructor(nodeKey)
    {
        this.nodeKey = nodeKey;
        this.node = new Peer(nodeKey);
        this.node.on('connection', (conn) =>
        {
            conn.on('data', (data) =>
            {
                console.log(data);
                socket.send(data);
            });
        });
    }
    send(data, peerKey)
    {
        let conn = this.node.connect(peerKey);
        conn.on('open', () =>
        {
            conn.send(data);
        });
    }
}

let nodeID = document.getElementById('nodeID').value;
const myNode = new p2pNode(nodeID);
const socketInfo = readXML('../SocketsInformation.xml'); // This returns [Host, Port]
let socket = new WebSocket("ws://" + socketInfo[0] + ":" + socketInfo[1]);

socket.onmessage = function(event)
{
    const data = cleanData(event);
    let msgContent = data['Data'];
    let fromIP = data['fromIP']; let toIP = data['toIP'];
    if (fromIP == myNode.nodeKey)
        myNode.send(msgContent, toIP);
};
