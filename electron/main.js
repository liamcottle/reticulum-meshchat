const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('node:path');

// remember main window
var mainWindow = null;

// remember child process for exe so we can kill it when app exits
var exeChildProcess = null;

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
    const exe = path.join(__dirname, 'build/exe/ReticulumWebChat');

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
