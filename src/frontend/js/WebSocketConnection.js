import mitt from 'mitt';

class WebSocketConnection {

    constructor() {
        this.emitter = mitt();
        this.reconnect();
    }

    // add event listener
    on(event, handler) {
        this.emitter.on(event, handler);
    }

    // remove event listener
    off(event, handler) {
        this.emitter.off(event, handler);
    }

    // emit event
    emit(type, event) {
        this.emitter.emit(type, event);
    }

    reconnect() {

        // connect to websocket
        this.ws = new WebSocket(location.origin.replace(/^http/, 'ws') + "/ws");

        // auto reconnect when websocket closes
        this.ws.addEventListener('close', () => {
            setTimeout(() => {
                this.reconnect();
            }, 1000);
        });

        // emit data received from websocket
        this.ws.onmessage = (message) => {
            this.emit("message", message);
        };

    }

    send(message) {
        if(this.ws != null && this.ws.readyState === WebSocket.OPEN){
            this.ws.send(message);
        }
    }

}

export default new WebSocketConnection();
