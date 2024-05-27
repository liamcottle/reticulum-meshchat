const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('node:path');

// remember child process for exe so when can kill it when app exits
var exeChildProcess = null;

app.whenReady().then(async () => {

    // create browser window
    const win = new BrowserWindow({
        width: 1024,
        height: 768,
    })

    // navigate to loading page
    await win.loadFile(path.join(__dirname, 'loading.html'));

    // find path to reticulum webchat python/cxfreexe executable
    const exe = path.join(__dirname, '..', 'build/exe.macosx-12.4-x86_64-3.11/ReticulumWebChat');

    // spawn exe
    exeChildProcess = spawn(exe, [
        '--headless',
        '--port', '9337', // FIXME: let system pick a random unused port?
    ]);

    // listen to stdout
    exeChildProcess.stdout.setEncoding('utf8');
    exeChildProcess.stdout.on('data', function(data) {
        console.log('stdout: ' + data);
    });

    // listen to stderror
    exeChildProcess.stderr.setEncoding('utf8');
    exeChildProcess.stderr.on('data', function(data) {
        console.log('stderr: ' + data);
    });

    // listen to process exit
    exeChildProcess.on('exit', function(code) {
        console.log("exit: " + code);
    });

});

function quit() {

    // kill python process
    if(exeChildProcess){
        exeChildProcess.kill();
    }

    // quit electron app
    app.quit();

}

app.on('window-all-closed', () => {
    quit();
});
