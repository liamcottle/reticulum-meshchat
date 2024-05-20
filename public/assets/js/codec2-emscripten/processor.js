class AudioProcessor extends AudioWorkletProcessor {

    constructor() {
        super();
        this.bufferSize = 4096; // Adjust the buffer size as needed
        this.sampleRate = 8000; // Target sample rate
        this.inputBuffer = new Float32Array(this.bufferSize);
        this.bufferIndex = 0;
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            const inputData = input[0];
            for (let i = 0; i < inputData.length; i++) {
                if (this.bufferIndex < this.bufferSize) {
                    this.inputBuffer[this.bufferIndex++] = inputData[i];
                }
                if (this.bufferIndex === this.bufferSize) {
                    // Downsample the buffer and send to the main thread
                    const downsampledBuffer = this.downsampleBuffer(this.inputBuffer, this.sampleRate);
                    this.port.postMessage(downsampledBuffer);
                    this.bufferIndex = 0;
                }
            }
        }
        return true;
    }

    downsampleBuffer(buffer, targetSampleRate) {
        if (targetSampleRate === this.sampleRate) {
            return buffer;
        }
        const sampleRateRatio = this.sampleRate / targetSampleRate;
        const newLength = Math.round(buffer.length / sampleRateRatio);
        const result = new Float32Array(newLength);
        let offsetResult = 0;
        let offsetBuffer = 0;
        while (offsetResult < result.length) {
            const nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
            let accum = 0;
            let count = 0;
            for (let i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
                accum += buffer[i];
                count++;
            }
            result[offsetResult] = accum / count;
            offsetResult++;
            offsetBuffer = nextOffsetBuffer;
        }
        return result;
    }
}

registerProcessor('audio-processor', AudioProcessor);
