const myPeer = new Peer('');
var isReady = false;
var p2pConnection = null;

myPeer1.on('open', peerID =>
{
    console.log('ID: ' + peerID);
    isReady = true;
});

myPeer1.on('connection', conn =>
{
    conn.on('data', data =>
    {
        console.log('Received: ' + data);
    });
});

function connectToPeer(peerID)
{
    if (!isReady)
    {
        setTimeout(() => connectToPeer(peerID), 500);
    }
    p2pConnection = myPeer.connect(peerID);
    p2pConnection.on('open', () =>
    {
        p2pConnection.send("Hello!");
    });
}