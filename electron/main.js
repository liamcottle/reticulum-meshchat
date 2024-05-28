const { app, BrowserWindow, ipcMain, systemPreferences } = require('electron');
const electronPrompt = require('electron-prompt');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('node:path');

// remember main window
var mainWindow = null;

// remember child process for exe so we can kill it when app exits
var exeChildProcess = null;

// add support for showing a prompt window via ipc
ipcMain.handle('prompt', async(event, message) => {
    return await electronPrompt({
        title: message,
        label: '',
        value: '',
        type: 'input',
        inputAttrs: {
            type: 'text',
        },
    });
});

function log(message) {

    // make sure main window exists
    if(!mainWindow){
        return;
    }

    // make sure window is not destroyed
    if(mainWindow.isDestroyed()){
        return;
    }

    // log to electron console
    console.log(message);

    // log to web console
    mainWindow.webContents.send('log', message);

}

app.whenReady().then(async () => {

    // create browser window
    mainWindow = new BrowserWindow({
        width: 1500,
        height: 800,
        webPreferences: {
            // used to inject logging over ipc
            preload: path.join(__dirname, 'preload.js'),
        },
    });

    // navigate to loading page
    await mainWindow.loadFile(path.join(__dirname, 'loading.html'));

    // find path to python/cxfreeze reticulum webchat executable
    var exe = path.join(__dirname, 'build/exe/ReticulumWebChat');

    // if dist exe doesn't exist, check local build
    if(!fs.existsSync(exe)){
        exe = path.join(__dirname, '..', 'build/exe/ReticulumWebChat');
    }

    // ask mac users for microphone access for audio calls to work
    if(process.platform === "darwin"){
        await systemPreferences.askForMediaAccess('microphone');
    }

    try {

        // spawn executable
        exeChildProcess = await spawn(exe, [
            '--headless', // reticulum webchat usually launches default web browser, we don't want this when using electron
            '--port', '9337', // FIXME: let system pick a random unused port?
            '--storage-dir', path.join(app.getPath('home'), '.reticulum-webchat'), // ~/.reticulum-webchat
        ]);

        // log stdout
        exeChildProcess.stdout.setEncoding('utf8');
        exeChildProcess.stdout.on('data', function(data) {
            log(data.toString());
        });

        // log stderr
        exeChildProcess.stderr.setEncoding('utf8');
        exeChildProcess.stderr.on('data', function(data) {
            log(data.toString());
        });

        // log errors
        exeChildProcess.on('error', function(error) {
            log(error);
        });

        // quit electron app if exe dies
        exeChildProcess.on('exit', function(code) {
            quit();
        });

    } catch(e) {
        log(e);
    }

});

function quit() {

    // kill python process
    if(exeChildProcess){
        exeChildProcess.kill();
    }

    // quit electron app
    app.quit();

}

// quit electron if all windows are closed
app.on('window-all-closed', () => {
    quit();
});

// make sure child process is killed if app is quiting
app.on('quit', () => {
    quit();
});
