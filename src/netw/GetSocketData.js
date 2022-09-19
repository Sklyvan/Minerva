const PORT = 8080;

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
        var dictData = {};
        // Loop through the array
        for (var i = 0; i < asArray.length; i++) 
        {
            // Split the array by colon
            var splitArray = asArray[i].split(':');
            // Add the split array to the new array
            dictData[splitArray[0]] = splitArray[1];
        }

        // Transform the dictData['timeCreated'] to a int
        var timeCreated = parseInt(dictData['timeCreated']);
        dictData['timeCreated'] = timeCreated;

        console.log(dictData);
    });
});
server.listen(PORT);
