const { app, BrowserWindow, dialog, ipcMain, shell, systemPreferences } = require('electron');
const electronPrompt = require('electron-prompt');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('node:path');

// remember main window
var mainWindow = null;

// remember child process for exe so we can kill it when app exits
var exeChildProcess = null;

// allow fetching app version via ipc
ipcMain.handle('app-version', () => {
    return app.getVersion();
});

// add support for showing an alert window via ipc
ipcMain.handle('alert', async(event, message) => {
    return await dialog.showMessageBox(mainWindow, {
        message: message,
    });
});

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

// allow relaunching app via ipc
ipcMain.handle('relaunch', () => {
    app.relaunch();
    app.exit();
});

// allow showing a file path in os file manager
ipcMain.handle('showPathInFolder', (event, path) => {
    shell.showItemInFolder(path);
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

    // find path to python/cxfreeze reticulum meshchat executable
    const exeName = process.platform === "win32" ? "ReticulumMeshChat.exe" : "ReticulumMeshChat";
    var exe = path.join(__dirname, `build/exe/${exeName}`);

    // if dist exe doesn't exist, check local build
    if(!fs.existsSync(exe)){
        exe = path.join(__dirname, '..', `build/exe/${exeName}`);
    }

    // ask mac users for microphone access for audio calls to work
    if(process.platform === "darwin"){
        await systemPreferences.askForMediaAccess('microphone');
    }

    try {

        // determine path for storage
        const storageDir = path.join(app.getPath('home'), '.reticulum-meshchat'); // ~/.reticulum-meshchat

        // migrate old storage dir to new storage dir
        const oldStorageDir = path.join(app.getPath('home'), '.reticulum-webchat'); // ~/.reticulum-webchat
        if(fs.existsSync(oldStorageDir) && !fs.existsSync(storageDir)){
            fs.renameSync(oldStorageDir, storageDir);
        }

        // get arguments passed to application, and remove the provided application path
        const userProvidedArguments = process.argv.slice(1);

        // arguments we always want to pass in
        const requiredArguments = [
            '--headless', // reticulum meshchat usually launches default web browser, we don't want this when using electron
            '--port', '9337', // FIXME: let system pick a random unused port?
            // '--test-exception-message', 'Test Exception Message', // uncomment to test the crash dialog
        ];

        // if user didn't provide storage dir, we should provide it
        if(!userProvidedArguments.includes("--storage-dir")){
            requiredArguments.push("--storage-dir", storageDir);
        }

        // spawn executable
        exeChildProcess = await spawn(exe, [
            ...requiredArguments, // always provide required arguments
            ...userProvidedArguments, // also include any user provided arguments
        ]);

        // log stdout
        var stdoutLines = [];
        exeChildProcess.stdout.setEncoding('utf8');
        exeChildProcess.stdout.on('data', function(data) {

            // log
            log(data.toString());

            // keep track of last 10 stdout lines
            stdoutLines.push(data.toString());
            if(stdoutLines.length > 10){
                stdoutLines.shift();
            }

        });

        // log stderr
        var stderrLines = [];
        exeChildProcess.stderr.setEncoding('utf8');
        exeChildProcess.stderr.on('data', function(data) {

            // log
            log(data.toString());

            // keep track of last 10 stderr lines
            stderrLines.push(data.toString());
            if(stderrLines.length > 10){
                stderrLines.shift();
            }

        });

        // log errors
        exeChildProcess.on('error', function(error) {
            log(error);
        });

        // quit electron app if exe dies
        exeChildProcess.on('exit', async function(code) {

            // if no exit code provided, we wanted exit to happen, so do nothing
            if(code == null){
                return;
            }

            // tell user that Visual C++ redistributable needs to be installed on Windows
            if(code === 3221225781 && process.platform === "win32"){
                await dialog.showMessageBox(mainWindow, {
                    message: "Microsoft Visual C++ redistributable must be installed to run this application.",
                });
                app.quit();
                return;
            }

            // show crash log
            const stdout = stdoutLines.join("");
            const stderr = stderrLines.join("");
            await dialog.showMessageBox(mainWindow, {
                message: [
                    "MeshChat Crashed!",
                    "",
                    `Exit Code: ${code}`,
                    "",
                    `----- stdout -----`,
                    "",
                    stdout,
                    `----- stderr -----`,
                    "",
                    stderr,
                ].join("\n"),
            });

            // quit after dismissing error dialog
            app.quit();

        });

    } catch(e) {
        log(e);
    }

});

function quit() {

    // kill python process
    if(exeChildProcess){
        exeChildProcess.kill("SIGKILL");
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
