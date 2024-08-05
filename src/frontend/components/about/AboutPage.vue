<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- app info -->
            <div v-if="appInfo" class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">App Info</div>
                <div class="divide-y text-gray-900">
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Version</div>
                            <div class="text-sm text-gray-700">v{{ appInfo.version }}</div>
                        </div>
                        <div class="mx-2 my-auto">
                            <a target="_blank" href="https://github.com/liamcottle/reticulum-meshchat/releases" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Check for Updates
                            </a>
                        </div>
                    </div>
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Reticulum Config Path</div>
                            <div class="text-sm text-gray-700">{{ appInfo.reticulum_config_path }}</div>
                        </div>
                        <div v-if="isElectron" class="mx-2 my-auto">
                            <button @click="showReticulumConfigFile" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Show in Folder
                            </button>
                        </div>
                    </div>
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Database Path</div>
                            <div class="text-sm text-gray-700">{{ appInfo.database_path }}</div>
                        </div>
                        <div v-if="isElectron" class="mx-2 my-auto">
                            <button @click="showDatabaseFile" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Show in Folder
                            </button>
                        </div>
                    </div>
                    <div class="p-1">
                        <div>Database File Size</div>
                        <div class="text-sm text-gray-700">{{ formatBytes(appInfo.database_file_size) }}</div>
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
            if(window.electron && this.appInfo.reticulum_config_path){
                window.electron.showPathInFolder(this.appInfo.reticulum_config_path);
            }
        },
        showDatabaseFile() {
            if(window.electron && this.appInfo.database_path){
                window.electron.showPathInFolder(this.appInfo.database_path);
            }
        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
    },
    computed: {
        isElectron() {
            return Utils.isElectron();
        },
    },
}
</script>
