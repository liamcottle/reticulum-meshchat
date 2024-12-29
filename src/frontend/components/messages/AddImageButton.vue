<template>
    <div class="inline-flex rounded-md shadow-sm">

        <button @click="showMenu" type="button" class="my-auto mr-1 inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:bg-zinc-800 dark:text-white dark:hover:bg-zinc-700 dark:focus-visible:outline-zinc-500">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 0 1 2.25-2.25h16.5A2.25 2.25 0 0 1 22.5 6v12a2.25 2.25 0 0 1-2.25 2.25H3.75A2.25 2.25 0 0 1 1.5 18V6ZM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0 0 21 18v-1.94l-2.69-2.689a1.5 1.5 0 0 0-2.12 0l-.88.879.97.97a.75.75 0 1 1-1.06 1.06l-5.16-5.159a1.5 1.5 0 0 0-2.12 0L3 16.061Zm10.125-7.81a1.125 1.125 0 1 1 2.25 0 1.125 1.125 0 0 1-2.25 0Z" clip-rule="evenodd" />
            </svg>
            <span class="ml-1 hidden xl:inline-block whitespace-nowrap">Add Image</span>
        </button>

        <div class="relative block">
            <Transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95">
                <div v-if="isShowingMenu" v-click-outside="hideMenu" class="absolute bottom-0 -ml-11 sm:right-0 sm:ml-0 z-10 mb-10 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div class="py-1">
                        <button @click="addImage('low')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Low Quality (320x320)</button>
                        <button @click="addImage('medium')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Medium Quality (640x640)</button>
                        <button @click="addImage('high')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">High Quality (1280x1280)</button>
                        <button @click="addImage('original')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Original Quality</button>
                    </div>
                </div>
            </Transition>
        </div>

        <!-- hidden file input for selecting files -->
        <input ref="image-input" @change="onImageInputChange" type="file" accept="image/*" style="display:none"/>

    </div>
</template>

<script>
import Compressor from 'compressorjs';
import DialogUtils from "../../js/DialogUtils";
export default {
    name: 'AddImageButton',
    emits: [
        "add-image",
    ],
    data() {
        return {
            isShowingMenu: false,
            selectedImageQuality: null,
        };
    },
    methods: {
        showMenu() {
            this.isShowingMenu = true;
        },
        hideMenu() {
            this.isShowingMenu = false;
        },
        addImage(quality) {
            this.isShowingMenu = false;
            this.selectedImageQuality = quality;
            this.$refs["image-input"].click();
        },
        clearImageInput: function() {
            this.$refs["image-input"].value = null;
        },
        onImageInputChange: async function(event) {
            if(event.target.files.length > 0){

                // get selected file
                const file = event.target.files[0];

                // process file based on selected image quality
                switch(this.selectedImageQuality) {
                    case "low": {
                        new Compressor(file, {
                            maxWidth: 320,
                            maxHeight: 320,
                            quality: 0.2,
                            mimeType: "image/webp",
                            success: (result) => {
                                this.$emit("add-image", result);
                            },
                            error: (err) => {
                                DialogUtils.alert(err.message);
                            },
                        });
                        break;
                    }
                    case "medium": {
                        new Compressor(file, {
                            maxWidth: 640,
                            maxHeight: 640,
                            quality: 0.6,
                            mimeType: "image/webp",
                            success: (result) => {
                                this.$emit("add-image", result);
                            },
                            error: (err) => {
                                DialogUtils.alert(err.message);
                            },
                        });
                        break;
                    }
                    case "high": {
                        new Compressor(file, {
                            maxWidth: 1280,
                            maxHeight: 1280,
                            quality: 0.75,
                            mimeType: "image/webp",
                            success: (result) => {
                                this.$emit("add-image", result);
                            },
                            error: (err) => {
                                DialogUtils.alert(err.message);
                            },
                        });
                        break;
                    }
                    case "original": {
                        this.$emit("add-image", file);
                        break;
                    }
                    default: {
                        DialogUtils.alert(`Unsupported image quality: ${this.selectedImageQuality}`);
                        break;
                    }
                }

                // clear image input to allow selecting the same file after user removed it
                this.clearImageInput();

            }
        },
    },
}
</script>
