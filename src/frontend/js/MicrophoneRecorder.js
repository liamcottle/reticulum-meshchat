/**
 * A simple class for recording microphone input and returning the audio.
 */
class MicrophoneRecorder {

    constructor() {
        this.audioChunks = [];
        this.microphoneMediaStream = null;
        this.mediaRecorder = null;
    }

    async start() {
        try {

            // request access to the microphone
            this.microphoneMediaStream = await navigator.mediaDevices.getUserMedia({
                audio: true,
            });

            // create media recorder
            this.mediaRecorder = new MediaRecorder(this.microphoneMediaStream);

            // handle received audio from media recorder
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            // start recording
            this.mediaRecorder.start();

            // successfully started recording
            return true;

        } catch(e) {
            return false;
        }
    }

    async stop() {
        return new Promise((resolve, reject) => {
            try {

                // handle media recording stopped
                this.mediaRecorder.onstop = () => {

                    // stop using microphone
                    if(this.microphoneMediaStream){
                        this.microphoneMediaStream.getTracks().forEach(track => track.stop());
                    }

                    // create blob from audio chunks
                    const blob = new Blob(this.audioChunks, {
                        type: this.mediaRecorder.mimeType, // likely to be "audio/webm;codecs=opus" in chromium
                    });

                    // resolve promise
                    resolve(blob);

                };

                // stop recording
                this.mediaRecorder.stop();

            } catch(e) {
                reject(e);
            }
        });
    }

}

export default MicrophoneRecorder;
