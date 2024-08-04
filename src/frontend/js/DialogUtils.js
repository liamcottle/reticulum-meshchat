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

}

export default DialogUtils;
