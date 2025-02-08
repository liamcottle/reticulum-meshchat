class Utils {

    /**
     * Waits for the provided milliseconds, and then resolves.
     * @param millis
     * @returns {Promise<void>}
     */
    static async sleepMillis(millis) {
        await new Promise((resolve) => {
            setTimeout(resolve, millis);
        });
    }

    static bytesToHex(bytes) {
        for(var hex = [], i = 0; i < bytes.length; i++){
            var current = bytes[i] < 0 ? bytes[i] + 256 : bytes[i];
            hex.push((current >>> 4).toString(16));
            hex.push((current & 0xF).toString(16));
        }
        return hex.join("");
    }

    static md5(data) {
        var bytes = [];
        const hash = CryptoJS.MD5(CryptoJS.enc.Hex.parse(this.bytesToHex(data)));
        for(var i = 0; i < hash.sigBytes; i++){
            bytes.push((hash.words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff);
        }
        return bytes;
    }

    static packUInt32BE(value) {
        const buffer = new ArrayBuffer(4);
        const view = new DataView(buffer);
        view.setUint32(0, value, false);
        return new Uint8Array(buffer);
    }

    static unpackUInt32BE(byteArray) {
        const buffer = new Uint8Array(byteArray).buffer;
        const view = new DataView(buffer);
        return view.getUint32(0, false);
    }

}

class RNode {

    KISS_FEND = 0xC0;
    KISS_FESC = 0xDB;
    KISS_TFEND = 0xDC;
    KISS_TFESC = 0xDD;

    CMD_FREQUENCY = 0x01;
    CMD_BANDWIDTH = 0x02;
    CMD_TXPOWER = 0x03;
    CMD_SF = 0x04;
    CMD_CR = 0x05;
    CMD_RADIO_STATE = 0x06;

    CMD_STAT_RX = 0x21;
    CMD_STAT_TX = 0x22
    CMD_STAT_RSSI = 0x23;
    CMD_STAT_SNR = 0x24;

    CMD_BOARD = 0x47;
    CMD_PLATFORM = 0x48;
    CMD_MCU = 0x49;
    CMD_RESET = 0x55;
    CMD_RESET_BYTE = 0xF8;
    CMD_DEV_HASH = 0x56;
    CMD_FW_VERSION = 0x50;
    CMD_ROM_READ = 0x51;
    CMD_ROM_WRITE = 0x52;
    CMD_CONF_SAVE = 0x53;
    CMD_CONF_DELETE = 0x54;
    CMD_FW_HASH = 0x58;
    CMD_UNLOCK_ROM = 0x59;
    ROM_UNLOCK_BYTE = 0xF8;
    CMD_HASHES = 0x60;
    CMD_FW_UPD = 0x61;
    CMD_DISP_ROT = 0x67;
    CMD_DISP_RCND = 0x68;

    CMD_BT_CTRL = 0x46;
    CMD_BT_PIN = 0x62;

    CMD_DISP_READ = 0x66;

    CMD_DETECT = 0x08;
    DETECT_REQ = 0x73;
    DETECT_RESP = 0x46;

    RADIO_STATE_OFF = 0x00;
    RADIO_STATE_ON = 0x01;
    RADIO_STATE_ASK = 0xFF;

    CMD_ERROR = 0x90
    ERROR_INITRADIO = 0x01
    ERROR_TXFAILED = 0x02
    ERROR_EEPROM_LOCKED = 0x03

    PLATFORM_AVR = 0x90;
    PLATFORM_ESP32 = 0x80;
    PLATFORM_NRF52 = 0x70;

    MCU_1284P = 0x91;
    MCU_2560 = 0x92;
    MCU_ESP32 = 0x81;
    MCU_NRF52 = 0x71;

    BOARD_RNODE = 0x31;
    BOARD_HMBRW = 0x32;
    BOARD_TBEAM = 0x33;
    BOARD_HUZZAH32 = 0x34;
    BOARD_GENERIC_ESP32 = 0x35;
    BOARD_LORA32_V2_0 = 0x36;
    BOARD_LORA32_V2_1 = 0x37;
    BOARD_RAK4631 = 0x51;

    HASH_TYPE_TARGET_FIRMWARE = 0x01;
    HASH_TYPE_FIRMWARE = 0x02;

    constructor(serialPort) {
        this.serialPort = serialPort;
        this.reader = serialPort.readable.getReader();
        this.writable = serialPort.writable;
        this.callbacks = {};
        this.readLoop();
    }

    static async fromSerialPort(serialPort) {

        // open port
        await serialPort.open({
            baudRate: 115200,
        });

        return new RNode(serialPort);

    }

    async close() {

        // release reader lock
        try {
            this.reader.releaseLock();
        } catch(e) {
            //console.log("failed to release lock on serial port readable, ignoring...", e);
        }

        // close serial port
        try {
            await this.serialPort.close();
        } catch(e) {
            //console.log("failed to close serial port, ignoring...", e);
        }

    }

    async write(bytes) {
        const writer = this.writable.getWriter();
        try {
            await writer.write(new Uint8Array(bytes));
        } finally {
            writer.releaseLock();
        }
    }

    async readLoop() {
        try {
            let buffer = [];
            let inFrame = false;
            while(true){

                // read kiss frames until reader indicates it's done
                const { value, done } = await this.reader.read();
                if(done){
                    break;
                }

                // read kiss frames
                for(const byte of value){
                    if(byte === this.KISS_FEND){
                        if(inFrame){
                            // End of frame
                            const decodedFrame = this.decodeKissFrame(buffer);
                            if(decodedFrame){
                                this.onCommandReceived(decodedFrame);
                            } else {
                                console.warn("Invalid frame ignored.");
                            }
                            buffer = [];
                        }
                        inFrame = !inFrame;
                    } else if(inFrame) {
                        buffer.push(byte);
                    }
                }

            }
        } catch(error) {

            // ignore error if reader was released
            if(error instanceof TypeError){
                return;
            }

            console.error('Error reading from serial port: ', error);

        } finally {
            this.reader.releaseLock();
        }
    }

    onCommandReceived(data) {
        try {

            // get received command and bytes from data
            const [ command, ...bytes ] = data;
            console.log("onCommandReceived", "0x" + command.toString(16), bytes);

            // find callback for received command
            const callback = this.callbacks[command];
            if(!callback){
                return;
            }

            // fire callback
            callback(bytes);

            // forget callback
            delete this.callbacks[command];

        } catch(e) {
            console.log("failed to handle received command", data, e);
        }
    }

    decodeKissFrame(frame) {

        const data = [];
        let escaping = false;

        for(const byte of frame){
            if(escaping){
                if(byte === this.KISS_TFEND){
                    data.push(this.KISS_FEND);
                } else if(byte === this.KISS_TFESC) {
                    data.push(this.KISS_FESC);
                } else {
                    return null; // Invalid escape sequence
                }
                escaping = false;
            } else if(byte === this.KISS_FESC) {
                escaping = true;
            } else {
                data.push(byte);
            }
        }

        // return null if incomplete escape at end
        return escaping ? null : data;

    }

    createKissFrame(data) {
        let frame = [this.KISS_FEND];
        for(let byte of data){
            if(byte === this.KISS_FEND){
                frame.push(this.KISS_FESC, this.KISS_TFEND);
            } else if(byte === this.KISS_FESC){
                frame.push(this.KISS_FESC, this.KISS_TFESC);
            } else {
                frame.push(byte);
            }
        }
        frame.push(this.KISS_FEND);
        return new Uint8Array(frame);
    }

    async sendKissCommand(data) {
        await this.write(this.createKissFrame(data));
    }

    // sends a command to the rnode, and resolves the promise with the result
    async sendCommand(command, data) {
        return new Promise(async (resolve, reject) => {
            try {

                // listen for response
                this.callbacks[command] = (response) => {
                    resolve(response);
                };

                // send command
                await this.sendKissCommand([
                    command,
                    ...data,
                ]);

            } catch(e) {
                reject(e);
            }
        });
    }

    async reset() {
        await this.sendKissCommand([
            this.CMD_RESET,
            this.CMD_RESET_BYTE,
        ]);
    }

    async detect() {
        return new Promise(async (resolve) => {
            try {

                // timeout after provided millis
                const timeout = setTimeout(() => {
                    resolve(false);
                }, 2000);

                // detect rnode
                const response = await this.sendCommand(this.CMD_DETECT, [
                    this.DETECT_REQ,
                ]);

                // we no longer want to timeout
                clearTimeout(timeout);

                // device is an rnode if response is as expected
                const [ responseByte ] = response;
                const isRnode = responseByte === this.DETECT_RESP;
                resolve(isRnode);

            } catch(e) {
                resolve(false);
            }
        });

    }

    async getFirmwareVersion() {

        const response = await this.sendCommand(this.CMD_FW_VERSION, [
            0x00,
        ]);

        // read response from device
        var [ majorVersion, minorVersion ] = response;
        if(minorVersion.length === 1){
            minorVersion = "0" + minorVersion;
        }

        // 1.23
        return majorVersion + "." + minorVersion;

    }

    async getPlatform() {

        const response = await this.sendCommand(this.CMD_PLATFORM, [
            0x00,
        ]);

        // read response from device
        const [ platformByte ] = response;
        return platformByte;

    }

    async getMcu() {

        const response = await this.sendCommand(this.CMD_MCU, [
            0x00,
        ]);

        // read response from device
        const [ mcuByte ] = response;
        return mcuByte;

    }

    async getBoard() {

        const response = await this.sendCommand(this.CMD_BOARD, [
            0x00,
        ]);

        // read response from device
        const [ boardByte ] = response;
        return boardByte;

    }

    async getDeviceHash() {

        const response = await this.sendCommand(this.CMD_DEV_HASH, [
            0x01, // anything != 0x00
        ]);

        // read response from device
        const [ ...deviceHash ] = response;
        return deviceHash;

    }

    async getTargetFirmwareHash() {

        const response = await this.sendCommand(this.CMD_HASHES, [
            this.HASH_TYPE_TARGET_FIRMWARE,
        ]);

        // read response from device
        const [ hashType, ...targetFirmwareHash ] = response;
        return targetFirmwareHash;

    }

    async getFirmwareHash() {

        const response = await this.sendCommand(this.CMD_HASHES, [
            this.HASH_TYPE_FIRMWARE,
        ]);

        // read response from device
        const [ hashType, ...firmwareHash ] = response;
        return firmwareHash;

    }

    async getRom() {

        const response = await this.sendCommand(this.CMD_ROM_READ, [
            0x00,
        ]);

        // read response from device
        const [ ...eepromBytes ] = response;
        return eepromBytes;

    }

    async getFrequency() {

        const response = await this.sendCommand(this.CMD_FREQUENCY, [
            // request frequency by sending zero as 4 bytes
            0x00,
            0x00,
            0x00,
            0x00,
        ]);

        // read response from device
        const [ ...frequencyBytes ] = response;

        // convert 4 bytes to 32bit integer representing frequency in hertz
        const frequencyInHz = frequencyBytes[0] << 24 | frequencyBytes[1] << 16 | frequencyBytes[2] << 8 | frequencyBytes[3];
        return frequencyInHz;

    }

    async getBandwidth() {

        const response = await this.sendCommand(this.CMD_BANDWIDTH, [
            // request bandwidth by sending zero as 4 bytes
            0x00,
            0x00,
            0x00,
            0x00,
        ]);

        // read response from device
        const [ ...bandwidthBytes ] = response;

        // convert 4 bytes to 32bit integer representing bandwidth in hertz
        const bandwidthInHz = bandwidthBytes[0] << 24 | bandwidthBytes[1] << 16 | bandwidthBytes[2] << 8 | bandwidthBytes[3];
        return bandwidthInHz;

    }

    async getTxPower() {

        const response = await this.sendCommand(this.CMD_TXPOWER, [
            0xFF, // request tx power
        ]);

        // read response from device
        const [ txPower ] = response;
        return txPower;

    }

    async getSpreadingFactor() {

        const response = await this.sendCommand(this.CMD_SF, [
            0xFF, // request spreading factor
        ]);

        // read response from device
        const [ spreadingFactor ] = response;
        return spreadingFactor;

    }

    async getCodingRate() {

        const response = await this.sendCommand(this.CMD_CR, [
            0xFF, // request coding rate
        ]);

        // read response from device
        const [ codingRate ] = response;
        return codingRate;

    }

    async getRadioState() {

        const response = await this.sendCommand(this.CMD_RADIO_STATE, [
            0xFF, // request radio state
        ]);

        // read response from device
        const [ radioState ] = response;
        return radioState;

    }

    async getRxStat() {

        const response = await this.sendCommand(this.CMD_STAT_RX, [
            0x00,
        ]);

        // read response from device
        const [ ...statBytes ] = response;

        // convert 4 bytes to 32bit integer
        const stat = statBytes[0] << 24 | statBytes[1] << 16 | statBytes[2] << 8 | statBytes[3];
        return stat;

    }

    async getTxStat() {

        const response = await this.sendCommand(this.CMD_STAT_TX, [
            0x00,
        ]);

        // read response from device
        const [ ...statBytes ] = response;

        // convert 4 bytes to 32bit integer
        const stat = statBytes[0] << 24 | statBytes[1] << 16 | statBytes[2] << 8 | statBytes[3];
        return stat;

    }

    async getRssiStat() {

        const response = await this.sendCommand(this.CMD_STAT_RSSI, [
            0x00,
        ]);

        // read response from device
        const [ rssi ] = response;
        return rssi;

    }

    async disableBluetooth() {
        await this.sendKissCommand([
            this.CMD_BT_CTRL,
            0x00, // stop
        ]);
    }

    async enableBluetooth() {
        await this.sendKissCommand([
            this.CMD_BT_CTRL,
            0x01, // start
        ]);
    }

    async startBluetoothPairing(pinCallback) {

        // listen for bluetooth pin
        // pin will be available once the user has initiated pairing from an Android device
        this.callbacks[this.CMD_BT_PIN] = (response) => {

            // read response from device
            const [ ...pinBytes ] = response;

            // convert 4 bytes to 32bit integer
            const pin = pinBytes[0] << 24 | pinBytes[1] << 16 | pinBytes[2] << 8 | pinBytes[3];

            // tell user what the bluetooth pin is
            console.log("Bluetooth Pairing Pin: " + pin);
            pinCallback(pin);

        };

        // enable pairing
        await this.sendKissCommand([
            this.CMD_BT_CTRL,
            0x02, // enable pairing
        ]);

    }

    async readDisplay() {

        const response = await this.sendCommand(this.CMD_DISP_READ, [
            0x01,
        ]);

        // read response from device
        const [ ...displayBuffer ] = response;
        return displayBuffer;

    }

    async setFrequency(frequencyInHz) {

        const c1 = frequencyInHz >> 24;
        const c2 = frequencyInHz >> 16 & 0xFF;
        const c3 = frequencyInHz >> 8 & 0xFF;
        const c4 = frequencyInHz & 0xFF;

        await this.sendKissCommand([
            this.CMD_FREQUENCY,
            c1,
            c2,
            c3,
            c4,
        ]);

    }

    async setBandwidth(bandwidthInHz) {

        const c1 = bandwidthInHz >> 24;
        const c2 = bandwidthInHz >> 16 & 0xFF;
        const c3 = bandwidthInHz >> 8 & 0xFF;
        const c4 = bandwidthInHz & 0xFF;

        await this.sendKissCommand([
            this.CMD_BANDWIDTH,
            c1,
            c2,
            c3,
            c4,
        ]);

    }

    async setTxPower(db) {
        await this.sendKissCommand([
            this.CMD_TXPOWER,
            db,
        ]);
    }

    async setSpreadingFactor(spreadingFactor) {
        await this.sendKissCommand([
            this.CMD_SF,
            spreadingFactor,
        ]);
    }

    async setCodingRate(codingRate) {
        await this.sendKissCommand([
            this.CMD_CR,
            codingRate,
        ]);
    }

    async setRadioStateOn() {
        await this.sendKissCommand([
            this.CMD_RADIO_STATE,
            this.RADIO_STATE_ON,
        ]);
    }

    async setRadioStateOff() {
        await this.sendKissCommand([
            this.CMD_RADIO_STATE,
            this.RADIO_STATE_OFF,
        ]);
    }

    // setTNCMode
    async saveConfig() {
        await this.sendKissCommand([
            this.CMD_CONF_SAVE,
            0x00,
        ]);
    }

    // setNormalMode
    async deleteConfig() {
        await this.sendKissCommand([
            this.CMD_CONF_DELETE,
            0x00,
        ]);
    }

    async indicateFirmwareUpdate() {
        await this.sendKissCommand([
            this.CMD_FW_UPD,
            0x01,
        ]);
    }

    async setFirmwareHash(hash) {
        await this.sendKissCommand([
            this.CMD_FW_HASH,
            ...hash,
        ]);
    }

    async writeRom(address, value) {

        // write to rom
        await this.sendKissCommand([
            this.CMD_ROM_WRITE,
            address,
            value,
        ]);

        // wait a bit to allow device to write to rom
        await Utils.sleepMillis(85);

    }

    async wipeRom() {

        await this.sendKissCommand([
            this.CMD_UNLOCK_ROM,
            this.ROM_UNLOCK_BYTE,
        ]);

        // wiping can take up to 30 seconds
        await Utils.sleepMillis(30000);

    }

    async getRomAsObject() {
        const rom = await this.getRom();
        return new ROM(rom);
    }

    async setDisplayRotation(rotation) {
        await this.sendKissCommand([
            this.CMD_DISP_ROT,
            rotation & 0xFF,
        ]);
    }

    async startDisplayReconditioning() {
        await this.sendKissCommand([
            this.CMD_DISP_RCND,
            0x01,
        ]);
    }

}

class ROM {

    static PLATFORM_AVR   = 0x90
    static PLATFORM_ESP32 = 0x80
    static PLATFORM_NRF52 = 0x70

    static MCU_1284P      = 0x91
    static MCU_2560       = 0x92
    static MCU_ESP32      = 0x81
    static MCU_NRF52      = 0x71

    static PRODUCT_RAK4631 = 0x10
    static MODEL_11       = 0x11
    static MODEL_12       = 0x12

    static PRODUCT_RNODE  = 0x03
    static MODEL_A1       = 0xA1
    static MODEL_A6       = 0xA6
    static MODEL_A4       = 0xA4
    static MODEL_A9       = 0xA9
    static MODEL_A3       = 0xA3
    static MODEL_A8       = 0xA8
    static MODEL_A2       = 0xA2
    static MODEL_A7       = 0xA7
    static MODEL_A5       = 0xA5;
    static MODEL_AA       = 0xAA;
    static MODEL_AC       = 0xAC;

    static PRODUCT_T32_10 = 0xB2
    static MODEL_BA       = 0xBA
    static MODEL_BB       = 0xBB

    static PRODUCT_T32_20 = 0xB0
    static MODEL_B3       = 0xB3
    static MODEL_B8       = 0xB8

    static PRODUCT_T32_21 = 0xB1
    static MODEL_B4       = 0xB4
    static MODEL_B9       = 0xB9
    static MODEL_B4_TCXO  = 0x04 // The TCXO model codes are only used here to select the
    static MODEL_B9_TCXO  = 0x09 // correct firmware, actual model codes in firmware is still 0xB4 and 0xB9.

    static PRODUCT_H32_V2 = 0xC0
    static MODEL_C4       = 0xC4
    static MODEL_C9       = 0xC9

    static PRODUCT_H32_V3 = 0xC1
    static MODEL_C5       = 0xC5
    static MODEL_CA       = 0xCA

    static PRODUCT_HELTEC_T114 = 0xC2
    static MODEL_C6       = 0xC6
    static MODEL_C7       = 0xC7

    static PRODUCT_TBEAM  = 0xE0
    static MODEL_E4       = 0xE4
    static MODEL_E9       = 0xE9
    static MODEL_E3       = 0xE3
    static MODEL_E8       = 0xE8

    static PRODUCT_TBEAM_S_V1 = 0xEA;
    static MODEL_DB           = 0xDB
    static MODEL_DC           = 0xDC

    static PRODUCT_TDECK  = 0xD0;
    static MODEL_D4       = 0xD4;
    static MODEL_D9       = 0xD9;

    static PRODUCT_TECHO  = 0x15;
    static MODEL_16       = 0x16;
    static MODEL_17       = 0x17;

    static PRODUCT_HMBRW  = 0xF0
    static MODEL_FF       = 0xFF
    static MODEL_FE       = 0xFE

    static ADDR_PRODUCT   = 0x00
    static ADDR_MODEL     = 0x01
    static ADDR_HW_REV    = 0x02
    static ADDR_SERIAL    = 0x03
    static ADDR_MADE      = 0x07
    static ADDR_CHKSUM    = 0x0B
    static ADDR_SIGNATURE = 0x1B
    static ADDR_INFO_LOCK = 0x9B
    static ADDR_CONF_SF   = 0x9C
    static ADDR_CONF_CR   = 0x9D
    static ADDR_CONF_TXP  = 0x9E
    static ADDR_CONF_BW   = 0x9F
    static ADDR_CONF_FREQ = 0xA3
    static ADDR_CONF_OK   = 0xA7

    static INFO_LOCK_BYTE = 0x73
    static CONF_OK_BYTE   = 0x73

    static BOARD_RNODE         = 0x31
    static BOARD_HMBRW         = 0x32
    static BOARD_TBEAM         = 0x33
    static BOARD_HUZZAH32      = 0x34
    static BOARD_GENERIC_ESP32 = 0x35
    static BOARD_LORA32_V2_0   = 0x36
    static BOARD_LORA32_V2_1   = 0x37
    static BOARD_RAK4631       = 0x51

    static MANUAL_FLASH_MODELS = [ROM.MODEL_A1, ROM.MODEL_A6]

    constructor(eeprom) {
        this.eeprom = eeprom;
    }

    getProduct() {
        return this.eeprom[ROM.ADDR_PRODUCT];
    }

    getModel() {
        return this.eeprom[ROM.ADDR_MODEL];
    }

    getHardwareRevision() {
        return this.eeprom[ROM.ADDR_HW_REV];
    }

    getSerialNumber() {
        return [
            this.eeprom[ROM.ADDR_SERIAL],
            this.eeprom[ROM.ADDR_SERIAL + 1],
            this.eeprom[ROM.ADDR_SERIAL + 2],
            this.eeprom[ROM.ADDR_SERIAL + 3],
        ];
    }

    getMade() {
        return [
            this.eeprom[ROM.ADDR_MADE],
            this.eeprom[ROM.ADDR_MADE + 1],
            this.eeprom[ROM.ADDR_MADE + 2],
            this.eeprom[ROM.ADDR_MADE + 3],
        ];
    }

    getChecksum() {
        const checksum = [];
        for(var i = 0; i < 16; i++){
            checksum.push(this.eeprom[ROM.ADDR_CHKSUM + i]);
        }
        return checksum;
    }

    getSignature() {
        const signature = [];
        for(var i = 0; i < 128; i++){
            signature.push(this.eeprom[ROM.ADDR_SIGNATURE + i]);
        }
        return signature;
    }

    getCalculatedChecksum() {
        return Utils.md5([
            this.getProduct(),
            this.getModel(),
            this.getHardwareRevision(),
            ...this.getSerialNumber(),
            ...this.getMade(),
        ]);
    }

    getConfiguredSpreadingFactor() {
        return this.eeprom[ROM.ADDR_CONF_SF];
    }

    getConfiguredCodingRate() {
        return this.eeprom[ROM.ADDR_CONF_CR];
    }

    getConfiguredTxPower() {
        return this.eeprom[ROM.ADDR_CONF_TXP];
    }

    getConfiguredFrequency() {
        return this.eeprom[ROM.ADDR_CONF_FREQ] << 24
            | this.eeprom[ROM.ADDR_CONF_FREQ + 1] << 16
            | this.eeprom[ROM.ADDR_CONF_FREQ + 2] << 8
            | this.eeprom[ROM.ADDR_CONF_FREQ + 3];
    }

    getConfiguredBandwidth() {
        return this.eeprom[ROM.ADDR_CONF_BW] << 24
            | this.eeprom[ROM.ADDR_CONF_BW + 1] << 16
            | this.eeprom[ROM.ADDR_CONF_BW + 2] << 8
            | this.eeprom[ROM.ADDR_CONF_BW + 3];
    }

    isInfoLocked() {
        return this.eeprom[ROM.ADDR_INFO_LOCK] === ROM.INFO_LOCK_BYTE;
    }

    isConfigured() {
        return this.eeprom[ROM.ADDR_CONF_OK] === ROM.CONF_OK_BYTE;
    }

    parse() {

        // ensure info lock byte is set
        if(!this.isInfoLocked()){
            return null;
        }

        // convert to hex
        const checksumHex = Utils.bytesToHex(this.getChecksum());
        const calculatedChecksumHex = Utils.bytesToHex(this.getCalculatedChecksum());
        const signatureHex = Utils.bytesToHex(this.getSignature());

        // add details
        var details = {
            is_provisioned: true,
            is_configured: this.isConfigured(),
            product: this.getProduct(),
            model: this.getModel(),
            hardware_revision: this.getHardwareRevision(),
            serial_number: Utils.unpackUInt32BE(this.getSerialNumber()),
            made: Utils.unpackUInt32BE(this.getMade()),
            checksum: checksumHex,
            calculated_checksum: calculatedChecksumHex,
            signature: signatureHex,
        }

        // if configured, add configuration to details
        if(details.is_configured){
            details = {
                ...details,
                configured_spreading_factor: this.getConfiguredSpreadingFactor(),
                configured_coding_rate: this.getConfiguredCodingRate(),
                configured_tx_power: this.getConfiguredTxPower(),
                configured_frequency: this.getConfiguredFrequency(),
                configured_bandwidth: this.getConfiguredBandwidth(),
            };
        }

        // if checksum in eeprom does not match checksum calculated from info, it is not provisioned
        if(details.checksum !== details.calculated_checksum){
            details.is_provisioned = false;
        }

        return details;

    }

}
