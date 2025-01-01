<template>
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
                <button @click="dismiss" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 dark:bg-zinc-800 dark:text-zinc-200 dark:border-zinc-600 dark:hover:bg-zinc-700">
                    Cancel
                </button>
                <button @click="importSelectedInterfaces" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
                    Import Selected
                </button>
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
            showingImportDialog: false,
            importableInterfaces: [],
            selectedInterfaces: [],
            importFile: null,
        };
    },
    methods: {
        show() {
            this.showingImportDialog = true;
            this.importableInterfaces = [];
            this.selectedInterfaces = [];
            this.importFile = null;
        },
        dismiss() {
            this.showingImportDialog = false;
            this.$emit("dismissed");
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
                    this.dismiss();
                }
            } catch(e) {
                DialogUtils.alert("Failed to parse configuration file");
                console.error(e);
                this.dismiss();
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
                this.dismiss();
                DialogUtils.alert("Interfaces imported successfully");
            } catch(e) {
                const message = e.response?.data?.message || "Failed to import interfaces";
                DialogUtils.alert(message);
                console.error(e);
            }
        },
    },
}
</script>