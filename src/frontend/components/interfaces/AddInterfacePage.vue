<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="overflow-y-auto p-2 space-y-2">

            <!-- community interfaces -->
            <div v-if="!isEditingInterface && config != null && config.show_suggested_community_interfaces" class="bg-white rounded shadow divide-y divide-gray-200 dark:bg-zinc-900">
                <div class="flex p-2">
                    <div class="my-auto mr-auto">
                        <div class="font-bold dark:text-white">Community Interfaces</div>
                        <div class="text-sm dark:text-gray-100">These TCP interfaces serve as a quick way to test Reticulum. We suggest running your own as these may not always be available.</div>
                    </div>
                    <div class="my-auto ml-2">
                        <button @click="updateConfig({'show_suggested_community_interfaces': false})" type="button" class="text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full dark:bg-zinc-600 dark:text-white dark:hover:bg-zinc-700 dark:focus-visible:outline-zinc-500">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z"/>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="divide-y divide-gray-200 dark:text-white">

                    <div class="flex px-2 py-1">
                        <div class="my-auto mr-auto">
                            <div>RNS Testnet Amsterdam</div>
                            <div class="text-xs">amsterdam.connect.reticulum.network:4965</div>
                        </div>
                        <div class="ml-2 my-auto">
                            <button
                                @click="newInterfaceName='RNS Testnet Amsterdam';newInterfaceType='TCPClientInterface';newInterfaceTargetHost='amsterdam.connect.reticulum.network';newInterfaceTargetPort='4965'"
                                type="button"
                                class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
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
                            <button
                                @click="newInterfaceName='RNS Testnet BetweenTheBorders';newInterfaceType='TCPClientInterface';newInterfaceTargetHost='reticulum.betweentheborders.com';newInterfaceTargetPort='4242'"
                                type="button"
                                class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                <span>Use Interface</span>
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            <!-- add interface form -->
            <div class="bg-white rounded shadow divide-y divide-gray-300 dark:divide-zinc-700 dark:bg-zinc-900">
                <div class="p-2 font-bold dark:text-white">
                    <span v-if="isEditingInterface">Edit Interface</span>
                    <span v-else>Add Interface</span>
                </div>
                <div class="p-2 space-y-3">

                    <!-- iGeneric interface settings -->
                    <!-- interface name -->
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Name</label>
                        <input type="text" :disabled="isEditingInterface" placeholder="New Interface Name"
                               v-model="newInterfaceName"
                               class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                               :class="[ isEditingInterface ? 'cursor-not-allowed bg-gray-200' : 'bg-gray-50' ]">
                        <div class="text-xs text-gray-600 dark:text-zinc-300">Interface names must be unique.</div>
                    </div>

                    <!-- interface type -->
                    <div class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Type</label>
                        <select v-model="newInterfaceType" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                            <option disabled selected>--</option>
                            <option value="AutoInterface">Auto Interface</option>
                            <option disabled selected>RNodes</option>
                            <option value="RNodeInterface">RNode Interface</option>
                            <option value="RNodeMultiInterface">RNode Multi Interface</option>
                            <option disabled selected>IP Networks</option>
                            <option value="TCPClientInterface">TCP Client Interface</option>
                            <option value="TCPServerInterface">TCP Server Interface</option>
                            <option value="UDPInterface">UDP Interface</option>
                            <option value="I2PInterface">I2P Interface</option>
                            <option disabled selected>Hardware</option>
                            <option value="SerialInterface">Serial Interface</option>
                            <option value="KISSInterface">KISS Interface</option>
                            <option hidden value="AX25KISSInterface">AX.25 KISS Interface</option>
                            <option disabled selected>Other</option>
                            <option value="PipeInterface">Pipe Interface</option>
                        </select>
                        <div class="text-xs text-gray-600 dark:text-zinc-300">
                            Need help? <a class="text-blue-500 underline" href="https://reticulum.network/manual/interfaces.html" target="_blank">Reticulum Docs: Configuring Interfaces</a>
                        </div>
                    </div>

                    <!-- TCPClientInterface -->
                    <!-- interface target host -->
                    <div v-if="newInterfaceType === 'TCPClientInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Target Host</label>
                        <input type="text" placeholder="example.com" v-model="newInterfaceTargetHost" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    </div>

                    <!-- interface target port -->
                    <div v-if="newInterfaceType === 'TCPClientInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Target Port</label>
                        <input type="text" placeholder="1234" v-model="newInterfaceTargetPort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    </div>

                    <!-- TCPServerInterface -->
                    <!-- interface listen ip -->
                    <div v-if="newInterfaceType === 'TCPServerInterface' || newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Listen IP</label>
                        <input type="text" placeholder="0.0.0.0" v-model="newInterfaceListenIp" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    </div>

                    <!-- interface listen port -->
                    <div v-if="newInterfaceType === 'TCPServerInterface' || newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Listen Port</label>
                        <input type="text" placeholder="1234" v-model="newInterfaceListenPort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    </div>

                    <!-- UDPInterface -->
                    <!-- interface forward ip -->
                    <div v-if="newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Forward IP</label>
                        <input type="text" placeholder="255.255.255.255" v-model="newInterfaceForwardIp" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    </div>

                    <!-- interface listen port -->
                    <div v-if="newInterfaceType === 'UDPInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Forward Port</label>
                        <input type="text" placeholder="1234" v-model="newInterfaceForwardPort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    </div>

                    <!-- I2PInterface -->
                    <!-- peers -->
                    <div v-if="newInterfaceType === 'I2PInterface'">
                        <div class="mb-2 text-sm text-gray-500 dark:text-zinc-300">ⓘ To use the I2P interface, you must have an I2P router running on your system. When the I2P Interface is added for the first time Reticulum will generate a new I2P address for the interface and begin listening for inbound traffic.</div>
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Peers</label>
                        <div class="space-y-2">
                            <div v-for="(peer, index) in I2PSettings.newInterfacePeers" :key="index" class="flex items-center space-x-2">
                                <input
                                    type="text"
                                    v-model="I2PSettings.newInterfacePeers[index]"
                                    placeholder="Enter peer address (e.g: 5urvjicpzi7q3ybztsef4i5ow2aq4soktfj7zedz53s47r54jnqq.b32.i2p)"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600"
                                />
                                <button @click="removeI2PPeer(index)" type="button" class="bg-red-500 hover:bg-red-400 text-white text-sm p-2 rounded-lg">Remove</button>
                            </div>
                            <button @click="addI2PPeer('')" type="button" class="bg-green-500 hover:bg-green-400 text-white text-sm px-4 py-2 rounded-lg">Add Peer</button>
                        </div>
                    </div>

                    <!-- RNode interface -->
                    <!-- interface port -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Port</label>
                        <select v-model="newInterfacePort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                            <option v-for="comport of comports" :value="comport.device">{{ comport.device }} (Product: {{ comport.product ?? '?' }}, Serial: {{ comport.serial ?? '?' }})</option>
                        </select>
                    </div>
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2 flex flex-wrap items-start gap-4">

                        <!-- interface Frequency -->
                        <div class="flex-1">
                            <div class="mb-2">
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Frequency</label>
                                <div class="flex items-center gap-2">
                                    <div class="flex flex-col">
                                        <input
                                            type="number"
                                            v-model.number="RNodeGHzValue"
                                            min="0"
                                            placeholder="GHz"
                                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600"
                                        />
                                        <label class="text-xs text-gray-500 dark:text-zinc-400 mt-1 text-center">GHz</label>
                                    </div>
                                    <div class="flex flex-col">
                                        <input
                                            type="number"
                                            v-model.number="RNodeMHzValue"
                                            min="0"
                                            placeholder="MHz"
                                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600"
                                        />
                                        <label class="text-xs text-gray-500 dark:text-zinc-400 mt-1 text-center">MHz</label>
                                    </div>
                                    <div class="flex flex-col">
                                        <input
                                            type="number"
                                            v-model.number="RNodekHzValue"
                                            min="0"
                                            placeholder="kHz"
                                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600"
                                        />
                                        <label class="text-xs text-gray-500 dark:text-zinc-400 mt-1 text-center">kHz</label>
                                    </div>
                                </div>
                                <div class="text-sm text-gray-600 dark:text-zinc-100 mt-2 font-bold">
                                    Selected Frequency: {{ formattedFrequency }}
                                </div>
                            </div>
                        </div>

                        <!-- interface Bandwidth -->
                        <div class="flex-1">
                            <div class="mb-2">
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Bandwidth</label>
                                <select v-model="newInterfaceBandwidth" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                    <option v-for="bandwidth in RNodeInterfaceDefaults.bandwidths" :value="bandwidth">{{ bandwidth / 1000 }} KHz</option>
                                </select>
                            </div>
                        </div>

                    </div>

                    <!-- interface txpower -->
                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Transmit Power (dBm)</label>
                        <input v-model="newInterfaceTxpower" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                    </div>

                    <div v-if="newInterfaceType === 'RNodeInterface'" class="mb-2 flex flex-wrap items-start gap-4">

                        <!-- interface spreading factor -->
                        <div class="flex-1">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Spreading Factor</label>
                            <select v-model="newInterfaceSpreadingFactor" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                <option v-for="spreadingfactor in RNodeInterfaceDefaults.spreadingfactors" :value="spreadingfactor">{{ spreadingfactor }}</option>
                            </select>
                        </div>

                        <!-- interface coding rate -->
                        <div class="flex-1">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Coding Rate</label>
                            <select v-model="newInterfaceCodingRate" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                <option v-for="codingrate in RNodeInterfaceDefaults.codingrates" :value="codingrate">{{ codingrate }}</option>
                            </select>
                        </div>

                    </div>

                    <!-- RNodeMultiInterface -->
                    <div v-if="newInterfaceType === 'RNodeMultiInterface'" class="mb-2">
                        <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">ⓘ The RNode Multi Interface is used for custom devices with multiple LoRa transceivers such as the openCom XL.</p>
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Port</label>
                        <select v-model="newInterfacePort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                            <option v-for="comport of comports" :value="comport.device">{{ comport.device }} (Product: {{ comport.product ?? '?' }}, Serial: {{ comport.serial ?? '?' }})</option>
                        </select>
                    </div>

                    <!-- RNodeMultiInterface: Sub Interfaces -->
                    <div v-if="newInterfaceType === 'RNodeMultiInterface'" class="mb-2">
                        <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Sub-Interfaces</label>
                        <div class="space-y-3">
                            <div :key="idx" v-for="(sub, idx) in RNodeMultiInterface.subInterfaces" class="p-2 space-y-2 border border-gray-200 rounded-lg dark:border-zinc-700">

                                <input
                                    v-model="sub.name"
                                    type="text"
                                    placeholder="Sub-Interface Name"
                                    class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">

                                <div class="flex gap-2">
                                    <div class="flex-1">
                                        <label class="text-sm dark:text-zinc-100">Frequency (Hz)</label>
                                        <input
                                            v-model.number="sub.frequency"
                                            type="number"
                                            class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                                    </div>
                                    <div class="flex-1">
                                        <label class="text-sm dark:text-zinc-100">Bandwidth</label>
                                        <select v-model="sub.bandwidth" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                            <option v-for="bandwidth in RNodeInterfaceDefaults.bandwidths" :value="bandwidth">{{ bandwidth / 1000 }} KHz</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="flex gap-2">
                                    <div class="flex-1">
                                        <label class="text-sm dark:text-zinc-100">Spreading Factor</label>
                                        <select v-model.number="sub.spreadingfactor" class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                                            <option :key="sf" v-for="sf in RNodeInterfaceDefaults.spreadingfactors" :value="sf">{{ sf }}</option>
                                        </select>
                                    </div>
                                    <div class="flex-1">
                                        <label class="text-sm dark:text-zinc-100">Coding Rate</label>
                                        <select v-model.number="sub.codingrate" class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                                            <option :key="cr" v-for="cr in RNodeInterfaceDefaults.codingrates" :value="cr">{{ cr }}</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="flex gap-2 items-center">
                                    <div class="flex-1">
                                        <label class="text-sm dark:text-zinc-100">TX Power (dBm)</label>
                                        <input
                                            v-model.number="sub.txpower"
                                            type="number"
                                            class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                                    </div>
                                    <div class="flex-1">
                                        <label class="text-sm dark:text-zinc-100">Virtual Port</label>
                                        <input
                                            v-model.number="sub.vport"
                                            type="number"
                                            class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                                    </div>
                                </div>

                                <button @click="removeSubInterface(idx)" type="button" class="bg-red-500 hover:bg-red-400 text-white text-sm p-2 rounded-lg">Remove Sub-Interface</button>

                            </div>
                            <button @click="addSubInterface" type="button" class="bg-green-500 hover:bg-green-400 text-white text-sm px-4 py-2 rounded-lg">Add Sub-Interface</button>
                        </div>
                    </div>

                    <!-- Serial, KISS, and AX25Kiss -->
                    <div v-if="['SerialInterface', 'KISSInterface', 'AX25KISSInterface'].includes(newInterfaceType)" class="mb-4">

                        <div class="mb-2">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Port</label>
                            <select v-model="newInterfacePort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                <option v-for="comport of comports" :value="comport.device">{{ comport.device }} (Product: {{ comport.product ?? '?' }}, Serial: {{ comport.serial ?? '?' }})</option>
                            </select>
                        </div>

                        <div class="mb-2">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Serial connection baud rate (bps)</label>
                            <input v-model="newInterfaceSpeed" placeholder="115200" type="number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                        </div>

                        <div class="mb-2">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Databits</label>
                            <input v-model="newInterfaceDatabits" type="number" placeholder="8" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                        </div>

                        <div class="mb-2">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Parity </label>
                            <input v-model="newInterfaceParity" type="number" placeholder="" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                        </div>

                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Stopbits</label>
                            <input v-model="newInterfaceStopbits" type="number" placeholder="1" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                        </div>

                    </div>

                    <!-- KISS and AX.25 KISS -->
                    <div v-if="['KISSInterface', 'AX25KISSInterface'].includes(newInterfaceType)" class="mb-4">

                        <div class="flex items-center mb-2">
                            <input
                                id="use-ax25"
                                type="checkbox"
                                :checked="newInterfaceType === 'AX25KISSInterface'"
                                @click="useKISSAX25"
                                class="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring focus:ring-blue-500 dark:border-zinc-600 dark:bg-zinc-800 dark:focus:ring-blue-600"
                            />
                            <label for="use-ax25" class="ml-2 text-sm font-medium text-gray-900 dark:text-zinc-100">Enable AX.25 Framing</label>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Preamble (milliseconds)</label>
                                <input
                                    v-model="this.newInterfacePreamble"
                                    type="number"
                                    placeholder="150"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div>
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">TX Tail (milliseconds)</label>
                                <input
                                    v-model="this.newInterfaceTXTail"
                                    type="number"
                                    placeholder="10"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div>
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">CDMA Persistence (milliseconds)</label>
                                <input
                                    v-model="this.newInterfacePersistence"
                                    type="number"
                                    placeholder="200"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div>
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">CDMA Slot Time (milliseconds)</label>
                                <input
                                    v-model="this.newInterfaceSlotTime"
                                    type="number"
                                    placeholder="20"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>

                        <div class="flex items-center space-x-4 mt-4">
                            <div class="flex-1">
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">SSID</label>
                                <input
                                    type="text"
                                    value="0"
                                    v-model="newInterfaceSSID"
                                    placeholder="Enter SSID"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Callsign</label>
                                <input
                                    type="text"
                                    v-model="newInterfaceCallsign"
                                    placeholder="Enter callsign"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Callsign ID Interval</label>
                                <input
                                    type="number"
                                    v-model="newInterfaceIDInterval"
                                    placeholder="Enter interval (seconds)"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>

                    </div>

                    <!-- Pipe Interface -->
                    <div v-if="newInterfaceType === 'PipeInterface'" class="mb-2">

                        <div class="text-sm text-gray-500 dark:text-zinc-300 mb-3">ⓘ Using this interface, Reticulum can use any program as an interface via stdin and stdout. This can be usedto easily create virtual interfaces, or to interface with custom hardware or other systems.</div>

                        <div class="mb-2">
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Command</label>
                            <input type="text" placeholder="netcat -l 5757" v-model="newInterfaceCommand" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                        </div>

                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-900 dark:text-zinc-100">Respawn Delay (seconds)</label>
                            <input type="number" placeholder="5" v-model="newInterfaceRespawnDelay" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                        </div>

                    </div>

                </div>
            </div>

            <!-- RNodeInterface bitrate & link budget -->
            <ExpandingSection v-if="newInterfaceType === 'RNodeInterface'">
                <template v-slot:title>Calculated On-Air RNode Bitrate & Link Budget</template>
                <template v-slot:content>
                    <div class="p-2 space-y-3">

                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-800 dark:text-white">Antenna Gain (dBi)</label>
                            <input
                                type="number"
                                v-model.number="RNodeInterfaceLoRaParameters.antennaGain"
                                placeholder="Enter gain"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                            />
                            <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">ⓘ A stub or PCB antenna might have around 1 dBi of gain, where a directional Yagi might have 5 dBi of gain.</p>
                        </div>

                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-800 dark:text-white">On-Air Calculations</label>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 text-center">
                                <div class="bg-gray-100 p-3 rounded-lg border dark:bg-zinc-800">
                                    <div class="text-sm font-medium text-gray-700 dark:text-gray-300">Sensitivity</div>
                                    <div class="text-xl font-bold text-gray-900 dark:text-white">{{ RNodeInterfaceLoRaParameters.sensitivity ?? "???" }}</div>
                                </div>
                                <div class="bg-gray-100 p-3 rounded-lg border dark:bg-zinc-800">
                                    <div class="text-sm font-medium text-gray-700 dark:text-gray-300">Data Rate</div>
                                    <div class="text-xl font-bold text-gray-900 dark:text-white">{{ RNodeInterfaceLoRaParameters.dataRate ?? "???" }}</div>
                                </div>
                                <div class="bg-gray-100 p-3 rounded-lg border dark:bg-zinc-800">
                                    <div class="text-sm font-medium text-gray-700 dark:text-gray-300">Link Budget</div>
                                    <div class="text-xl font-bold text-gray-900 dark:text-white">{{ RNodeInterfaceLoRaParameters.linkBudget ?? "???" }}</div>
                                </div>
                            </div>
                        </div>

                    </div>
                </template>
            </ExpandingSection>

            <!-- optional AutoInterface settings -->
            <ExpandingSection v-if="newInterfaceType === 'AutoInterface'">
                <template v-slot:title>Optional AutoInterface Settings</template>
                <template v-slot:content>
                    <div class="p-2 space-y-3">

                        <div class="flex-1">
                            <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Group ID</label>
                            <input
                                type="text"
                                v-model="newInterfaceGroupID"
                                placeholder="reticulum"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                            />
                        </div>

                        <div class="flex-1">
                            <label class="text-sm dark:text-zinc-100">Multicast Address Type</label>
                            <select v-model="newInterfaceMulticastAddressType" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                <option value="permanent">Permanent</option>
                                <option value="temporary">Temporary</option>
                            </select>
                        </div>

                        <div class="flex items-center space-x-4 mt-4">
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Network devices</label>
                                <input
                                    type="text"
                                    v-model="newInterfaceDevices"
                                    placeholder="wlan0,eth1"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Ignored Devices</label>
                                <input
                                    type="text"
                                    v-model="newInterfaceIgnoredDevices"
                                    placeholder="tun0,eth0"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>

                        <div class="flex items-center space-x-4 mt-4">
                            <div class="flex-1">
                                <label class="text-sm dark:text-zinc-100">Discovery Scope</label>
                                <select v-model="newInterfaceDiscoveryScope" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                    <option value="global">Global</option>
                                    <option value="admin">Admin</option>
                                    <option value="organisation">Organisation</option>
                                    <option value="site">Site</option>
                                    <option value="link">Link</option>
                                </select>
                            </div>
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Discovery Port</label>
                                <input
                                    type="number"
                                    v-model="newInterfaceDiscoveryPort"
                                    placeholder="48555"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Data Port</label>
                                <input
                                    type="number"
                                    v-model="newInterfaceDataPort"
                                    placeholder="49555"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>

                    </div>
                </template>
            </ExpandingSection>

            <!-- optional TCPClientInterface settings -->
            <ExpandingSection v-if="newInterfaceType === 'TCPClientInterface'">
                <template v-slot:title>Optional TCPClientInterface Settings</template>
                <template v-slot:content>
                    <div class="p-2 space-y-3">

                        <div class="flex">
                            <div class="flex flex-col mr-auto">
                                <label for="kiss-framing" class="text-sm font-medium text-gray-900 dark:text-zinc-100">Enable KISS Framing</label>
                                <span class="text-sm text-gray-500 dark:text-zinc-300">Enable this when connecting to software that uses KISS framing such as packet radio sound modems. For KISS connections through serial hardware select "KISS Interface" as the interface type.</span>
                            </div>
                            <input id="kiss-framing" type="checkbox" v-model="newInterfaceKISSFramingEnabled" class="my-auto mx-2 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring focus:ring-blue-500 dark:border-zinc-600 dark:bg-zinc-800 dark:focus:ring-blue-600"/>
                        </div>

                        <div class="flex">
                            <div class="flex flex-col mr-auto">
                                <label for="i2p-tunneled" class="text-sm font-medium text-gray-900 dark:text-zinc-100">Enable I2P tunneling</label>
                                <span class="text-sm text-gray-500 dark:text-zinc-300">Enables tunnelling through an I2P Connection using the TCPClientInterface</span>
                            </div>
                            <input id="i2p-tunneled" type="checkbox" v-model="newInterfaceI2PTunnelingEnabled" class="my-auto mx-2 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring focus:ring-blue-500 dark:border-zinc-600 dark:bg-zinc-800 dark:focus:ring-blue-600"/>
                        </div>

                    </div>
                </template>
            </ExpandingSection>

            <!-- optional TCPClientInterface and UDPInterface settings -->
            <ExpandingSection v-if="newInterfaceType === 'TCPServerInterface' || newInterfaceType === 'UDPInterface'">
                <template v-slot:title>Optional {{ newInterfaceType }} settings</template>
                <template v-slot:content>
                    <div class="p-2 space-y-3">

                        <div>
                            <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Network device</label>
                            <span class="text-sm text-gray-500 dark:text-zinc-300">Binds the interface to a specific network interface</span>
                            <input type="text" placeholder="e.g: eth0" v-model="newInterfaceNetworkDevice" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                        </div>

                        <div class="flex items-start">
                            <div class="flex flex-col mr-auto">
                                <label for="prefer-ipv6" class="text-sm font-medium text-gray-900 dark:text-zinc-100">Prefer IPv6</label>
                                <span class="text-sm text-gray-500 dark:text-zinc-300">Binds the TCP Server Interface to an IPv6 address</span>
                            </div>
                            <input
                                id="prefer-ipv6"
                                type="checkbox"
                                value="1"
                                v-model="newInterfacePreferIPV6"
                                class="my-auto mx-2 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring focus:ring-blue-500 dark:border-zinc-600 dark:bg-zinc-800 dark:focus:ring-blue-600"
                            />
                        </div>

                    </div>
                </template>
            </ExpandingSection>

            <!-- optional RNodeInterface settings -->
            <ExpandingSection v-if="newInterfaceType === 'RNodeInterface'">
                <template v-slot:title>Optional RNodeInterface Settings</template>
                <template v-slot:content>
                    <div class="p-2 space-y-3">

                        <div class="flex items-center space-x-4">
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Callsign</label>
                                <input
                                    type="text"
                                    v-model="newInterfaceCallsign"
                                    placeholder="Enter callsign"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Callsign ID Interval</label>
                                <input
                                    type="number"
                                    v-model="newInterfaceIDInterval"
                                    placeholder="Enter interval (seconds)"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>

                        <div class="flex items-center space-x-4">
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Airtime Limit (Short)</label>
                                <input
                                    type="number"
                                    v-model="newInterfaceAirtimeLimitShort"
                                    placeholder="Enter short airtime limit (seconds)"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Airtime Limit (Long)</label>
                                <input
                                    type="number"
                                    v-model="newInterfaceAirtimeLimitLong"
                                    placeholder="Enter long airtime limit (seconds)"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>

                    </div>
                </template>
            </ExpandingSection>

            <!-- common interface settings -->
            <ExpandingSection>
                <template v-slot:title>Common Interface Settings</template>
                <template v-slot:content>
                    <div class="p-2 space-y-3">

                        <div v-show="transportEnabled">
                            <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Interface Mode</label>
                            <select v-model="sharedInterfaceSettings.mode" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white">
                                <option value="full">Full</option>
                                <option value="gateway">Gateway</option>
                                <option value="access_point">Access Point</option>
                                <option value="roaming">Roaming</option>
                                <option value="boundary">Boundary</option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Inferred Interface Bitrate</label>
                            <input
                                v-model="sharedInterfaceSettings.bitrate"
                                type="number"
                                placeholder="Enter inferred bitrate"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                            />
                        </div>

                    </div>
                </template>
            </ExpandingSection>

            <!-- ifac settings -->
            <ExpandingSection>
                <template v-slot:title>IFAC Settings</template>
                <template v-slot:subtitle>Interface Access Code settings are used for creating private networks and can be configured on the interface level.</template>
                <template v-slot:content>
                    <div class="p-2">
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-y-2 lg:gap-x-2">
                            <div>
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Network Name</label>
                                <input
                                    v-model="sharedInterfaceSettings.network_name"
                                    type="text"
                                    placeholder="Enter network name"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">Passphrase</label>
                                <input
                                    v-model="sharedInterfaceSettings.passphrase"
                                    type="text"
                                    placeholder="Enter passphrase"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-900 dark:text-zinc-100">IFAC Size</label>
                                <input
                                    v-model="sharedInterfaceSettings.ifac_size"
                                    type="number"
                                    min="8"
                                    max="512"
                                    placeholder="Enter size (8-512)"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white"
                                />
                            </div>
                        </div>
                    </div>
                </template>
            </ExpandingSection>

            <!-- add/save interface button -->
            <div class="p-2 bg-white rounded shadow divide-y divide-gray-200 dark:bg-zinc-900">
                <button @click="addInterface" type="button" class="bg-green-500 hover:bg-green-400 focus-visible:outline-green-500 my-auto inline-flex items-center gap-x-1 rounded-md p-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                    <span v-if="isEditingInterface">Save Interface</span>
                    <span v-else>Add Interface</span>
                </button>
            </div>

        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import DialogUtils from "../../js/DialogUtils";
import ExpandingSection from "./ExpandingSection.vue";

export default {
    name: 'AddInterfacePage',
    components: {
        ExpandingSection,
    },
    data() {
        return {

            isEditingInterface: false,
            showAllSettings: false, // more interface settings, used for TCPInterface and RNodeInterface

            appInfo: null,
            transportEnabled: false,

            config: null,

            comports: [],

            newInterfaceName: null,
            newInterfaceType: null,

            newInterfaceGroupID: null,
            newInterfaceMulticastAddressType: null,
            newInterfaceDevices: null,
            newInterfaceIgnoredDevices: null,
            newInterfaceDiscoveryScope: null,
            newInterfaceDiscoveryPort: null,
            newInterfaceDataPort: null,

            newInterfaceTargetHost: null,
            newInterfaceTargetPort: null,

            newInterfaceListenIp: null,
            newInterfaceListenPort: null,
            newInterfaceNetworkDevice: null,
            newInterfacePreferIPV6: null,
            newInterfaceKISSFramingEnabled: null,
            newInterfaceI2PTunnelingEnabled: null,

            sharedInterfaceSettings: {
                "mode": null,
                "network_name": null,
                "passphrase": null,
                "ifac_size": null,
            },

            newInterfaceForwardIp: null,
            newInterfaceForwardPort: null,

            I2PSettings: {
                showPeerAccordion: false,
                newInterfacePeers: [],
            },

            RNodeMultiInterface: {
                port: null,
                subInterfaces: [],
            },

            newInterfacePort: null,
            RNodeGHzValue: 0,
            RNodeMHzValue: 0,
            RNodekHzValue: 0,
            newInterfaceFrequency: null,
            newInterfaceBandwidth: null,
            newInterfaceTxpower: null,
            newInterfaceSpreadingFactor: null,
            newInterfaceCodingRate: null,

            // Serial, KISS, and AX25KISS options
            newInterfaceSpeed: null,
            newInterfaceDatabits: null,
            newInterfaceParity: null,
            newInterfaceStopbits: null,

            // KISS and AX25KISS
            newInterfacePreamble: null,
            newInterfaceTXTail: null,
            newInterfacePersistence: null,
            newInterfaceSlotTime: null,

            // RNode and KISS
            newInterfaceCallsign: null,
            newInterfaceIDInterval: null,
            newInterfaceFlowControl: null,
            newInterfaceAirtimeLimitLong: null,
            newInterfaceAirtimeLimitShort: null,

            // Pipe interface
            newInterfaceCommand: null,
            newInterfaceRespawnDelay: null,

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

            RNodeInterfaceLoRaParameters: {
                antennaGain: 0,
                noiseFloor: 5,
                sensitivity: null,
                dataRate: null,
                linkBudget: null,
            },

        };
    },
    computed: {
        formattedFrequency() {
            const totalHz = this.calculateFrequencyInHz();
            if(totalHz >= 1e9){
                return `${(totalHz / 1e9).toFixed(3)} GHz`;
            } else if(totalHz >= 1e6) {
                return `${(totalHz / 1e6).toFixed(3)} MHz`;
            } else if(totalHz >= 1e3) {
                return `${(totalHz / 1e3).toFixed(3)} kHz`;
            }
            return `${totalHz} Hz`;
        },
    },
    watch: {
        newInterfaceBandwidth: "updateRNodeCalculations",
        newInterfaceSpreadingFactor: "updateRNodeCalculations",
        newInterfaceCodingRate: "updateRNodeCalculations",
        newInterfaceTxpower: "updateRNodeCalculations",
        'RNodeInterfaceLoRaParameters.antennaGain': "updateRNodeCalculations",
    },
    mounted() {

        this.getAppInfo();
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
            } catch (e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        async updateConfig(config) {
            try {
                const response = await window.axios.patch("/api/v1/config", config);
                this.config = response.data.config;
            } catch (e) {
                alert("Failed to save config!");
                console.log(e);
            }
        },
        async loadComports() {
            try {
                const response = await window.axios.get(`/api/v1/comports`);
                this.comports = response.data.comports;
            } catch (e) {
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
                if (!iface) {
                    DialogUtils.alert("The selected interface for editing could not be found.");
                    this.$router.push({
                        "name": "interfaces",
                    });
                    return;
                }

                // set form values
                this.newInterfaceName = interfaceName;
                this.newInterfaceType = iface.type;

                // AutoInterface additional settings
                this.newInterfaceGroupID = iface.group_id;
                this.newInterfaceMulticastAddressType = iface.multicast_address_type;
                this.newInterfaceDevices = iface.devices;
                this.newInterfaceIgnoredDevices = iface.ignored_devices;
                this.newInterfaceDiscoveryScope = iface.discovery_scope;
                this.newInterfaceDiscoveryPort = iface.discovery_port;
                this.newInterfaceDataPort = iface.data_port;

                // tcp client interface
                this.newInterfaceTargetHost = iface.target_host;
                this.newInterfaceTargetPort = iface.target_port;

                if (iface.kiss_framing) {
                    this.newInterfaceKISSFramingEnabled = true;
                }
                if (iface.i2p_tunneled) {
                    this.newInterfaceI2PTunnelingEnabled = true;
                }
                if (iface.prefer_ipv6) {
                    this.newInterfacePreferIPV6 = true;
                }


                // tcp server interface & udp interface
                this.newInterfaceNetworkDevice = iface.device;
                this.newInterfaceListenIp = iface.listen_ip;
                this.newInterfaceListenPort = iface.listen_port;

                // I2P Interface
                if(iface.peers){
                    const peersToAdd = iface.peers.split(',');
                    for(const address of peersToAdd){
                        this.addI2PPeer(address);
                    }
                }

                // udp interface
                this.newInterfaceForwardIp = iface.forward_ip;
                this.newInterfaceForwardPort = iface.forward_port;

                // Port (For RNode, Serial, and KISS)
                this.newInterfacePort = iface.port;

                // RNode Interface
                this.newInterfaceFrequency = iface.frequency;
                this.RNodeGHzValue = Math.floor(iface.frequency / 1e9);
                this.RNodeMHzValue = Math.floor((iface.frequency % 1e9) / 1e6);
                this.RNodekHzValue = Math.floor((iface.frequency % 1e6) / 1e3);
                this.newInterfaceBandwidth = iface.bandwidth;
                this.newInterfaceTxpower = iface.txpower;
                this.newInterfaceSpreadingFactor = iface.spreadingfactor;
                this.newInterfaceCodingRate = iface.codingrate;

                // RNode Multi Interface
                this.RNodeMultiInterface.subInterfaces = iface.sub_interfaces;

                // Serial, KISS, and AX25KISS
                this.newInterfaceSpeed = iface.speed;
                this.newInterfaceDatabits = iface.databits;
                this.newInterfaceParity = iface.parity;
                this.newInterfaceStopbits = iface.stopbits;

                this.newInterfacePreamble = iface.preamble;
                this.newInterfaceTXTail = iface.txtail;
                this.newInterfacePersistence = iface.persistence;
                this.newInterfaceSlotTime = iface.slottime;

                this.newInterfaceCallsign = iface.callsign;
                this.newInterfaceIDInterval = iface.id_interval;
                this.newInterfaceSSID = iface.ssid;

                // Airtime limit
                this.newInterfaceAirtimeLimitLong = iface.airtime_limit_long;
                this.newInterfaceAirtimeLimitShort = iface.airtime_limit_short;

                // Pipe Interface
                this.newInterfaceCommand = iface.command;
                this.newInterfaceRespawnDelay = iface.respawn_delay;

                // Shared interface settings
                this.sharedInterfaceSettings.mode = iface.mode;
                this.sharedInterfaceSettings.bitrate = iface.bitrate;
                this.sharedInterfaceSettings.network_name = iface.network_name;
                this.sharedInterfaceSettings.passphrase = iface.passphrase;
                this.sharedInterfaceSettings.ifac_size = iface.ifac_size;

            } catch (e) {
                // do nothing if failed to load interfaces
            }
        },
        async addInterface() {
            try {
                let subInterfacesData = null;
                if(this.newInterfaceType === 'RNodeMultiInterface'){
                    subInterfacesData = this.RNodeMultiInterface.subInterfaces.map(s => ({
                        name: s.name,
                        frequency: s.frequency,
                        bandwidth: s.bandwidth,
                        txpower: s.txpower,
                        spreadingfactor: s.spreadingfactor,
                        codingrate: s.codingrate,
                        vport: s.vport
                    }));
                }
                // add interface
                const response = await window.axios.post(`/api/v1/reticulum/interfaces/add`, {

                    allow_overwriting_interface: this.isEditingInterface,

                    // required values
                    name: this.newInterfaceName,
                    type: this.newInterfaceType,

                    // AutoInterface
                    group_id: this.newInterfaceGroupID,
                    multicast_address_type: this.newInterfaceMulticastAddressType,
                    devices: this.newInterfaceDevices,
                    ignored_devices: this.newInterfaceIgnoredDevices,
                    discovery_scope: this.newInterfaceDiscoveryScope,
                    discovery_port:  this.newInterfaceDiscoveryPort,
                    data_port:       this.newInterfaceDataPort,

                    // tcp client interface
                    target_host: this.newInterfaceTargetHost,
                    target_port: this.newInterfaceTargetPort,

                    // TCP Client & Server interface
                    kiss_framing: this.newInterfaceKISSFramingEnabled,
                    i2p_tunneled: this.newInterfaceI2PTunnelingEnabled,

                    // tcp server interface & udp interface
                    listen_ip: this.newInterfaceListenIp,
                    listen_port: this.newInterfaceListenPort,
                    device: this.newInterfaceNetworkDevice,
                    prefer_ipv6: this.newInterfacePreferIPV6,

                    // udp interface
                    forward_ip: this.newInterfaceForwardIp,
                    forward_port: this.newInterfaceForwardPort,

                    //  I2P Interface
                    peers: this.I2PSettings.newInterfacePeers.join(','),

                    // rnode interface
                    port: this.newInterfacePort,
                    frequency: this.calculateFrequencyInHz(),
                    bandwidth: this.newInterfaceBandwidth,
                    txpower: this.newInterfaceTxpower,
                    spreadingfactor: this.newInterfaceSpreadingFactor,
                    codingrate: this.newInterfaceCodingRate,

                    // RNode Multi Interface
                    sub_interfaces: subInterfacesData,

                    // Seiral, KISS, and AX25KISS
                    speed: this.newInterfaceSpeed,
                    databits: this.newInterfaceDatabits,
                    parity: this.newInterfaceParity,
                    stopbits: this.newInterfaceStopbits,

                    // KISS and AX25KISS
                    preamble: this.newInterfacePreamble,
                    txtail: this.newInterfaceTXTail,
                    persistence: this.newInterfacePersistence,
                    slottime: this.newInterfaceSlotTime,

                    callsign: this.newInterfaceCallsign,
                    id_interval: this.newInterfaceIDInterval,
                    ssid: this.newInterfaceSSID,

                    // Pipe interface
                    command: this.newInterfaceCommand,
                    respawn_delay: this.newInterfaceRespawnDelay,

                    // Airtime limit
                    airtime_limit_long: this.newInterfaceAirtimeLimitLong,
                    airtime_limit_short: this.newInterfaceAirtimeLimitShort,

                    // Shared interface settings
                    mode: this.sharedInterfaceSettings.mode,
                    bitrate: this.sharedInterfaceSettings.bitrate,
                    network_name: this.sharedInterfaceSettings.network_name,
                    passphrase: this.sharedInterfaceSettings.passphrase,
                    ifac_size: this.sharedInterfaceSettings.ifac_size,

                });

                // show success message
                if(response.data.message){
                    DialogUtils.alert(response.data.message);
                }

                // go to interfaces page
                this.$router.push({
                    name: "interfaces",
                });

            } catch (e) {
                const message = e.response?.data?.message ?? "failed to add interface";
                DialogUtils.alert(message);
                console.log(e);
            }

        },
        formatFrequency(hz) {
            return Utils.formatFrequency(hz);
        },
        calculateFrequencyInHz() {
            const ghzToHz = this.RNodeGHzValue * 1e9;
            const mhzToHz = this.RNodeMHzValue * 1e6;
            const khzToHz = this.RNodekHzValue * 1e3;
            return ghzToHz + mhzToHz + khzToHz;
        },
        updateRNodeCalculations() {
            this.calculateRNodeParameters(
                this.newInterfaceBandwidth,
                this.newInterfaceSpreadingFactor,
                this.newInterfaceCodingRate,
                this.RNodeInterfaceLoRaParameters.noiseFloor,
                this.RNodeInterfaceLoRaParameters.antennaGain,
                this.newInterfaceTxpower
            );
        },
        calculateRNodeParameters(bandwidth, spreadingFactor, codingRate, noiseFloor, antennaGain, transmitPower) {

            // https://unsigned.io/understanding-lora-parameters/
            // "SX1272/3/6/7/8 LoRa Modem Design Guide" https://www.openhacks.com/uploadsproductos/loradesignguide_std.pdf
            // 4:5 - 4:8
            const crn = {
                5: 1,
                6: 2,
                7: 3,
                8: 4,
            };

            codingRate = crn[codingRate];

            const sfn = {
                5: -2.5,
                6: -5,
                7: -7.5,
                8: -10,
                9: -12.5,
                10: -15,
                11: -17.5,
                12: -20
            };

            let dataRate = spreadingFactor * ((4 / (4 + codingRate)) / (Math.pow(2, spreadingFactor) / (bandwidth / 1000))) * 1000;

            let sensitivity = -174 + 10 * Math.log10(bandwidth) + noiseFloor + (sfn[spreadingFactor] || 0);

            if(bandwidth === 203125 || bandwidth === 406250 || bandwidth > 500000){
                sensitivity = -165.6 + 10 * Math.log10(bandwidth) + noiseFloor + (sfn[spreadingFactor] || 0);
            }

            let linkBudget = (transmitPower - sensitivity) + antennaGain;
            this.RNodeInterfaceLoRaParameters.dataRate = dataRate < 1000
                ? `${dataRate.toFixed(0)} bps`
                : `${(dataRate / 1000).toFixed(2)} kbps`;
            this.RNodeInterfaceLoRaParameters.linkBudget = `${linkBudget.toFixed(1)} dB`;
            this.RNodeInterfaceLoRaParameters.sensitivity = `${sensitivity.toFixed(1)} dBm`;

        },
        toggleI2PPeerAccordion() {
            this.I2PSettings.showPeerAccordion = !this.I2PSettings.showPeerAccordion;
        },
        addI2PPeer(address = "") {
            this.I2PSettings.newInterfacePeers.push(address);
        },
        removeI2PPeer(index) {
            this.I2PSettings.newInterfacePeers.splice(index, 1);
        },
        toggleAllSettings() {
            this.showAllSettings = !this.showAllSettings;
        },
        addSubInterface() {
            this.RNodeMultiInterface.subInterfaces.push({
                name: '',
                frequency: null,
                bandwidth: null,
                txpower: null,
                spreadingfactor: null,
                codingrate: null,
                vport: null,
            });
        },
        useKISSAX25() {
            if(this.newInterfaceType === 'AX25KISSInterface'){
                this.newInterfaceType = "KISSInterface";
            } else {
                this.newInterfaceType = 'AX25KISSInterface';
            }
        },
        removeSubInterface(idx) {
            this.RNodeMultiInterface.subInterfaces.splice(idx, 1);
        },
        async getAppInfo() {
            try {
                const response = await window.axios.get("/api/v1/app/info");
                this.appInfo = response.data.app_info;
                this.transportEnabled = this.appInfo.is_transport_enabled;
            } catch (e) {
                console.log(e);
            }
        },
    },
}
</script>
