var net = require('net');
var fs = require('fs');

var xml = fs.readFileSync('SocketsInformation.xml', 'utf8');
var HOST = xml.match(/<host>(.*)<\/host>/)[1];
var PORT = xml.match(/<port>(.*)<\/port>/)[1];

function readSocketData(port) {
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
        });
    });
    server.listen(port);
}

readSocketData(PORT);