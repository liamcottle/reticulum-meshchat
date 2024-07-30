const { ipcRenderer, contextBridge } = require('electron');

// forward logs received from exe to web console
ipcRenderer.on('log', (event, message) => console.log(message));

contextBridge.exposeInMainWorld('electron', {

    // allow fetching app version in electron browser window
    appVersion: async function() {
        return await ipcRenderer.invoke('app-version');
    },

    // show an alert dialog in electron browser window, this fixes a bug where alert breaks input fields on windows
    alert: async function(message) {
        return await ipcRenderer.invoke('alert', message);
    },

    // add support for using "prompt" in electron browser window
    prompt: async function(message) {
        return await ipcRenderer.invoke('prompt', message);
    },

    // allow relaunching app in electron browser window
    relaunch: async function() {
        return await ipcRenderer.invoke('relaunch');
    },

    // allow showing a file path in os file manager
    showPathInFolder: async function(path) {
        return await ipcRenderer.invoke('showPathInFolder', path);
    },

});
