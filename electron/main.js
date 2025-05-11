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

    // log to stdout of this process
    console.log(message);

    // make sure main window exists
    if(!mainWindow){
        return;
    }

    // make sure window is not destroyed
    if(mainWindow.isDestroyed()){
        return;
    }

    // log to web console
    mainWindow.webContents.send('log', message);

}

function getDefaultStorageDir() {

    // if we are running a windows portable exe, we want to use .reticulum-meshchat in the portable exe dir
    // e.g if we launch "E:\Some\Path\MeshChat.exe" we want to use "E:\Some\Path\.reticulum-meshchat"
    const portableExecutableDir = process.env.PORTABLE_EXECUTABLE_DIR;
    if(process.platform === "win32" && portableExecutableDir != null){
        return path.join(portableExecutableDir, '.reticulum-meshchat');
    }

    // otherwise, we will fall back to putting the storage dir in the users home directory
    // e.g: ~/.reticulum-meshchat
    return path.join(app.getPath('home'), '.reticulum-meshchat');

}

function getDefaultReticulumConfigDir() {

    // if we are running a windows portable exe, we want to use .reticulum in the portable exe dir
    // e.g if we launch "E:\Some\Path\MeshChat.exe" we want to use "E:\Some\Path\.reticulum"
    const portableExecutableDir = process.env.PORTABLE_EXECUTABLE_DIR;
    if(process.platform === "win32" && portableExecutableDir != null){
        return path.join(portableExecutableDir, '.reticulum');
    }

    // otherwise, we will fall back to using the .reticulum folder in the users home directory
    // e.g: ~/.reticulum
    return path.join(app.getPath('home'), '.reticulum');

}

app.whenReady().then(async () => {

    // get arguments passed to application, and remove the provided application path
    const ignoredArguments = ["--no-sandbox"];
    const userProvidedArguments = process.argv.slice(1)
        .filter(arg => !ignoredArguments.includes(arg));
    const shouldLaunchHeadless = userProvidedArguments.includes("--headless");

    if(!shouldLaunchHeadless){

        // create browser window
        mainWindow = new BrowserWindow({
            width: 1500,
            height: 800,
            webPreferences: {
                // used to inject logging over ipc
                preload: path.join(__dirname, 'preload.js'),
            },
        });

        // open external links in default web browser instead of electron
        mainWindow.webContents.setWindowOpenHandler(({ url }) => {

            var shouldShowInNewElectronWindow = false;

            // we want to open call.html in a new electron window
            // but all other target="_blank" links should open in the system web browser
            // we don't want /rnode-flasher/index.html to open in electron, otherwise user can't select usb devices...
            if(url.startsWith("http://localhost") && url.includes("/call.html")){
                shouldShowInNewElectronWindow = true;
            }

            // we want to open blob urls in a new electron window
            else if(url.startsWith("blob:")) {
                shouldShowInNewElectronWindow = true;
            }

            // open in new electron window
            if(shouldShowInNewElectronWindow){
                return {
                    action: "allow",
                };
            }

            // fallback to opening any other url in external browser
            shell.openExternal(url);
            return {
                action: "deny",
            };

        });

        // navigate to loading page
        await mainWindow.loadFile(path.join(__dirname, 'loading.html'));

        // ask mac users for microphone access for audio calls to work
        if(process.platform === "darwin"){
            await systemPreferences.askForMediaAccess('microphone');
        }

    }

    // find path to python/cxfreeze reticulum meshchat executable
    const exeName = process.platform === "win32" ? "ReticulumMeshChat.exe" : "ReticulumMeshChat";
    var exe = path.join(__dirname, `build/exe/${exeName}`);

    // if dist exe doesn't exist, check local build
    if(!fs.existsSync(exe)){
        exe = path.join(__dirname, '..', `build/exe/${exeName}`);
    }

    try {

        // arguments we always want to pass in
        const requiredArguments = [
            '--headless', // reticulum meshchat usually launches default web browser, we don't want this when using electron
            '--port', '9337', // FIXME: let system pick a random unused port?
            // '--test-exception-message', 'Test Exception Message', // uncomment to test the crash dialog
        ];

        // if user didn't provide reticulum config dir, we should provide it
        if(!userProvidedArguments.includes("--reticulum-config-dir")){
            requiredArguments.push("--reticulum-config-dir", getDefaultReticulumConfigDir());
        }

        // if user didn't provide storage dir, we should provide it
        if(!userProvidedArguments.includes("--storage-dir")){
            requiredArguments.push("--storage-dir", getDefaultStorageDir());
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
