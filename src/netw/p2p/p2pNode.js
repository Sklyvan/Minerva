class p2pNode
{
    constructor(nodeID, socket)
    {
        this.nodeID = nodeID;
        this.node = new Peer(nodeID);
        this.socket = socket; // Received messages are sent to the WebSocket Server, then are sent to the Back-End.
    }

    start(logData=false)
    {
        this.node.on('connection', (conn) =>
        {
            conn.on('data', (internetPacket) =>
            {
                if (logData) console.log("Received: " + internetPacket);
                /*
                This data comes in the form of a InternetPacket, this date is sent by another node.
                internetPacket = { fromNode: ..., toNode: ..., data: ... }
                We are going to create a new for packet Python Back-End
                pyPacket = {toSend = False, toReceive = True, data = internetPacket}
                 */
                let pyPacket = {toSend: false, toReceive: true, data: internetPacket};
                this.socket.send(JSON.stringify(pyPacket));
            });
        });
    }

    send(pyPacket)
    {
        /*
        This data comes in the form of a pyPacket
        pyPacket = {toSend = True, toReceive = False, data = internetPacket}
        In this case, we want to send the data to another node, so we are going to create a new InternetPacket
         */

        let internetPacket = pyPacket.data;
        let conn = this.node.connect(internetPacket.toNode);
        conn.on('open', () =>
        {
            conn.send(internetPacket);
            console.log("Sent: " + internetPacket);
        });
    }

}
