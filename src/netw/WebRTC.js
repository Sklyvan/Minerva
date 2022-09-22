var wrtc = require('wrtc');
var fs = require('fs');

// https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity

const stunServer = {iceServers: [{urls: "stun:stun.l.google.com:19302"}]};
const offerFile = "Offer.json"; const answerFile = "Answer.json";

let caller = null; let callerChannel = null;
let recipient = null; let recipientChannel = null;
callerChannel = null; recipientChannel = null;

function createCaller()
{
    caller = new wrtc.RTCPeerConnection(); // Create the WebRTC connection.
    caller.ondatachannel = receiveChannelCallback; // Set the function to run when a data channel is received.
    callerChannel = caller.createDataChannel("callerChannel"); // Create the data channel to send data.

    caller.createOffer() // Create the offer.
        .then(offer => caller.setLocalDescription(offer)) // Set the local description.
        .then(() => {return caller;}, (error) => {console.log(error);}); // Return the WebRTC connection.

    // Generate the ICE candidates.
    return new Promise((resolve, reject) =>
    {
        caller.onicecandidate = (event) =>
        {
            if (event.candidate) { resolve(event.candidate); }
        };
    });
}

function createRecipient(remoteDescription)
{
    recipient = new wrtc.RTCPeerConnection(); // Create the WebRTC connection.
    recipient.ondatachannel = receiveChannelCallback; // Set the function to run when a data channel is received.
    recipientChannel = recipient.createDataChannel("recipientChannel"); // Create the data channel to send data.

    recipient.setRemoteDescription(remoteDescription) // Set the remote description.
        .then(() => recipient.createAnswer()) // Create the answer.
        .then(answer => recipient.setLocalDescription(answer)) // Set the answer as local description.
        .catch(error => console.log(error)); // Log any errors.
    // At this point, the recipient is fully set up and ready to communicate with the caller.

    // Generate the ICE candidates.
    return new Promise((resolve, reject) =>
    {
        recipient.onicecandidate = (event) =>
        {
            if (event.candidate) { resolve(event.candidate); }
        };
    });
}

function receiveChannelCallback(event)
{
    recipientChannel = event.channel;
    recipientChannel.onmessage = receiveMessage;
}

function sendMessage(message)
{
    callerChannel.send(message);
}

function receiveMessage(event)
{
    console.log("Received Message: " + event.data);
}

createCaller()
    .then(() => fs.writeFileSync(offerFile, JSON.stringify(caller.localDescription))) // The caller creates the offer and writes it.
    .then(() => createRecipient(JSON.parse(fs.readFileSync(offerFile)))) // The recipient reads the offer and creates the answer.
    .then(() => fs.writeFileSync(answerFile, JSON.stringify(recipient.localDescription))) // The recipient writes the answer to a JSON file.
    .then(() => caller.setRemoteDescription(JSON.parse(fs.readFileSync(answerFile)))) // The caller reads the answer and sets it as the remote description.
    .then(console.log("Done!"))
    .catch((error) => console.log(error))

setTimeout(function() { sendMessage("Hello World!");},100);
