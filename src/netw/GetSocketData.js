// Start listening on the port 8080 and return the data

var net = require('net');
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
        var newArray = {};
        // Loop through the array
        for (var i = 0; i < asArray.length; i++) {
            // Split the array by colon
            var splitArray = asArray[i].split(':');
            // Add the split array to the new array
            newArray[splitArray[0]] = splitArray[1];
        }

        // Transform the newArray['timeCreated'] to a int
        var timeCreated = parseInt(newArray['timeCreated']);
        newArray['timeCreated'] = timeCreated;

        console.log(newArray);
    });
});
server.listen(8080);
