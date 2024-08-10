<template>
    <div class="border rounded bg-white shadow overflow-hidden">

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
                <button v-if="isInterfaceEnabled(iface)" @click="disableInterface" type="button" class="cursor-pointer">
                    <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9" />
                        </svg>
                    </span>
                </button>
                <button v-else @click="enableInterface" type="button" class="cursor-pointer">
                    <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9" />
                        </svg>
                    </span>
                </button>
            </div>

            <!-- edit interface button -->
            <div class="my-auto mr-1">
                <button @click="editInterface" type="button" class="cursor-pointer">
                    <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
                        </svg>
                    </span>
                </button>
            </div>

            <!-- delete interface button -->
            <div class="my-auto mr-2">
                <button @click="deleteInterface" type="button" class="cursor-pointer">
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
            <div v-if="iface._stats?.clients">• Clients: {{ iface._stats?.clients }}</div>

        </div>

    </div>
</template>

<script>
import DialogUtils from "../../js/DialogUtils";
import Utils from "../../js/Utils";

export default {
    name: 'Interface',
    props: {
        iface: Object,
    },
    data() {
        return {

        };
    },
    methods: {
        onIFACSignatureClick: function(ifacSignature) {
            DialogUtils.alert(ifacSignature);
        },
        isInterfaceEnabled: function(iface) {
            return Utils.isInterfaceEnabled(iface);
        },
        enableInterface() {
            this.$emit("enable");
        },
        disableInterface() {
            this.$emit("disable");
        },
        editInterface() {
            this.$emit("edit");
        },
        deleteInterface() {
            this.$emit("delete");
        },
        formatBitsPerSecond: function(bits) {
            return Utils.formatBitsPerSecond(bits);
        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
    },
}
</script>
