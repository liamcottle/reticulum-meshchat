class NotificationUtils {

    static showIncomingCallNotification() {
        Notification.requestPermission().then((result) => {
            if(result === "granted"){
                new window.Notification("Incoming Call", {
                    body: "Someone is calling you.",
                    tag: "new_audio_call", // only ever show one incoming call notification at a time
                });
            }
        });
    }

    static showNewMessageNotification() {
        Notification.requestPermission().then((result) => {
            if(result === "granted"){
                new window.Notification("New Message", {
                    body: "Someone sent you a message.",
                    tag: "new_message", // only ever show one new message notification at a time
                });
            }
        });
    }

}

export default NotificationUtils;
