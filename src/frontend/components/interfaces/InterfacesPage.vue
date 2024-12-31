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

            <div class="flex space-x-2">
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

                <!-- Export button -->
                <button @click="exportInterfaces" type="button" 
                    class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-700">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                    </svg>
                    <span>Export</span>
                </button>

                <!-- Import button -->
                <button @click="showImportDialog" type="button" 
                    class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-700">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                    <span>Import</span>
                </button>
            </div>

            <!-- enabled interfaces -->
            <Interface
                v-for="iface of enabledInterfaces"
                :iface="iface"
                @enable="enableInterface(iface._name)"
                @disable="disableInterface(iface._name)"
                @edit="editInterface(iface._name)"
                @delete="deleteInterface(iface._name)"/>

            <!-- disabled interfaces -->
            <div v-if="disabledInterfaces.length > 0" class="font-semibold dark:text-zinc-200">Disabled Interfaces</div>
            <Interface
                v-for="iface of disabledInterfaces"
                :iface="iface"
                @enable="enableInterface(iface._name)"
                @disable="disableInterface(iface._name)"
                @edit="editInterface(iface._name)"
                @delete="deleteInterface(iface._name)"/>
        </div>
    </div>

    <!-- Import Dialog -->
    <div v-if="showingImportDialog" class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity flex items-center justify-center">
        <div class="bg-white dark:bg-zinc-900 rounded-lg shadow-xl max-w-2xl w-full mx-4">
            <div class="p-4 border-b dark:border-zinc-700">
                <h3 class="text-lg font-semibold dark:text-white">Import Interfaces</h3>
            </div>
            
            <div class="p-4 space-y-4">
                <!-- File Input -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-zinc-200">Select Configuration File</label>
                    <input type="file" 
                        @change="onFileSelected" 
                        accept="*"
                        class="mt-1 block w-full text-sm text-gray-500 dark:text-zinc-400
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-md file:border-0
                        file:text-sm file:font-semibold
                        file:bg-gray-500 file:text-white
                        hover:file:bg-gray-400
                        dark:file:bg-zinc-700 dark:hover:file:bg-zinc-600">
                </div>

                <!-- Interface Selection -->
                <div v-if="importableInterfaces.length > 0">
                    <div class="flex justify-between mb-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-zinc-200">Select Interfaces to Import</label>
                        <div class="space-x-2">
                            <button @click="selectAllInterfaces" class="text-sm text-blue-500">Select All</button>
                            <button @click="deselectAllInterfaces" class="text-sm text-blue-500">Deselect All</button>
                        </div>
                    </div>
                    <div class="space-y-2 max-h-60 overflow-y-auto">
                        <div v-for="iface in importableInterfaces" :key="iface.name" 
                            class="flex items-center p-2 border rounded dark:border-zinc-700">
                            <input type="checkbox" 
                                v-model="selectedInterfaces" 
                                :value="iface.name"
                                class="h-4 w-4 text-blue-600 rounded border-gray-300 dark:border-zinc-600">
                            <label class="ml-2 text-sm text-gray-700 dark:text-zinc-200">
                                {{ iface.name }} ({{ iface.type }})
                            </label>
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-4 border-t dark:border-zinc-700 flex justify-end space-x-2">
                <button @click="closeImportDialog" 
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 dark:bg-zinc-800 dark:text-zinc-200 dark:border-zinc-600 dark:hover:bg-zinc-700">
                    Cancel
                </button>
                <button @click="importSelectedInterfaces" 
                    class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
                    Import Selected
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import DialogUtils from "../../js/DialogUtils";
import ElectronUtils from "../../js/ElectronUtils";
import Interface from "./Interface.vue";
import Utils from "../../js/Utils";

export default {
    name: 'InterfacesPage',
    components: {
        Interface,
    },
    data() {
        return {
            interfaces: {},
            interfaceStats: {},
            reloadInterval: null,
            showingImportDialog: false,
            importableInterfaces: [],
            selectedInterfaces: [],
            importFile: null
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
                const response = await window.axios.get('/api/v1/reticulum/interfaces/export', {
                    responseType: 'blob'
                });
                
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'reticulum_interfaces');
                document.body.appendChild(link);
                link.click();
                link.remove();
            } catch(e) {
                DialogUtils.alert("Failed to export interfaces");
                console.error(e);
            }
        },
        showImportDialog() {
            this.showingImportDialog = true;
            this.importableInterfaces = [];
            this.selectedInterfaces = [];
            this.importFile = null;
        },
        closeImportDialog() {
            this.showingImportDialog = false;
        },
        async onFileSelected(event) {
            const file = event.target.files[0];
            if (!file) return;

            this.importFile = file;
            this.importableInterfaces = [];
            this.selectedInterfaces = [];

            const formData = new FormData();
            formData.append('config', file);

            try {
                const response = await window.axios.post('/api/v1/reticulum/interfaces/preview', formData);
                if (response.data.interfaces && response.data.interfaces.length > 0) {
                    this.importableInterfaces = response.data.interfaces;
                    this.selectedInterfaces = this.importableInterfaces.map(i => i.name);
                } else {
                    DialogUtils.alert("No valid interfaces found in configuration file");
                    this.closeImportDialog();
                }
            } catch(e) {
                DialogUtils.alert("Failed to parse configuration file");
                console.error(e);
                this.closeImportDialog();
            }
        },
        selectAllInterfaces() {
            this.selectedInterfaces = this.importableInterfaces.map(i => i.name);
        },
        deselectAllInterfaces() {
            this.selectedInterfaces = [];
        },
        async importSelectedInterfaces() {
            if (!this.importFile) {
                DialogUtils.alert("Please select a configuration file");
                return;
            }

            if (this.selectedInterfaces.length === 0) {
                DialogUtils.alert("Please select at least one interface to import");
                return;
            }

            const formData = new FormData();
            formData.append('config', this.importFile);
            formData.append('selected_interfaces', JSON.stringify(this.selectedInterfaces));

            try {
                await window.axios.post('/api/v1/reticulum/interfaces/import', formData);
                await this.loadInterfaces();
                this.closeImportDialog();
                DialogUtils.alert("Interfaces imported successfully");
            } catch(e) {
                const message = e.response?.data?.message || "Failed to import interfaces";
                DialogUtils.alert(message);
                console.error(e);
            }
        }
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
