#target photoshop

function importImagesAsLayers(folderPath) {
    var folder = new Folder(folderPath);
    if (!folder.exists) {
        alert('Folder does not exist');
        return;
    }

    var files = folder.getFiles(/\.(jpg|jpeg|tif|tiff|png|psd|bmp)$/i);
    if (files.length === 0) {
        alert('No valid images found in the folder');
        return;
    }
    
    // Open the first file to set the document size and rename it
    app.open(files[0]);
    var doc = app.activeDocument;
    doc.name = "Concept_v001.psd";

    // Process the first layer immediately after it is loaded
    processLayer(doc, doc.activeLayer);

    // Process each subsequent file
    for (var i = 1; i < files.length; i++) {
        app.open(files[i]);
        var loadedDoc = app.activeDocument;
        var layer = loadedDoc.artLayers[0].duplicate(doc, ElementPlacement.PLACEATEND);
        app.activeDocument = doc; // Ensure the target document is active after closing the loaded document
        layer.name = loadedDoc.name.match(/([^\/\\]+)\.\w+$/)[1]; // Extract the file name without extension
        loadedDoc.close(SaveOptions.DONOTSAVECHANGES);

        // Process each layer immediately after it is added
        processLayer(doc, layer);
    }

    return doc;
}

function processLayer(doc, layer) {
    var layerName = String(layer.name).toLowerCase(); // Ensure layerName is a string

    doc.activeLayer = layer; // Set the layer as active to work with it
    layer.visible = true; // Ensure the layer is visible before copying

    if (layerName.indexOf('normal') !== -1 || layerName.indexOf('position') !== -1) {
        var channels = ['Red', 'Green', 'Blue'];
        for (var j = 0; j < channels.length; j++) {
            duplicateChannel(doc, layerName + ' ' + channels[j], channels[j]);
        }
        layer.remove();
    } else if (layerName.match(/(cryptomatte|fresnel|mist|occlusion|ao)/)) {
        duplicateChannel(doc, layerName, "Red");
        layer.remove();
    } else if (layerName.indexOf('image') === -1) {
        layer.visible = false;
    }
}

function duplicateChannel(doc, newName, channelName) {
    try {
        var channelToDuplicate = doc.channels.getByName(channelName); // Get the channel by name
        var newChannel = doc.channels.add(); // Add a new channel
        newChannel.name = newName; // Rename the new channel

        // Copy the content from the specified channel to the new channel
        doc.activeChannels = [channelToDuplicate];
        doc.selection.selectAll();
        doc.selection.copy();
        doc.activeChannels = [newChannel];
        doc.paste();
        doc.selection.deselect();

    } catch (e) {
        alert("Failed to duplicate and rename channel: " + e.toString());
    }
}

function main() {
    var folderPath = Folder.selectDialog("Select the folder with images");
    if (folderPath) {
        var doc = importImagesAsLayers(folderPath);
        alert('Process completed successfully!');
    }
}

main();
