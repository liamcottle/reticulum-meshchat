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

                // convert audio received from worklet processor to wav
                const buffer = WavEncoder.encodeWAV(event.data, this.sampleRate);

                // convert wav audio to codec2
                const rawBuffer = await Codec2Lib.audioFileToRaw(buffer, "audio.wav");
                const encoded = await Codec2Lib.runEncode(this.codec2Mode, rawBuffer);

                // pass encoded audio to callback
                this.audioChunks.push(new Uint8Array(encoded.buffer));

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

    stop() {

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

        // calculate total length
        let totalLength = 0;
        for(const chunk of this.audioChunks){
            totalLength += chunk.length;
        }

        // create a new Uint8Array with the total length
        const concatenatedArray = new Uint8Array(totalLength);

        // copy each chunk into the new array
        let offset = 0;
        for(const chunk of this.audioChunks){
            concatenatedArray.set(chunk, offset);
            offset += chunk.length;
        }

        return concatenatedArray;

    }

}
