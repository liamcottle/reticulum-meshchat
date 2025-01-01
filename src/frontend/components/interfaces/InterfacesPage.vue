<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="overflow-y-auto p-2 space-y-2">

            <!-- warning - keeping orange-500 for warning visibility in both modes -->
            <div class="flex bg-orange-500 p-2 text-sm font-semibold leading-6 text-white rounded shadow">
                <div class="my-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                    </svg>
                </div>
                <div class="ml-2 my-auto">Reticulum MeshChat must be restarted for any interface changes to take effect.</div>
                <button v-if="isElectron" 
                    @click="relaunch" 
                    type="button" 
                    class="ml-auto my-auto inline-flex items-center gap-x-1 rounded-md bg-white dark:bg-zinc-800 px-2 py-1 text-sm font-semibold text-black dark:text-zinc-200 shadow-sm hover:bg-gray-50 dark:hover:bg-zinc-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white dark:focus-visible:outline-zinc-700">
                    <span>Restart Now</span>
                </button>
            </div>

            <div class="flex space-x-1">

                <!-- Add Interface button -->
                <RouterLink :to="{ name: 'interfaces.add' }">
                    <button type="button" 
                        class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-700">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                        <span>Add Interface</span>
                    </button>
                </RouterLink>

                <!-- Import button -->
                <div class="my-auto">
                    <button @click="showImportInterfacesModal" type="button" class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-700">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                        </svg>
                        <span>Import</span>
                    </button>
                </div>

                <!-- Export button -->
                <div class="my-auto">
                    <button @click="exportInterfaces" type="button" class="inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-700">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                        </svg>
                        <span>Export</span>
                    </button>
                </div>

            </div>

            <!-- enabled interfaces -->
            <Interface
                v-for="iface of enabledInterfaces"
                :iface="iface"
                @enable="enableInterface(iface._name)"
                @disable="disableInterface(iface._name)"
                @edit="editInterface(iface._name)"
                @export="exportInterface(iface._name)"
                @delete="deleteInterface(iface._name)"/>

            <!-- disabled interfaces -->
            <div v-if="disabledInterfaces.length > 0" class="font-semibold dark:text-zinc-200">Disabled Interfaces</div>
            <Interface
                v-for="iface of disabledInterfaces"
                :iface="iface"
                @enable="enableInterface(iface._name)"
                @disable="disableInterface(iface._name)"
                @edit="editInterface(iface._name)"
                @export="exportInterface(iface._name)"
                @delete="deleteInterface(iface._name)"/>

        </div>
    </div>

    <!-- Import Dialog -->
    <ImportInterfacesModal ref="import-interfaces-modal" @dismissed="onImportInterfacesModalDismissed"/>

</template>

<script>
import DialogUtils from "../../js/DialogUtils";
import ElectronUtils from "../../js/ElectronUtils";
import Interface from "./Interface.vue";
import Utils from "../../js/Utils";
import ImportInterfacesModal from "./ImportInterfacesModal.vue";
import DownloadUtils from "../../js/DownloadUtils";

export default {
    name: 'InterfacesPage',
    components: {
        ImportInterfacesModal,
        Interface,
    },
    data() {
        return {
            interfaces: {},
            interfaceStats: {},
            reloadInterval: null,
        };
    },
    beforeUnmount() {
        clearInterval(this.reloadInterval);
    },
    mounted() {

        this.loadInterfaces();
        this.updateInterfaceStats();

        // update info every few seconds
        this.reloadInterval = setInterval(() => {
            this.updateInterfaceStats();
        }, 1000);

    },
    methods: {
        relaunch() {
            ElectronUtils.relaunch();
        },
        isInterfaceEnabled: function(iface) {
            return Utils.isInterfaceEnabled(iface);
        },
        async loadInterfaces() {
            try {
                const response = await window.axios.get(`/api/v1/reticulum/interfaces`);
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
            this.$router.push({
                name: "interfaces.edit",
                query: {
                    interface_name: interfaceName,
                },
            });
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
        async exportInterfaces() {
            try {

                // fetch exported interfaces
                const response = await window.axios.post('/api/v1/reticulum/interfaces/export');

                // download file to browser
                DownloadUtils.downloadFile("meshchat_interfaces", new Blob([response.data], {
                    type: "application/octet-stream",
                }));

            } catch(e) {
                DialogUtils.alert("Failed to export interfaces");
                console.error(e);
            }
        },
        async exportInterface(interfaceName) {
            try {

                // fetch exported interfaces
                const response = await window.axios.post('/api/v1/reticulum/interfaces/export', {
                    selected_interface_names: [
                        interfaceName,
                    ],
                });

                // download file to browser
                DownloadUtils.downloadFile(interfaceName, new Blob([response.data], {
                    type: "application/octet-stream",
                }));

            } catch(e) {
                DialogUtils.alert("Failed to export interface");
                console.error(e);
            }
        },
        showImportInterfacesModal() {
            this.$refs["import-interfaces-modal"].show();
        },
        onImportInterfacesModalDismissed() {
            // reload interfaces as something may have been imported
            this.loadInterfaces();
        },
    },
    computed: {
        isElectron() {
            return ElectronUtils.isElectron();
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
        enabledInterfaces() {
            return this.interfacesWithStats.filter((iface) => this.isInterfaceEnabled(iface));
        },
        disabledInterfaces() {
            return this.interfacesWithStats.filter((iface) => !this.isInterfaceEnabled(iface));
        },
    },
}
</script>
