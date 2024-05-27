const { ipcRenderer } = require('electron');

// forward logs received from exe to web console
ipcRenderer.on('log', (event, message) => console.log(message));
