const { ipcRenderer, contextBridge } = require('electron');

// forward logs received from exe to web console
ipcRenderer.on('log', (event, message) => console.log(message));

// add support for using "prompt" in electron browser window
contextBridge.exposeInMainWorld('electron', {
    prompt: async function(message) {
        return await ipcRenderer.invoke('prompt', message);
    },
});
