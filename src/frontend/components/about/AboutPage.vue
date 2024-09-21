<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- app info -->
            <div v-if="appInfo" class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">App Info</div>
                <div class="divide-y text-gray-900">

                    <!-- version -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Versions</div>
                            <div class="text-sm text-gray-700">MeshChat v{{ appInfo.version }} • RNS v{{ appInfo.rns_version }} • LXMF v{{ appInfo.lxmf_version }}</div>
                        </div>
                        <div class="hidden sm:block mx-2 my-auto">
                            <a target="_blank" href="https://github.com/liamcottle/reticulum-meshchat/releases" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Check for Updates
                            </a>
                        </div>
                    </div>

                    <!-- reticulum config path -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Reticulum Config Path</div>
                            <div class="text-sm text-gray-700 break-all">{{ appInfo.reticulum_config_path }}</div>
                        </div>
                        <div v-if="isElectron" class="mx-2 my-auto">
                            <button @click="showReticulumConfigFile" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Show in Folder
                            </button>
                        </div>
                    </div>

                    <!-- database path -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Database Path</div>
                            <div class="text-sm text-gray-700 break-all">{{ appInfo.database_path }}</div>
                        </div>
                        <div v-if="isElectron" class="mx-2 my-auto">
                            <button @click="showDatabaseFile" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Show in Folder
                            </button>
                        </div>
                    </div>

                    <!-- database file size -->
                    <div class="p-1">
                        <div>Database File Size</div>
                        <div class="text-sm text-gray-700">{{ formatBytes(appInfo.database_file_size) }}</div>
                    </div>

                </div>
            </div>

            <!-- reticulum status -->
            <div v-if="appInfo" class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">Reticulum Status</div>
                <div class="divide-y text-gray-900">

                    <!-- instance mode -->
                    <div class="p-1">
                        <div>Instance Mode</div>
                        <div class="text-sm text-gray-700">
                            <span v-if="appInfo.is_connected_to_shared_instance" class="text-orange-600">Connected to Shared Instance</span>
                            <span v-else class="text-green-600">Running as Standalone Instance</span>
                        </div>
                    </div>

                    <!-- transport mode -->
                    <div class="p-1">
                        <div>Transport Mode</div>
                        <div class="text-sm text-gray-700">
                            <span v-if="appInfo.is_transport_enabled" class="text-green-600">Transport Enabled</span>
                            <span v-else class="text-orange-600">Transport Disabled</span>
                        </div>
                    </div>

                </div>
            </div>

            <!-- my addresses -->
            <div v-if="config" class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">My Addresses</div>
                <div class="divide-y text-gray-900">
                    <div class="p-1">
                        <div>Identity Hash</div>
                        <div class="text-sm text-gray-700">{{ config.identity_hash }}</div>
                    </div>
                    <div class="p-1">
                        <div>LXMF Address</div>
                        <div class="text-sm text-gray-700">{{ config.lxmf_address_hash }}</div>
                    </div>
                    <div class="p-1">
                        <div>LXMF Propagation Node Address</div>
                        <div class="text-sm text-gray-700">{{ config.lxmf_local_propagation_node_address_hash }}</div>
                    </div>
                    <div class="p-1">
                        <div>Audio Call Address</div>
                        <div class="text-sm text-gray-700">{{ config.audio_call_address_hash }}</div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import ElectronUtils from "../../js/ElectronUtils";
export default {
    name: 'AboutPage',
    data() {
        return {
            appInfo: null,
            config: null,
        };
    },
    mounted() {
        this.getAppInfo();
        this.getConfig();
    },
    methods: {
        async getAppInfo() {
            try {
                const response = await window.axios.get("/api/v1/app/info");
                this.appInfo = response.data.app_info;
            } catch(e) {
                // do nothing if failed to load app info
                console.log(e);
            }
        },
        async getConfig() {
            try {
                const response = await window.axios.get("/api/v1/config");
                this.config = response.data.config;
            } catch(e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        showReticulumConfigFile() {
            const reticulumConfigPath = this.appInfo.reticulum_config_path;
            if(reticulumConfigPath){
                ElectronUtils.showPathInFolder(reticulumConfigPath);
            }
        },
        showDatabaseFile() {
            const databasePath = this.appInfo.database_path;
            if(databasePath){
                ElectronUtils.showPathInFolder(databasePath);
            }
        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
    },
    computed: {
        isElectron() {
            return ElectronUtils.isElectron();
        },
    },
}
</script>
