/**
 * A simple class for recording microphone input and returning the audio encoded in codec2
 */
class Codec2MicrophoneRecorder {

    constructor() {

        this.sampleRate = 8000;
        this.codec2Mode = "1200";
        this.audioChunks = [];

        this.audioContext = null;
        this.audioWorkletNode = null;
        this.microphoneMediaStream = null;
        this.mediaStreamSource = null;

    }

    async start() {
        try {

            // load audio worklet module
            this.audioContext = new AudioContext({ sampleRate: this.sampleRate });
            await this.audioContext.audioWorklet.addModule('assets/js/codec2-emscripten/processor.js');
            this.audioWorkletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');

            // handle audio received from audio worklet
            this.audioWorkletNode.port.onmessage = async (event) => {
                this.audioChunks.push(event.data);
            };

            // request access to the microphone
            this.microphoneMediaStream = await navigator.mediaDevices.getUserMedia({
                audio: true,
            });

            // send mic audio to audio worklet
            this.mediaStreamSource = this.audioContext.createMediaStreamSource(this.microphoneMediaStream);
            this.mediaStreamSource.connect(this.audioWorkletNode);

            // successfully started recording
            return true;

        } catch(e) {
            console.log(e);
            return false;
        }
    }

    async stop() {

        // disconnect media stream source
        if(this.mediaStreamSource){
            this.mediaStreamSource.disconnect();
        }

        // stop using microphone
        if(this.microphoneMediaStream){
            this.microphoneMediaStream.getTracks().forEach(track => track.stop());
        }

        // disconnect the audio worklet node
        if(this.audioWorkletNode){
            this.audioWorkletNode.disconnect();
        }

        // close audio context
        if(this.audioContext && this.audioContext.state !== "closed"){
            this.audioContext.close();
        }

        // concatenate all audio chunks into a single array
        var fullAudio = [];
        for(const chunk of this.audioChunks){
            fullAudio = [
                ...fullAudio,
                ...chunk,
            ]
        }

        // convert audio to wav
        const buffer = WavEncoder.encodeWAV(fullAudio, this.sampleRate);

        // convert wav audio to codec2
        const rawBuffer = await Codec2Lib.audioFileToRaw(buffer, "audio.wav");
        const encoded = await Codec2Lib.runEncode(this.codec2Mode, rawBuffer);

        return encoded;

    }

}
