<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">
        <div class="overflow-y-auto p-2 space-y-2">

            <!-- community interfaces -->
            <div v-if="!isEditingInterface && config != null && config.show_suggested_community_interfaces" class="bg-white rounded shadow divide-y divide-gray-200">
                <div class="flex p-2">
                    <div class="my-auto mr-auto">
                        <div class="font-bold">Community Interfaces</div>
                        <div class="text-sm">These TCP interfaces serve as a quick way to test Reticulum. We suggest running your own as these may not always be available.</div>
                    </div>
                    <div class="my-auto ml-2">
                        <button @click="updateConfig({'show_suggested_community_interfaces': false})" type="button" class="text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="divide-y divide-gray-200">

                    <div class="flex px-2 py-1">
                        <div class="my-auto mr-auto">
                            <div>RNS Testnet Amsterdam</div>
                            <div class="text-xs">amsterdam.connect.reticulum.network:4965</div>
                        </div>
                        <div class="ml-2 my-auto">
                            <button @click="newInterfaceName='RNS Testnet Amsterdam';newInterfaceType='TCPClientInterface';newInterfaceTargetHost='amsterdam.connect.reticulum.network';newInterfaceTargetPort='4965'" type="button" class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                <span>Use Interface</span>
                            </button>
                        </div>
                    </div>

                    <div class="flex px-2 py-1">
                        <div class="my-auto mr-auto">
                            <div>RNS Testnet BetweenTheBorders</div>
                            <div class="text-xs">reticulum.betweentheborders.com:4242</div>
                        </div>
                        <div class="ml-2 my-auto">
                            <button @click="newInterfaceName='RNS Testnet BetweenTheBorders';newInterfaceType='TCPClientInterface';newInterfaceTargetHost='reticulum.betweentheborders.com';newInterfaceTargetPort='4242'" type="button" class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                <span>Use Interface</span>
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            <!-- add interface form -->
            <div class="bg-white rounded shadow divide-y divide-gray-200">
                <div class="p-2 font-bold">
                    <span v-if="isEditingInterface">Edit Interface</span>
                    <span v-else>Add Interface</span>
                </div>
                <div class="p-2 space-y-3">

                    <!-- interface name -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-900">Name</label>
                        <input type="text" :disabled="isEditingInterface" placeholder="New Interface Name" v-model="newInterfaceName" class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" :class="[ isEditingInterface ? 'cursor-not-allowed bg-gray-200' : 'bg-gray-50' ]">
                        <div class="text-xs text-gray-600">Interface names must be unique.</div>
                    </div>

                    <!-- interface type -->
                    <div class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Type</label>
                        <select v-model="newInterfaceType" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            <option disabled selected>--</option>
                            <option value="AutoInterface">AutoInterface</option>
                            <option value="RNodeInterface">RNodeInterface</option>
                            <option value="TCPClientInterface">TCPClientInterface</option>
                            <option value="TCPServerInterface">TCPServerInterface</option>
                            <option value="UDPInterface">UDPInterface</option>
                        </select>
                        <div class="text-xs text-gray-600">
                            Need help? <a class="text-blue-500 underline" href="https://reticulum.network/manual/interfaces.html" target="_blank">Reticulum Docs: Configuring Interfaces</a>
                        </div>
                    </div>

                    <!-- interface target host -->
                    <div v-if="newInterfaceType === 'TCPClientInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Target Host</label>
                        <input type="text" placeholder="example.com" v-model="newInterfaceTargetHost" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface target port -->
                    <div v-if="newInterfaceType === 'TCPClientInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Target Port</label>
                        <input type="text" placeholder="1234" v-model="newInterfaceTargetPort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface listen ip -->
                    <div v-if="newInterfaceType === 'TCPServerInterface' || newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Listen IP</label>
                        <input type="text" placeholder="0.0.0.0" v-model="newInterfaceListenIp" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface listen port -->
                    <div v-if="newInterfaceType === 'TCPServerInterface' || newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Listen Port</label>
                        <input type="text" placeholder="1234" v-model="newInterfaceListenPort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface forward ip -->
                    <div v-if="newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Forward IP</label>
                        <input type="text" placeholder="255.255.255.255" v-model="newInterfaceForwardIp" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface listen port -->
                    <div v-if="newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Forward Port</label>
                        <input type="text" placeholder="1234" v-model="newInterfaceForwardPort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface port -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Port</label>
                        <select v-model="newInterfacePort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            <option v-for="comport of comports" :value="comport.device">{{ comport.device }} (Product: {{ comport.product ?? '?' }}, Serial: {{ comport.serial ?? '?' }})</option>
                        </select>
                    </div>

                    <!-- interface frequency -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Frequency (Hz)</label>
                        <input type="number" v-model="newInterfaceFrequency" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                        <div class="text-xs text-gray-600">{{ formatFrequency(newInterfaceFrequency) }}</div>
                    </div>

                    <!-- interface bandwidth -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Bandwidth</label>
                        <select v-model="newInterfaceBandwidth" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            <option v-for="bandwidth in RNodeInterfaceDefaults.bandwidths" :value="bandwidth">{{ bandwidth / 1000 }} KHz</option>
                        </select>
                    </div>

                    <!-- interface txpower -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Transmit Power (dBm)</label>
                        <input v-model="newInterfaceTxpower" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                    </div>

                    <!-- interface spreading factor -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Spreading Factor</label>
                        <select v-model="newInterfaceSpreadingFactor" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            <option v-for="spreadingfactor in RNodeInterfaceDefaults.spreadingfactors" :value="spreadingfactor">{{ spreadingfactor }}</option>
                        </select>
                    </div>

                    <!-- interface coding rate -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-2 text-sm font-medium text-gray-900">Coding Rate</label>
                        <select v-model="newInterfaceCodingRate" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            <option v-for="codingrate in RNodeInterfaceDefaults.codingrates" :value="codingrate">4:{{ codingrate }}</option>
                        </select>
                    </div>

                    <!-- add button -->
                    <button @click="addInterface" type="button" class="bg-green-500 hover:bg-green-400 focus-visible:outline-green-500 my-auto inline-flex items-center gap-x-1 rounded-md p-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
                        <span v-if="isEditingInterface">Save Interface</span>
                        <span v-else>Add Interface</span>
                    </button>

                </div>
            </div>

        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import DialogUtils from "../../js/DialogUtils";

export default {
    name: 'AddInterfacePage',
    data() {
        return {

            isEditingInterface: false,
            config: null,

            comports: [],

            newInterfaceName: null,
            newInterfaceType: null,

            newInterfaceTargetHost: null,
            newInterfaceTargetPort: null,

            newInterfaceListenIp: null,
            newInterfaceListenPort: null,

            newInterfaceForwardIp: null,
            newInterfaceForwardPort: null,

            newInterfacePort: null,
            newInterfaceFrequency: null,
            newInterfaceBandwidth: null,
            newInterfaceTxpower: null,
            newInterfaceSpreadingFactor: null,
            newInterfaceCodingRate: null,

            RNodeInterfaceDefaults: {
                // bandwidth in hz
                bandwidths: [
                    7800, // 7.8 kHz
                    10400, // 10.4 kHz
                    15600, // 15.6 kHz
                    20800, // 20.8 kHz
                    31250, // 31.25 kHz
                    41700, // 41.7 kHz
                    62500, // 62.5 kHz
                    125000, // 125 kHz
                    250000, // 250 kHz
                    500000, // 500 kHz
                    1625000, // 1625 kHz (for 2.4 GHz SX1280)
                ],
                codingrates: [
                    5, // 4:5
                    6, // 4:6
                    7, // 4:7
                    8, // 4:8
                ],
                spreadingfactors: [
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                ],
            },

        };
    },
    mounted() {

        this.getConfig();
        this.loadComports();

        // check if we are editing an interface
        const interfaceName = this.$route.query.interface_name;
        if(interfaceName != null){
            this.isEditingInterface = true;
            this.loadInterfaceToEdit(interfaceName);
        }

    },
    methods: {
        async getConfig() {
            try {
                const response = await window.axios.get(`/api/v1/config`);
                this.config = response.data.config;
            } catch(e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        async updateConfig(config) {
            try {
                const response = await window.axios.patch("/api/v1/config", config);
                this.config = response.data.config;
            } catch(e) {
                alert("Failed to save config!");
                console.log(e);
            }
        },
        async loadComports() {
            try {
                const response = await window.axios.get(`/api/v1/comports`);
                this.comports = response.data.comports;
            } catch(e) {
                // do nothing if failed to load interfaces
            }
        },
        async loadInterfaceToEdit(interfaceName) {
            try {

                // fetch interfaces
                const response = await window.axios.get(`/api/v1/reticulum/interfaces`);
                const interfaces = response.data.interfaces;

                // find interface, else show error and redirect to interfaces
                const iface = interfaces[interfaceName];
                if(!iface){
                    DialogUtils.alert("The selected interface for editing could not be found.");
                    this.$router.push({
                        "name": "interfaces",
                    });
                    return;
                }

                // set form values
                this.newInterfaceName = interfaceName;
                this.newInterfaceType = iface.type;

                // tcp client interface
                this.newInterfaceTargetHost = iface.target_host;
                this.newInterfaceTargetPort = iface.target_port;

                // tcp server interface & udp interface
                this.newInterfaceListenIp = iface.listen_ip;
                this.newInterfaceListenPort = iface.listen_port;

                // udp interface
                this.newInterfaceForwardIp = iface.forward_ip;
                this.newInterfaceForwardPort = iface.forward_port;

                // rnode interface
                this.newInterfacePort = iface.port;
                this.newInterfaceFrequency = iface.frequency;
                this.newInterfaceBandwidth = iface.bandwidth;
                this.newInterfaceTxpower = iface.txpower;
                this.newInterfaceSpreadingFactor = iface.spreadingfactor;
                this.newInterfaceCodingRate = iface.codingrate;

            } catch(e) {
                // do nothing if failed to load interfaces
            }
        },
        async addInterface() {

            try {

                // add interface
                const response = await window.axios.post(`/api/v1/reticulum/interfaces/add`, {
                    allow_overwriting_interface: this.isEditingInterface,
                    // required values
                    name: this.newInterfaceName,
                    type: this.newInterfaceType,
                    // tcp client interface
                    target_host: this.newInterfaceTargetHost,
                    target_port: this.newInterfaceTargetPort,
                    // tcp server interface & udp interface
                    listen_ip: this.newInterfaceListenIp,
                    listen_port: this.newInterfaceListenPort,
                    // udp interface
                    forward_ip: this.newInterfaceForwardIp,
                    forward_port: this.newInterfaceForwardPort,
                    // rnode interface
                    port: this.newInterfacePort,
                    frequency: this.newInterfaceFrequency,
                    bandwidth: this.newInterfaceBandwidth,
                    txpower: this.newInterfaceTxpower,
                    spreadingfactor: this.newInterfaceSpreadingFactor,
                    codingrate: this.newInterfaceCodingRate,
                });

                // show success message
                if(response.data.message){
                    DialogUtils.alert(response.data.message);
                }

                // go to interfaces page
                this.$router.push({
                    name: "interfaces",
                });

            } catch(e) {
                const message = e.response?.data?.message ?? "failed to add interface";
                DialogUtils.alert(message);
                console.log(e);
            }

        },
        formatFrequency(hz) {
            return Utils.formatFrequency(hz);
        },
    },
}
</script>
