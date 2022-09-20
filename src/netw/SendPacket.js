var wrtc = require('wrtc');

let localConnection = null;   // RTCPeerConnection for our "local" connection
let remoteConnection = null;  // RTCPeerConnection for the "remote"

let sendChannel = null;       // RTCDataChannel for the local (sender)
let receiveChannel = null;    // RTCDataChannel for the remote (receiver)

function connectPeers()
{
    localConnection = new wrtc.RTCPeerConnection();

    sendChannel = localConnection.createDataChannel("sendChannel");

    remoteConnection = new wrtc.RTCPeerConnection();
    remoteConnection.ondatachannel = receiveChannelCallback;

    localConnection.onicecandidate = (e) => !e.candidate
        || remoteConnection.addIceCandidate(e.candidate)
            .catch(handleAddCandidateError);

    remoteConnection.onicecandidate = (e) => !e.candidate
        || localConnection.addIceCandidate(e.candidate)
            .catch(handleAddCandidateError);

    localConnection.createOffer()
        .then(offer => localConnection.setLocalDescription(offer))
        .then(() => remoteConnection.setRemoteDescription(localConnection.localDescription))
        .then(() => remoteConnection.createAnswer())
        .then(answer => remoteConnection.setLocalDescription(answer))
        .then(() => localConnection.setRemoteDescription(remoteConnection.localDescription))
        .catch(handleCreateDescriptionError);
}

function handleCreateDescriptionError(error)
{
    console.log(`Unable to create an offer: ${error.toString()}`);
}

function handleAddCandidateError()
{
    console.log("Oh noes! addICECandidate failed!");
}

function receiveChannelCallback(event)
{
    receiveChannel = event.channel;
    receiveChannel.onmessage = receiveMessage;
}

function sendMessage(message)
{
    sendChannel.send(message);
}

function receiveMessage(event)
{
    console.log("Received Message: " + event.data);
}

connectPeers();
setTimeout(function() { sendMessage("Hello!");},100);
