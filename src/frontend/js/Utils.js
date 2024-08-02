class Utils {

    static formatBytes(bytes) {

        if(bytes === 0){
            return '0 Bytes';
        }

        const k = 1024;
        const decimals = 0;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];

    }

}

export default Utils;
