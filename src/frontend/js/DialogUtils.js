class DialogUtils {

    static alert(message) {
        if(window.electron){
            // running inside electron, use ipc alert
            window.electron.alert(message);
        } else {
            // running inside normal browser, use browser alert
            window.alert(message);
        }
    }

    static async prompt(message) {
        if(window.electron){
            // running inside electron, use ipc prompt
            return await window.electron.prompt(message);
        } else {
            // running inside normal browser, use browser prompt
            return window.prompt(message);
        }
    }

}

export default DialogUtils;
