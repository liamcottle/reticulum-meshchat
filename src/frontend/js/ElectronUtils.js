class ElectronUtils {

    static isElectron() {
        return window.electron != null;
    }

    static relaunch() {
        if(window.electron){
            window.electron.relaunch();
        }
    }

    static showPathInFolder(path) {
        if(window.electron){
            window.electron.showPathInFolder(path);
        }
    }

}

export default ElectronUtils;
