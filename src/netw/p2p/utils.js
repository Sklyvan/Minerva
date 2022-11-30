function cleanData(event)
{
    let asString = event.data;
    asString = asString.replace(/{/g, '');
    asString = asString.replace(/}/g, '');
    asString = asString.replace(/"/g, '');
    asString = asString.replace(/b'/g, '');
    asString = asString.replace(/'/g, '');
    asString = asString.replace(/ /g, '');
    const asArray = asString.split(',');
    // Create a new array
    let dictData = {};
    // Loop through the array
    for (let i = 0; i < asArray.length; i++)
    {
        // Split the array by colon
        let splitArray = asArray[i].split(':');
        // Add the split array to the new array
        dictData[splitArray[0]] = splitArray[1];
    }
    return dictData;
}

function readXML(fileName)
{
    let xml = new XMLHttpRequest();
    xml.open("GET", fileName, false);
    xml.send();
    let xmlDoc = xml.responseXML;

    let host = xmlDoc.getElementsByTagName("host")[0].childNodes[0].nodeValue;
    let port = xmlDoc.getElementsByTagName("port")[0].childNodes[0].nodeValue;
    return [host, port];
}
