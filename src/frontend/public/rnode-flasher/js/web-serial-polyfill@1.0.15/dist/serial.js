/*
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of
 * the License at
 *
 *    https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in
 * writing, software distributed under the License is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
 * OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing
 * permissions and limitations under the License.
 */
'use strict';
export var SerialPolyfillProtocol;
(function (SerialPolyfillProtocol) {
    SerialPolyfillProtocol[SerialPolyfillProtocol["UsbCdcAcm"] = 0] = "UsbCdcAcm";
})(SerialPolyfillProtocol || (SerialPolyfillProtocol = {}));
const kSetLineCoding = 0x20;
const kSetControlLineState = 0x22;
const kSendBreak = 0x23;
const kDefaultBufferSize = 255;
const kDefaultDataBits = 8;
const kDefaultParity = 'none';
const kDefaultStopBits = 1;
const kAcceptableDataBits = [16, 8, 7, 6, 5];
const kAcceptableStopBits = [1, 2];
const kAcceptableParity = ['none', 'even', 'odd'];
const kParityIndexMapping = ['none', 'odd', 'even'];
const kStopBitsIndexMapping = [1, 1.5, 2];
const kDefaultPolyfillOptions = {
    protocol: SerialPolyfillProtocol.UsbCdcAcm,
    usbControlInterfaceClass: 2,
    usbTransferInterfaceClass: 10,
};
/**
 * Utility function to get the interface implementing a desired class.
 * @param {USBDevice} device The USB device.
 * @param {number} classCode The desired interface class.
 * @return {USBInterface} The first interface found that implements the desired
 * class.
 * @throws TypeError if no interface is found.
 */
function findInterface(device, classCode) {
    const configuration = device.configurations[0];
    for (const iface of configuration.interfaces) {
        const alternate = iface.alternates[0];
        if (alternate.interfaceClass === classCode) {
            return iface;
        }
    }
    throw new TypeError(`Unable to find interface with class ${classCode}.`);
}
/**
 * Utility function to get an endpoint with a particular direction.
 * @param {USBInterface} iface The interface to search.
 * @param {USBDirection} direction The desired transfer direction.
 * @return {USBEndpoint} The first endpoint with the desired transfer direction.
 * @throws TypeError if no endpoint is found.
 */
function findEndpoint(iface, direction) {
    const alternate = iface.alternates[0];
    for (const endpoint of alternate.endpoints) {
        if (endpoint.direction == direction) {
            return endpoint;
        }
    }
    throw new TypeError(`Interface ${iface.interfaceNumber} does not have an ` +
        `${direction} endpoint.`);
}
/**
 * Implementation of the underlying source API[1] which reads data from a USB
 * endpoint. This can be used to construct a ReadableStream.
 *
 * [1]: https://streams.spec.whatwg.org/#underlying-source-api
 */
class UsbEndpointUnderlyingSource {
    /**
     * Constructs a new UnderlyingSource that will pull data from the specified
     * endpoint on the given USB device.
     *
     * @param {USBDevice} device
     * @param {USBEndpoint} endpoint
     * @param {function} onError function to be called on error
     */
    constructor(device, endpoint, onError) {
        this.type = 'bytes';
        this.device_ = device;
        this.endpoint_ = endpoint;
        this.onError_ = onError;
    }
    /**
     * Reads a chunk of data from the device.
     *
     * @param {ReadableByteStreamController} controller
     */
    pull(controller) {
        (async () => {
            var _a;
            let chunkSize;
            if (controller.desiredSize) {
                const d = controller.desiredSize / this.endpoint_.packetSize;
                chunkSize = Math.ceil(d) * this.endpoint_.packetSize;
            }
            else {
                chunkSize = this.endpoint_.packetSize;
            }
            try {
                const result = await this.device_.transferIn(this.endpoint_.endpointNumber, chunkSize);
                if (result.status != 'ok') {
                    controller.error(`USB error: ${result.status}`);
                    this.onError_();
                }
                if ((_a = result.data) === null || _a === void 0 ? void 0 : _a.buffer) {
                    const chunk = new Uint8Array(result.data.buffer, result.data.byteOffset, result.data.byteLength);
                    controller.enqueue(chunk);
                }
            }
            catch (error) {
                controller.error(error.toString());
                this.onError_();
            }
        })();
    }
}
/**
 * Implementation of the underlying sink API[2] which writes data to a USB
 * endpoint. This can be used to construct a WritableStream.
 *
 * [2]: https://streams.spec.whatwg.org/#underlying-sink-api
 */
class UsbEndpointUnderlyingSink {
    /**
     * Constructs a new UnderlyingSink that will write data to the specified
     * endpoint on the given USB device.
     *
     * @param {USBDevice} device
     * @param {USBEndpoint} endpoint
     * @param {function} onError function to be called on error
     */
    constructor(device, endpoint, onError) {
        this.device_ = device;
        this.endpoint_ = endpoint;
        this.onError_ = onError;
    }
    /**
     * Writes a chunk to the device.
     *
     * @param {Uint8Array} chunk
     * @param {WritableStreamDefaultController} controller
     */
    async write(chunk, controller) {
        try {
            const result = await this.device_.transferOut(this.endpoint_.endpointNumber, chunk);
            if (result.status != 'ok') {
                controller.error(result.status);
                this.onError_();
            }
        }
        catch (error) {
            controller.error(error.toString());
            this.onError_();
        }
    }
}
/** a class used to control serial devices over WebUSB */
export class SerialPort {
    /**
     * constructor taking a WebUSB device that creates a SerialPort instance.
     * @param {USBDevice} device A device acquired from the WebUSB API
     * @param {SerialPolyfillOptions} polyfillOptions Optional options to
     * configure the polyfill.
     */
    constructor(device, polyfillOptions) {
        this.polyfillOptions_ = Object.assign(Object.assign({}, kDefaultPolyfillOptions), polyfillOptions);
        this.outputSignals_ = {
            dataTerminalReady: false,
            requestToSend: false,
            break: false,
        };
        this.device_ = device;
        this.controlInterface_ = findInterface(this.device_, this.polyfillOptions_.usbControlInterfaceClass);
        this.transferInterface_ = findInterface(this.device_, this.polyfillOptions_.usbTransferInterfaceClass);
        this.inEndpoint_ = findEndpoint(this.transferInterface_, 'in');
        this.outEndpoint_ = findEndpoint(this.transferInterface_, 'out');
    }
    /**
     * Getter for the readable attribute. Constructs a new ReadableStream as
     * necessary.
     * @return {ReadableStream} the current readable stream
     */
    get readable() {
        var _a;
        if (!this.readable_ && this.device_.opened) {
            this.readable_ = new ReadableStream(new UsbEndpointUnderlyingSource(this.device_, this.inEndpoint_, () => {
                this.readable_ = null;
            }), {
                highWaterMark: (_a = this.serialOptions_.bufferSize) !== null && _a !== void 0 ? _a : kDefaultBufferSize,
            });
        }
        return this.readable_;
    }
    /**
     * Getter for the writable attribute. Constructs a new WritableStream as
     * necessary.
     * @return {WritableStream} the current writable stream
     */
    get writable() {
        var _a;
        if (!this.writable_ && this.device_.opened) {
            this.writable_ = new WritableStream(new UsbEndpointUnderlyingSink(this.device_, this.outEndpoint_, () => {
                this.writable_ = null;
            }), new ByteLengthQueuingStrategy({
                highWaterMark: (_a = this.serialOptions_.bufferSize) !== null && _a !== void 0 ? _a : kDefaultBufferSize,
            }));
        }
        return this.writable_;
    }
    /**
     * a function that opens the device and claims all interfaces needed to
     * control and communicate to and from the serial device
     * @param {SerialOptions} options Object containing serial options
     * @return {Promise<void>} A promise that will resolve when device is ready
     * for communication
     */
    async open(options) {
        this.serialOptions_ = options;
        this.validateOptions();
        try {
            await this.device_.open();
            if (this.device_.configuration === null) {
                await this.device_.selectConfiguration(1);
            }
            await this.device_.claimInterface(this.controlInterface_.interfaceNumber);
            if (this.controlInterface_ !== this.transferInterface_) {
                await this.device_.claimInterface(this.transferInterface_.interfaceNumber);
            }
            await this.setLineCoding();
            await this.setSignals({ dataTerminalReady: true });
        }
        catch (error) {
            if (this.device_.opened) {
                await this.device_.close();
            }
            throw new Error('Error setting up device: ' + error.toString());
        }
    }
    /**
     * Closes the port.
     *
     * @return {Promise<void>} A promise that will resolve when the port is
     * closed.
     */
    async close() {
        const promises = [];
        if (this.readable_) {
            promises.push(this.readable_.cancel());
        }
        if (this.writable_) {
            promises.push(this.writable_.abort());
        }
        await Promise.all(promises);
        this.readable_ = null;
        this.writable_ = null;
        if (this.device_.opened) {
            await this.setSignals({ dataTerminalReady: false, requestToSend: false });
            await this.device_.close();
        }
    }
    /**
     * Forgets the port.
     *
     * @return {Promise<void>} A promise that will resolve when the port is
     * forgotten.
     */
    async forget() {
        return this.device_.forget();
    }
    /**
     * A function that returns properties of the device.
     * @return {SerialPortInfo} Device properties.
     */
    getInfo() {
        return {
            usbVendorId: this.device_.vendorId,
            usbProductId: this.device_.productId,
        };
    }
    /**
     * A function used to change the serial settings of the device
     * @param {object} options the object which carries serial settings data
     * @return {Promise<void>} A promise that will resolve when the options are
     * set
     */
    reconfigure(options) {
        this.serialOptions_ = Object.assign(Object.assign({}, this.serialOptions_), options);
        this.validateOptions();
        return this.setLineCoding();
    }
    /**
     * Sets control signal state for the port.
     * @param {SerialOutputSignals} signals The signals to enable or disable.
     * @return {Promise<void>} a promise that is resolved when the signal state
     * has been changed.
     */
    async setSignals(signals) {
        this.outputSignals_ = Object.assign(Object.assign({}, this.outputSignals_), signals);
        if (signals.dataTerminalReady !== undefined ||
            signals.requestToSend !== undefined) {
            // The Set_Control_Line_State command expects a bitmap containing the
            // values of all output signals that should be enabled or disabled.
            //
            // Ref: USB CDC specification version 1.1 §6.2.14.
            const value = (this.outputSignals_.dataTerminalReady ? 1 << 0 : 0) |
                (this.outputSignals_.requestToSend ? 1 << 1 : 0);
            await this.device_.controlTransferOut({
                'requestType': 'class',
                'recipient': 'interface',
                'request': kSetControlLineState,
                'value': value,
                'index': this.controlInterface_.interfaceNumber,
            });
        }
        if (signals.break !== undefined) {
            // The SendBreak command expects to be given a duration for how long the
            // break signal should be asserted. Passing 0xFFFF enables the signal
            // until 0x0000 is send.
            //
            // Ref: USB CDC specification version 1.1 §6.2.15.
            const value = this.outputSignals_.break ? 0xFFFF : 0x0000;
            await this.device_.controlTransferOut({
                'requestType': 'class',
                'recipient': 'interface',
                'request': kSendBreak,
                'value': value,
                'index': this.controlInterface_.interfaceNumber,
            });
        }
    }
    /**
     * Checks the serial options for validity and throws an error if it is
     * not valid
     */
    validateOptions() {
        if (!this.isValidBaudRate(this.serialOptions_.baudRate)) {
            throw new RangeError('invalid Baud Rate ' + this.serialOptions_.baudRate);
        }
        if (!this.isValidDataBits(this.serialOptions_.dataBits)) {
            throw new RangeError('invalid dataBits ' + this.serialOptions_.dataBits);
        }
        if (!this.isValidStopBits(this.serialOptions_.stopBits)) {
            throw new RangeError('invalid stopBits ' + this.serialOptions_.stopBits);
        }
        if (!this.isValidParity(this.serialOptions_.parity)) {
            throw new RangeError('invalid parity ' + this.serialOptions_.parity);
        }
    }
    /**
     * Checks the baud rate for validity
     * @param {number} baudRate the baud rate to check
     * @return {boolean} A boolean that reflects whether the baud rate is valid
     */
    isValidBaudRate(baudRate) {
        return baudRate % 1 === 0;
    }
    /**
     * Checks the data bits for validity
     * @param {number} dataBits the data bits to check
     * @return {boolean} A boolean that reflects whether the data bits setting is
     * valid
     */
    isValidDataBits(dataBits) {
        if (typeof dataBits === 'undefined') {
            return true;
        }
        return kAcceptableDataBits.includes(dataBits);
    }
    /**
     * Checks the stop bits for validity
     * @param {number} stopBits the stop bits to check
     * @return {boolean} A boolean that reflects whether the stop bits setting is
     * valid
     */
    isValidStopBits(stopBits) {
        if (typeof stopBits === 'undefined') {
            return true;
        }
        return kAcceptableStopBits.includes(stopBits);
    }
    /**
     * Checks the parity for validity
     * @param {string} parity the parity to check
     * @return {boolean} A boolean that reflects whether the parity is valid
     */
    isValidParity(parity) {
        if (typeof parity === 'undefined') {
            return true;
        }
        return kAcceptableParity.includes(parity);
    }
    /**
     * sends the options alog the control interface to set them on the device
     * @return {Promise} a promise that will resolve when the options are set
     */
    async setLineCoding() {
        var _a, _b, _c;
        // Ref: USB CDC specification version 1.1 §6.2.12.
        const buffer = new ArrayBuffer(7);
        const view = new DataView(buffer);
        view.setUint32(0, this.serialOptions_.baudRate, true);
        view.setUint8(4, kStopBitsIndexMapping.indexOf((_a = this.serialOptions_.stopBits) !== null && _a !== void 0 ? _a : kDefaultStopBits));
        view.setUint8(5, kParityIndexMapping.indexOf((_b = this.serialOptions_.parity) !== null && _b !== void 0 ? _b : kDefaultParity));
        view.setUint8(6, (_c = this.serialOptions_.dataBits) !== null && _c !== void 0 ? _c : kDefaultDataBits);
        const result = await this.device_.controlTransferOut({
            'requestType': 'class',
            'recipient': 'interface',
            'request': kSetLineCoding,
            'value': 0x00,
            'index': this.controlInterface_.interfaceNumber,
        }, buffer);
        if (result.status != 'ok') {
            throw new DOMException('NetworkError', 'Failed to set line coding.');
        }
    }
}
/** implementation of the global navigator.serial object */
class Serial {
    /**
     * Requests permission to access a new port.
     *
     * @param {SerialPortRequestOptions} options
     * @param {SerialPolyfillOptions} polyfillOptions
     * @return {Promise<SerialPort>}
     */
    async requestPort(options, polyfillOptions) {
        polyfillOptions = Object.assign(Object.assign({}, kDefaultPolyfillOptions), polyfillOptions);
        const usbFilters = [];
        if (options && options.filters) {
            for (const filter of options.filters) {
                const usbFilter = {
                    classCode: polyfillOptions.usbControlInterfaceClass,
                };
                if (filter.usbVendorId !== undefined) {
                    usbFilter.vendorId = filter.usbVendorId;
                }
                if (filter.usbProductId !== undefined) {
                    usbFilter.productId = filter.usbProductId;
                }
                usbFilters.push(usbFilter);
            }
        }
        if (usbFilters.length === 0) {
            usbFilters.push({
                classCode: polyfillOptions.usbControlInterfaceClass,
            });
        }
        const device = await navigator.usb.requestDevice({ 'filters': usbFilters });
        const port = new SerialPort(device, polyfillOptions);
        return port;
    }
    /**
     * Get the set of currently available ports.
     *
     * @param {SerialPolyfillOptions} polyfillOptions Polyfill configuration that
     * should be applied to these ports.
     * @return {Promise<SerialPort[]>} a promise that is resolved with a list of
     * ports.
     */
    async getPorts(polyfillOptions) {
        polyfillOptions = Object.assign(Object.assign({}, kDefaultPolyfillOptions), polyfillOptions);
        const devices = await navigator.usb.getDevices();
        const ports = [];
        devices.forEach((device) => {
            try {
                const port = new SerialPort(device, polyfillOptions);
                ports.push(port);
            }
            catch (e) {
                // Skip unrecognized port.
            }
        });
        return ports;
    }
}
/* an object to be used for starting the serial workflow */
export const serial = new Serial();
//# sourceMappingURL=serial.js.map