const { ipcRenderer, contextBridge } = require('electron');

// forward logs received from exe to web console
ipcRenderer.on('log', (event, message) => console.log(message));

contextBridge.exposeInMainWorld('electron', {

    // allow fetching app version in electron browser window
    appVersion: async function() {
        return await ipcRenderer.invoke('app-version');
    },

    // add support for using "prompt" in electron browser window
    prompt: async function(message) {
        return await ipcRenderer.invoke('prompt', message);
    },

});
