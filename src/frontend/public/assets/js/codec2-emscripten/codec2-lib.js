class Codec2Lib {

    static arrayBufferToBase64(buffer) {
        let binary = "";
        let bytes = new Uint8Array(buffer);
        for (let byte of bytes) {
            binary += String.fromCharCode(byte);
        }
        return window.btoa(binary);
    }

    static base64ToArrayBuffer(base64) {
        let binary = window.atob(base64);
        let bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return bytes.buffer;
    }

    static readFileAsArrayBuffer(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                resolve(reader.result);
            };
            reader.readAsArrayBuffer(file);
        });
    }

    static runDecode(mode, data) {
        return new Promise((resolve, reject) => {
            const module = {
                arguments: [mode, "input.bit", "output.raw"],
                preRun: () => {
                    module.FS.writeFile("input.bit", new Uint8Array(data));
                },
                postRun: () => {
                    let buffer = module.FS.readFile("output.raw", {
                        encoding: "binary",
                    });
                    resolve(buffer);
                },
            };
            createC2Dec(module);
        });
    }

    static runEncode(mode, data) {
        return new Promise((resolve, reject) => {
            const module = {
                arguments: [mode, "input.raw", "output.bit"],
                preRun: () => {
                    module.FS.writeFile("input.raw", new Uint8Array(data));
                },
                postRun: () => {
                    let buffer = module.FS.readFile("output.bit", {
                        encoding: "binary",
                    });
                    resolve(buffer);
                },
            };
            createC2Enc(module);
        });
    }

    static rawToWav(buffer) {
        return new Promise((resolve, reject) => {
            const module = {
                arguments: [
                    "-r",
                    "8000",
                    "-L",
                    "-e",
                    "signed-integer",
                    "-b",
                    "16",
                    "-c",
                    "1",
                    "input.raw",
                    "output.wav",
                ],
                preRun: () => {
                    module.FS.writeFile("input.raw", new Uint8Array(buffer));
                },
                postRun: () => {
                    let output = module.FS.readFile("output.wav", {
                        encoding: "binary",
                    });
                    resolve(output);
                },
            };
            SOXModule(module);
        });
    }

    static audioFileToRaw(buffer, filename) {
        return new Promise((resolve, reject) => {
            const module = {
                arguments: [
                    filename,
                    "-r",
                    "8000",
                    "-L",
                    "-e",
                    "signed-integer",
                    "-b",
                    "16",
                    "-c",
                    "1",
                    "output.raw",
                ],
                preRun: () => {
                    module.FS.writeFile(filename, new Uint8Array(buffer));
                },
                postRun: () => {
                    let output = module.FS.readFile("output.raw", {
                        encoding: "binary",
                    });
                    resolve(output);
                },
            };
            SOXModule(module);
        });
    }

}
