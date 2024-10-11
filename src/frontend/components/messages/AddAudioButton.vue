<template>
    <div class="inline-flex rounded-md shadow-sm">

        <button v-if="isRecordingAudioAttachment" @click="stopRecordingAudioAttachment" type="button" class="my-auto mr-1 inline-flex items-center gap-x-1 rounded-md bg-red-500 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
                <path d="M7 4a3 3 0 0 1 6 0v6a3 3 0 1 1-6 0V4Z" />
                <path d="M5.5 9.643a.75.75 0 0 0-1.5 0V10c0 3.06 2.29 5.585 5.25 5.954V17.5h-1.5a.75.75 0 0 0 0 1.5h4.5a.75.75 0 0 0 0-1.5h-1.5v-1.546A6.001 6.001 0 0 0 16 10v-.357a.75.75 0 0 0-1.5 0V10a4.5 4.5 0 0 1-9 0v-.357Z" />
            </svg>
            <span class="ml-1">
                <slot/>
            </span>
        </button>

        <button v-else @click="showMenu" type="button" class="my-auto mr-1 inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
                <path d="M7 4a3 3 0 0 1 6 0v6a3 3 0 1 1-6 0V4Z" />
                <path d="M5.5 9.643a.75.75 0 0 0-1.5 0V10c0 3.06 2.29 5.585 5.25 5.954V17.5h-1.5a.75.75 0 0 0 0 1.5h4.5a.75.75 0 0 0 0-1.5h-1.5v-1.546A6.001 6.001 0 0 0 16 10v-.357a.75.75 0 0 0-1.5 0V10a4.5 4.5 0 0 1-9 0v-.357Z" />
            </svg>
            <span class="ml-1 hidden sm:inline-block">Add Voice</span>
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
                        <button @click="startRecordingCodec2('1200')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Low Quality - Codec2 (1200)</button>
                        <button @click="startRecordingCodec2('3200')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Medium Quality - Codec2 (3200)</button>
                        <button @click="startRecordingOpus()" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">High Quality - OPUS</button>
                    </div>
                </div>
            </Transition>
        </div>

    </div>
</template>

<script>
export default {
    name: 'AddAudioButton',
    props: {
        isRecordingAudioAttachment: Boolean,
    },
    data() {
        return {
            isShowingMenu: false,
        };
    },
    methods: {
        showMenu() {
            this.isShowingMenu = true;
        },
        hideMenu() {
            this.isShowingMenu = false;
        },
        startRecordingAudioAttachment(args) {
            this.isShowingMenu = false;
            this.$emit("start-recording", args);
        },
        startRecordingCodec2(mode) {
            this.startRecordingAudioAttachment({
                codec: "codec2",
                mode: mode,
            });
        },
        startRecordingOpus() {
            this.startRecordingAudioAttachment({
                codec: "opus",
            });
        },
        stopRecordingAudioAttachment() {
            this.isShowingMenu = false;
            this.$emit("stop-recording");
        },
    },
}
</script>
