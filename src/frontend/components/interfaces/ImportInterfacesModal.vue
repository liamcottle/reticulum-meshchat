<template>
    <div v-if="isShowing" class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity flex items-center justify-center">
        <div class="flex w-full h-full p-4 overflow-y-auto">
            <div v-click-outside="dismiss" class="my-auto mx-auto w-full bg-white dark:bg-zinc-900 rounded-lg shadow-xl max-w-2xl">

                <!-- title -->
                <div class="p-4 border-b dark:border-zinc-700">
                    <h3 class="text-lg font-semibold dark:text-white">Import Interfaces</h3>
                </div>

                <!-- content -->
                <div class="divide-y dark:divide-zinc-700">

                    <!-- file input -->
                    <div class="p-2">
                        <div>
                            <input ref="import-interfaces-file-input" type="file" @change="onFileSelected" accept="*" class="w-full text-sm text-gray-500 dark:text-zinc-400">
                        </div>
                        <div v-if="!selectedFile" class="mt-2 text-sm text-gray-700 dark:text-zinc-200">
                            <ul class="list-disc list-inside">
                                <li>You can import interfaces from a ~/.reticulum/config file.</li>
                                <li>You can import interfaces from an exported interfaces file.</li>
                            </ul>
                        </div>
                    </div>

                    <!-- select interfaces -->
                    <div v-if="importableInterfaces.length > 0" class="divide-y dark:divide-zinc-700">
                        <div class="flex p-2">
                            <div class="my-auto mr-auto text-sm font-medium text-gray-700 dark:text-zinc-200">Select Interfaces to Import</div>
                            <div class="my-auto space-x-2">
                                <button @click="selectAllInterfaces" class="text-sm text-blue-500 hover:underline">Select All</button>
                                <button @click="deselectAllInterfaces" class="text-sm text-blue-500 hover:underline">Deselect All</button>
                            </div>
                        </div>
                        <div class="bg-gray-200 p-2 space-y-2 max-h-80 overflow-y-auto dark:bg-zinc-800">
                            <div @click="toggleSelectedInterface(iface.name)" v-for="iface in importableInterfaces" :key="iface.name" class="bg-white cursor-pointer flex items-center p-2 border rounded shadow dark:bg-zinc-900 dark:border-zinc-700">
                                <div class="mr-auto text-sm">
                                    <div class="font-semibold text-gray-700 dark:text-zinc-100">{{ iface.name }}</div>
                                    <div class="text-sm text-gray-500 dark:text-zinc-100">{{ iface.type }}</div>
                                </div>
                                <input @click.stop type="checkbox" v-model="selectedInterfaces" :value="iface.name" class="mx-2 h-4 w-4 text-blue-600 rounded border-gray-300 dark:border-zinc-600">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- actions -->
                <div class="p-4 border-t dark:border-zinc-700 flex justify-end space-x-2">
                    <button @click="dismiss" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 dark:bg-zinc-800 dark:text-zinc-200 dark:border-zinc-600 dark:hover:bg-zinc-700">
                        Cancel
                    </button>
                    <button @click="importSelectedInterfaces" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
                        Import Selected
                    </button>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import DialogUtils from "../../js/DialogUtils";

export default {
    name: "ImportInterfacesModal",
    emits: [
        "dismissed",
    ],
    data() {
        return {
            isShowing: false,
            selectedFile: null,
            importableInterfaces: [],
            selectedInterfaces: [],
        };
    },
    methods: {
        show() {
            this.isShowing = true;
            this.selectedFile = null;
            this.importableInterfaces = [];
            this.selectedInterfaces = [];
        },
        dismiss() {
            this.isShowing = false;
            this.$emit("dismissed");
        },
        clearSelectedFile() {
            this.selectedFile = null;
            this.$refs["import-interfaces-file-input"].value = null;
        },
        async onFileSelected(event) {

            // get selected file
            const file = event.target.files[0];
            if(!file){
                return;
            }

            // update ui
            this.selectedFile = file;
            this.importableInterfaces = [];
            this.selectedInterfaces = [];

            try {

                // fetch preview of interfaces to import
                const response = await window.axios.post('/api/v1/reticulum/interfaces/import-preview', {
                    config: await file.text(),
                });

                // ensure there are some interfaces available to import
                if(!response.data.interfaces || response.data.interfaces.length === 0){
                    this.clearSelectedFile();
                    DialogUtils.alert("No interfaces were found in the selected configuration file");
                    return;
                }

                // update ui
                this.importableInterfaces = response.data.interfaces;

                // auto select all interfaces
                this.selectAllInterfaces();

            } catch(e) {
                this.clearSelectedFile();
                DialogUtils.alert("Failed to parse configuration file");
                console.error(e);
            }
        },
        isInterfaceSelected(name) {
            return this.selectedInterfaces.includes(name);
        },
        selectInterface(name) {
            if(!this.isInterfaceSelected(name)){
                this.selectedInterfaces.push(name);
            }
        },
        deselectInterface(name) {
            this.selectedInterfaces = this.selectedInterfaces.filter((selectedInterfaceName) => {
                return selectedInterfaceName !== name;
            });
        },
        toggleSelectedInterface(name) {
            if(this.isInterfaceSelected(name)){
                this.deselectInterface(name);
            } else {
                this.selectInterface(name);
            }
        },
        selectAllInterfaces() {
            this.selectedInterfaces = this.importableInterfaces.map(i => i.name);
        },
        deselectAllInterfaces() {
            this.selectedInterfaces = [];
        },
        async importSelectedInterfaces() {

            // ensure user selected a file to import from
            if(!this.selectedFile){
                DialogUtils.alert("Please select a configuration file");
                return;
            }

            // ensure user selected some interfaces
            if(this.selectedInterfaces.length === 0){
                DialogUtils.alert("Please select at least one interface to import");
                return;
            }

            try {

                // import interfaces
                await window.axios.post('/api/v1/reticulum/interfaces/import', {
                    config: await this.selectedFile.text(),
                    selected_interface_names: this.selectedInterfaces,
                });

                // dismiss modal
                this.dismiss();

                // tell user interfaces were imported
                DialogUtils.alert("Interfaces imported successfully. MeshChat must be restarted for these changes to take effect.");

            } catch(e) {
                const message = e.response?.data?.message || "Failed to import interfaces";
                DialogUtils.alert(message);
                console.error(e);
            }
        },
    },
}
</script>