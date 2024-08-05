<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">

        <!-- interfaces tab -->
        <div v-if="tab === 'interfaces'" class="overflow-y-auto p-2 space-y-2">

            <!-- warning -->
            <div class="flex bg-orange-500 p-2 text-sm font-semibold leading-6 text-white rounded shadow">
                <div class="my-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                    </svg>
                </div>
                <div class="ml-2 my-auto">Reticulum MeshChat must be restarted for any interface changes to take effect.</div>
                <button v-if="isElectron" @click="relaunch" type="button" class="ml-auto my-auto inline-flex items-center gap-x-1 rounded-md bg-white px-2 py-1 text-sm font-semibold text-black shadow-sm hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white">
                    <span>Restart Now</span>
                </button>
            </div>

            <button @click="showAddInterfaceForm" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
                <span>Add Interface</span>
            </button>

            <!-- interface list -->
            <div v-for="iface of interfacesWithStats" class="border rounded bg-white shadow overflow-hidden">

                <!-- IFAC info -->
                <div v-if="iface._stats?.ifac_signature != null" class="bg-gray-50 p-1 text-sm text-gray-500 space-x-1 border-b">
                    <div class="flex text-sm">
                        <div class="my-auto">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-4 text-green-500">
                                <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <span class="ml-1 my-auto">
                        <span class="text-green-500">{{ iface._stats.ifac_size * 8 }}-bit IFAC</span> with sig <span @click="onIFACSignatureClick(iface._stats.ifac_signature)" class="cursor-pointer">&lt;{{ iface._stats.ifac_signature.slice(0, 6) }}...{{ iface._stats.ifac_signature.slice(-6) }}&gt;</span>
                    </span>
                    </div>
                </div>

                <div class="flex py-2">

                    <!-- icon -->
                    <div class="my-auto mx-2">

                        <svg v-if="iface.type === 'AutoInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="size-6">
                            <path d="M219.31,108.68l-80-80a16,16,0,0,0-22.62,0l-80,80A15.87,15.87,0,0,0,32,120v96a8,8,0,0,0,8,8h64a8,8,0,0,0,8-8V160h32v56a8,8,0,0,0,8,8h64a8,8,0,0,0,8-8V120A15.87,15.87,0,0,0,219.31,108.68ZM208,208H160V152a8,8,0,0,0-8-8H104a8,8,0,0,0-8,8v56H48V120l80-80,80,80Z"></path>
                        </svg>

                        <svg v-else-if="iface.type === 'RNodeInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="size-6">
                            <path d="M128,88a40,40,0,1,0,40,40A40,40,0,0,0,128,88Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,152Zm73.71,7.14a80,80,0,0,1-14.08,22.2,8,8,0,0,1-11.92-10.67,63.95,63.95,0,0,0,0-85.33,8,8,0,1,1,11.92-10.67,80.08,80.08,0,0,1,14.08,84.47ZM69,103.09a64,64,0,0,0,11.26,67.58,8,8,0,0,1-11.92,10.67,79.93,79.93,0,0,1,0-106.67A8,8,0,1,1,80.29,85.34,63.77,63.77,0,0,0,69,103.09ZM248,128a119.58,119.58,0,0,1-34.29,84,8,8,0,1,1-11.42-11.2,103.9,103.9,0,0,0,0-145.56A8,8,0,1,1,213.71,44,119.58,119.58,0,0,1,248,128ZM53.71,200.78A8,8,0,1,1,42.29,212a119.87,119.87,0,0,1,0-168,8,8,0,1,1,11.42,11.2,103.9,103.9,0,0,0,0,145.56Z"></path>
                        </svg>

                        <svg v-else-if="iface.type === 'TCPClientInterface' || iface.type === 'TCPServerInterface' || iface.type === 'UDPInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="size-6">
                            <path d="M128,24h0A104,104,0,1,0,232,128,104.12,104.12,0,0,0,128,24Zm88,104a87.61,87.61,0,0,1-3.33,24H174.16a157.44,157.44,0,0,0,0-48h38.51A87.61,87.61,0,0,1,216,128ZM102,168H154a115.11,115.11,0,0,1-26,45A115.27,115.27,0,0,1,102,168Zm-3.9-16a140.84,140.84,0,0,1,0-48h59.88a140.84,140.84,0,0,1,0,48ZM40,128a87.61,87.61,0,0,1,3.33-24H81.84a157.44,157.44,0,0,0,0,48H43.33A87.61,87.61,0,0,1,40,128ZM154,88H102a115.11,115.11,0,0,1,26-45A115.27,115.27,0,0,1,154,88Zm52.33,0H170.71a135.28,135.28,0,0,0-22.3-45.6A88.29,88.29,0,0,1,206.37,88ZM107.59,42.4A135.28,135.28,0,0,0,85.29,88H49.63A88.29,88.29,0,0,1,107.59,42.4ZM49.63,168H85.29a135.28,135.28,0,0,0,22.3,45.6A88.29,88.29,0,0,1,49.63,168Zm98.78,45.6a135.28,135.28,0,0,0,22.3-45.6h35.66A88.29,88.29,0,0,1,148.41,213.6Z"></path>
                        </svg>

                        <svg v-else-if="iface.type === 'SerialInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="size-6">
                            <path d="M252.44,121.34l-48-32A8,8,0,0,0,192,96v24H72V72h33a32,32,0,1,0,0-16H72A16,16,0,0,0,56,72v48H8a8,8,0,0,0,0,16H56v48a16,16,0,0,0,16,16h32v8a16,16,0,0,0,16,16h32a16,16,0,0,0,16-16V176a16,16,0,0,0-16-16H120a16,16,0,0,0-16,16v8H72V136H192v24a8,8,0,0,0,12.44,6.66l48-32a8,8,0,0,0,0-13.32ZM136,48a16,16,0,1,1-16,16A16,16,0,0,1,136,48ZM120,176h32v32H120Zm88-30.95V111l25.58,17Z"></path>
                        </svg>

                        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="size-6">
                            <path d="M140,180a12,12,0,1,1-12-12A12,12,0,0,1,140,180ZM128,72c-22.06,0-40,16.15-40,36v4a8,8,0,0,0,16,0v-4c0-11,10.77-20,24-20s24,9,24,20-10.77,20-24,20a8,8,0,0,0-8,8v8a8,8,0,0,0,16,0v-.72c18.24-3.35,32-17.9,32-35.28C168,88.15,150.06,72,128,72Zm104,56A104,104,0,1,1,128,24,104.11,104.11,0,0,1,232,128Zm-16,0a88,88,0,1,0-88,88A88.1,88.1,0,0,0,216,128Z"></path>
                        </svg>

                    </div>

                    <!-- interface details -->
                    <div>
                        <div class="font-semibold leading-5">{{ iface._name }}</div>
                        <div class="text-sm flex space-x-1">

                            <!-- auto interface -->
                            <span v-if="iface.type === 'AutoInterface'">
                            {{ iface.type }} • Ethernet and WiFi
                        </span>

                            <!-- tcp client interface -->
                            <span v-else-if="iface.type === 'TCPClientInterface'">
                            {{ iface.type }} • {{ iface.target_host }}:{{ iface.target_port }}
                        </span>

                            <!-- tcp server interface -->
                            <span v-else-if="iface.type === 'TCPServerInterface'">
                            {{ iface.type }} • {{ iface.listen_ip }}:{{ iface.listen_port }}
                        </span>

                            <!-- udp interface -->
                            <span v-else-if="iface.type === 'UDPInterface'">
                            {{ iface.type }} • {{ iface.listen_ip }}:{{ iface.listen_port }} • {{ iface.forward_ip }}:{{ iface.forward_port }}
                        </span>

                            <!-- rnode interface details -->
                            <span v-else-if="iface.type === 'RNodeInterface'">
                           {{ iface.type }} • {{ iface.port }} • freq={{ iface.frequency }} • bw={{ iface.bandwidth }} • power={{ iface.txpower }}dBm • sf={{ iface.spreadingfactor }} • cr={{ iface.codingrate }}
                        </span>

                            <!-- unknown interface types -->
                            <span v-else>
                           {{ iface.type ?? 'Unknown Interface Type' }}
                        </span>

                        </div>
                    </div>

                    <!-- enabled state badge -->
                    <div class="ml-auto my-auto mr-2">
                        <span v-if="isInterfaceEnabled(iface)" class="inline-flex items-center rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">Enabled</span>
                        <span v-else class="inline-flex items-center rounded-full bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20">Disabled</span>
                    </div>

                    <!-- enable/disable interface button -->
                    <div class="my-auto mr-1">
                        <button v-if="isInterfaceEnabled(iface)" @click="disableInterface(iface._name)" type="button" class="cursor-pointer">
                        <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9" />
                            </svg>
                        </span>
                        </button>
                        <button v-else @click="enableInterface(iface._name)" type="button" class="cursor-pointer">
                        <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9" />
                            </svg>
                        </span>
                        </button>
                    </div>

                    <!-- edit interface button -->
                    <div class="my-auto mr-1">
                        <button @click="editInterface(iface._name)" type="button" class="cursor-pointer">
                        <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
                            </svg>
                        </span>
                        </button>
                    </div>

                    <!-- delete interface button -->
                    <div class="my-auto mr-2">
                        <button @click="deleteInterface(iface._name)" type="button" class="cursor-pointer">
                        <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                        </span>
                        </button>
                    </div>

                </div>

                <div class="flex bg-gray-50 p-1 text-sm text-gray-500 space-x-1 border-t">

                    <!-- status -->
                    <div v-if="iface._stats?.status === true" class="text-sm text-green-500">Connected</div>
                    <div v-else class="text-sm text-red-500">Disconnected</div>

                    <!-- stats -->
                    <div>• Bitrate: {{ formatBitsPerSecond(iface._stats?.bitrate ?? 0) }}</div>
                    <div>• TX: {{ formatBytes(iface._stats?.txb ?? 0) }}</div>
                    <div>• RX: {{ formatBytes(iface._stats?.rxb ?? 0) }}</div>

                </div>

            </div>
        </div>

        <!-- add interface tab -->
        <div v-if="tab === 'interfaces.add'" class="overflow-y-auto p-2 space-y-2">

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
                            <div class="text-xs">betweentheborders.com:4242</div>
                        </div>
                        <div class="ml-2 my-auto">
                            <button @click="newInterfaceName='RNS Testnet BetweenTheBorders';newInterfaceType='TCPClientInterface';newInterfaceTargetHost='betweentheborders.com';newInterfaceTargetPort='4242'" type="button" class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
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
import DialogUtils from "../../js/DialogUtils";
import Utils from "../../js/Utils";

export default {
    name: 'InterfacesPage',
    data() {
        return {

            tab: "interfaces",
            isEditingInterface: false,

            config: null,
            interfaces: {},
            interfaceStats: {},

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
                ],
                codingrates: [
                    5, // 4:5
                    6, // 4:6
                    7, // 4:7
                    8, // 4:8
                ],
                spreadingfactors: [
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                ],
            },

            comports: [],

        };
    },
    mounted() {

        this.getConfig();
        this.loadInterfaces();
        this.updateInterfaceStats();
        this.loadComports();

        // update info every few seconds
        setInterval(() => {
            this.updateInterfaceStats();
        }, 3000);

    },
    methods: {
        relaunch() {
            if(window.electron){
                window.electron.relaunch();
            }
        },
        onIFACSignatureClick: function(ifacSignature) {
            DialogUtils.alert(ifacSignature);
        },
        async getConfig() {
            try {
                const response = await window.axios.get(`/api/v1/config`);
                this.config = response.data.config;
            } catch(e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        async loadInterfaces() {
            try {

                // fetch interfaces
                const response = await window.axios.get(`/api/v1/reticulum/interfaces`);

                // update ui
                this.interfaces = response.data.interfaces;

            } catch(e) {
                // do nothing if failed to load interfaces
            }
        },
        async updateInterfaceStats() {
            try {

                // fetch interface stats
                const response = await window.axios.get(`/api/v1/interface-stats`);

                // update data
                const interfaces = response.data.interface_stats?.interfaces ?? [];
                for(const iface of interfaces){
                    this.interfaceStats[iface.name] = iface;
                }

            } catch(e) {
                // do nothing if failed to load interfaces
            }
        },
        showAddInterfaceForm() {
            this.resetAddInterfaceForm();
            this.loadComports();
            this.isEditingInterface = false;
            this.tab = "interfaces.add";
        },
        showEditInterfaceForm() {
            this.resetAddInterfaceForm();
            this.loadComports();
            this.isEditingInterface = true;
            this.tab = "interfaces.add";
        },
        resetAddInterfaceForm() {

            // clear add interface form
            this.newInterfaceName = null;
            this.newInterfaceType = null;

            // tcp client interface
            this.newInterfaceTargetHost = null;
            this.newInterfaceTargetPort = null;

            // tcp server interface & udp interface
            this.newInterfaceListenIp = null;
            this.newInterfaceListenPort = null;

            // udp interface
            this.newInterfaceForwardIp = null;
            this.newInterfaceForwardPort = null;

            // rnode interface
            this.newInterfacePort = null;
            this.newInterfaceFrequency = null;
            this.newInterfaceBandwidth = null;
            this.newInterfaceTxpower = null;
            this.newInterfaceSpreadingFactor = null;
            this.newInterfaceCodingRate = null;

        },
        findInterfaceStats(interfaceName) {
            const interfaceDescription = this.getInterfaceDescription(interfaceName);
            return this.interfaceStats[interfaceDescription];
        },
        getInterfaceDescription(interfaceName) {

            // the interface-stats api returns interface names like the following;
            //
            // "AutoInterface[Default Interface]"
            // "RNodeInterface[RNode LoRa Interface Fast]"
            // "TCPInterface[RNS Testnet Amsterdam/amsterdam.connect.reticulum.network:4965]"
            //
            // however, the interfaces api just returns;
            // "Default Interface"
            // "RNode LoRa Interface Fast"
            // "RNS Testnet Amsterdam"
            //
            // so we need to map the basic interface name to the former, so we can lookup stats for the interface
            const iface = this.interfaces[interfaceName];
            if(iface){
                switch(iface.type){
                    case "TCPClientInterface": {
                        // yes, this is meant to be passed as TCPInterface, even though the interface type includes client...
                        // example: "TCPInterface[RNS Testnet Amsterdam/amsterdam.connect.reticulum.network:4965]";
                        return `TCPInterface[${interfaceName}/${iface.target_host}:${iface.target_port}]`;
                    }
                    case "TCPServerInterface": {
                        // example: "TCPServerInterface[TCP Server Interface/0.0.0.0:4242]";
                        return `TCPServerInterface[${interfaceName}/${iface.listen_ip}:${iface.listen_port}]`;
                    }
                    case "UDPInterface": {
                        // example: "UDPInterface[UDP Interface/0.0.0.0:1234]";
                        return `UDPInterface[${interfaceName}/${iface.listen_ip}:${iface.listen_port}]`;
                    }
                    default: {
                        // example: "RNodeInterface[RNode LoRa Interface Fast]",
                        return `${iface.type}[${interfaceName}]`;
                    }
                }
            }

            return null;

        },
        isInterfaceEnabled: function(iface) {
            const rawValue = iface.enabled ?? iface.interface_enabled;
            const value = rawValue?.toLowerCase();
            return value === "on" || value === "yes" || value === "true";
        },
        async enableInterface(interfaceName) {

            // enable interface
            try {
                await window.axios.post(`/api/v1/reticulum/interfaces/enable`, {
                    name: interfaceName,
                });
            } catch(e) {
                DialogUtils.alert("failed to enable interface");
                console.log(e);
            }

            // reload interfaces
            await this.loadInterfaces();

        },
        async disableInterface(interfaceName) {

            // disable interface
            try {
                await window.axios.post(`/api/v1/reticulum/interfaces/disable`, {
                    name: interfaceName,
                });
            } catch(e) {
                DialogUtils.alert("failed to disable interface");
                console.log(e);
            }

            // reload interfaces
            await this.loadInterfaces();

        },
        async editInterface(interfaceName) {

            // find interface
            const iface = this.interfaces[interfaceName];
            if(!iface){
                return;
            }

            // go to edit interface tab
            this.showEditInterfaceForm();

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

        },
        async deleteInterface(interfaceName) {

            // ask user to confirm deleting conversation history
            if(!confirm("Are you sure you want to delete this interface? This can not be undone!")){
                return;
            }

            // delete interface
            try {
                await window.axios.post(`/api/v1/reticulum/interfaces/delete`, {
                    name: interfaceName,
                });
            } catch(e) {
                DialogUtils.alert("failed to delete interface");
                console.log(e);
            }

            // reload interfaces
            await this.loadInterfaces();

        },
        formatBitsPerSecond: function(bits) {
            return Utils.formatBitsPerSecond(bits);
        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
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
        formatFrequency: function(hz) {
            return Utils.formatFrequency(hz);
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

                // reset add interface form
                this.resetAddInterfaceForm();

                // go to interfaces tab
                this.tab = "interfaces";

                // show success message
                if(response.data.message){
                    DialogUtils.alert(response.data.message);
                }

            } catch(e) {
                const message = e.response?.data?.message ?? "failed to add interface";
                DialogUtils.alert(message);
                console.log(e);
            }

            // reload interfaces
            await this.loadInterfaces();

        },
        async loadComports() {
            try {
                const response = await window.axios.get(`/api/v1/comports`);
                this.comports = response.data.comports;
            } catch(e) {
                // do nothing if failed to load interfaces
            }
        },
    },
    computed: {
        isElectron() {
            return window.electron != null;
        },
        interfacesWithStats() {
            const results = [];
            for(const [interfaceName, iface] of Object.entries(this.interfaces)){
                iface._name = interfaceName;
                iface._stats = this.findInterfaceStats(interfaceName);
                results.push(iface);
            }
            return results;
        },
    },
}
</script>
