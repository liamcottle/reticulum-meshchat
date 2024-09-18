import moment from "moment";

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

    static parseSeconds(secondsToFormat) {
        secondsToFormat = Number(secondsToFormat);
        var days = Math.floor(secondsToFormat / (3600 * 24));
        var hours = Math.floor((secondsToFormat % (3600 * 24)) / 3600);
        var minutes = Math.floor((secondsToFormat % 3600) / 60);
        var seconds = Math.floor(secondsToFormat % 60);
        return {
            days: days,
            hours: hours,
            minutes: minutes,
            seconds: seconds,
        };
    }

    static formatSeconds(seconds) {

        const parsedSeconds = this.parseSeconds(seconds);

        if(parsedSeconds.days > 0){
            if(parsedSeconds.days === 1){
                return "1 day ago";
            } else {
                return parsedSeconds.days + " days ago";
            }
        }

        if(parsedSeconds.hours > 0){
            if(parsedSeconds.hours === 1){
                return "1 hour ago";
            } else {
                return parsedSeconds.hours + " hours ago";
            }
        }

        if(parsedSeconds.minutes > 0){
            if(parsedSeconds.minutes === 1){
                return "a minute ago";
            } else {
                return parsedSeconds.minutes + " minutes ago";
            }
        }

        if(parsedSeconds.seconds <= 1){
            return "a second ago";
        } else {
            return parsedSeconds.seconds + " seconds ago";
        }

    }

    static formatTimeAgo(datetimeString) {
        const millisecondsAgo = Date.now() - new Date(datetimeString).getTime();
        const secondsAgo = Math.round(millisecondsAgo / 1000);
        return this.formatSeconds(secondsAgo);
    }

    static formatSecondsAgo(seconds) {
        const secondsAgo = Math.round((Date.now() / 1000) - seconds);
        return this.formatSeconds(secondsAgo);
    }

    static formatMinutesSeconds(seconds) {
        const parsedSeconds = this.parseSeconds(seconds);
        const paddedMinutes = parsedSeconds.minutes.toString().padStart(2, "0");
        const paddedSeconds = parsedSeconds.seconds.toString().padStart(2, "0");
        return `${paddedMinutes}:${paddedSeconds}`;
    }

    static convertUnixMillisToLocalDateTimeString(unixTimestampInMilliseconds) {
        return moment(unixTimestampInMilliseconds, "x").local().format('YYYY-MM-DD hh:mm A')
    }

    static convertDateTimeToLocalDateTimeString(dateTime) {
        return this.convertUnixMillisToLocalDateTimeString(dateTime.getTime());
    }

    static arrayBufferToBase64(arrayBuffer) {
        var binary = '';
        var bytes = new Uint8Array(arrayBuffer);
        var len = bytes.byteLength;
        for(var i = 0; i < len; i++){
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

    static formatBitsPerSecond(bits) {

        if(bits === 0){
            return '0 bps';
        }

        const k = 1000; // Use 1000 instead of 1024 for network speeds
        const decimals = 0;
        const sizes = ['bps', 'kbps', 'Mbps', 'Gbps', 'Tbps', 'Pbps', 'Ebps', 'Zbps', 'Ybps'];

        const i = Math.floor(Math.log(bits) / Math.log(k));

        return parseFloat((bits / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];

    }

    static formatFrequency(hz) {

        if(hz === 0 || hz == null){
            return '0 Hz';
        }

        const k = 1000;
        const sizes = ['Hz', 'kHz', 'MHz', 'GHz', 'THz', 'PHz', 'EHz', 'ZHz', 'YHz'];
        const i = Math.floor(Math.log(hz) / Math.log(k));

        return parseFloat((hz / Math.pow(k, i))) + ' ' + sizes[i];

    }

    static decodeBase64ToUtf8String(base64) {
        // support for decoding base64 as a utf8 string to support emojis and cyrillic characters etc
        return decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
    }

    static isInterfaceEnabled(iface) {
        const rawValue = iface.enabled ?? iface.interface_enabled;
        const value = rawValue?.toLowerCase();
        return value === "on" || value === "yes" || value === "true";
    }

}

export default Utils;
