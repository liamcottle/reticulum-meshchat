<template>
    <div class="inline-flex rounded-md shadow-sm">

        <!-- send button -->
        <button @click="send" :disabled="!canSendMessage" type="button" class="my-auto inline-flex items-center rounded-l-md px-2.5 py-1.5 text-sm font-semibold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2" :class="[ canSendMessage ? 'bg-blue-500 hover:bg-blue-400 focus-visible:outline-blue-500' : 'bg-gray-400 focus-visible:outline-gray-500 cursor-not-allowed']">
            <span v-if="isSendingMessage">Sending...</span>
            <span v-else>
                <span>Send</span>
                <span v-if="deliveryMethod === 'direct'"> (Direct Link)</span>
                <span v-if="deliveryMethod === 'opportunistic'"> (Opportunistic)</span>
                <span v-if="deliveryMethod === 'propagated'"> (Propagated)</span>
            </span>
        </button>

        <div class="relative">

            <!-- dropdown button -->
            <button @click="showMenu" :disabled="!canSendMessage" type="button" class="my-auto border-l relative inline-flex items-center rounded-r-md bg-gray-500 focus-visible:outline-gray-400 px-2 py-1.5 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2" :class="[ canSendMessage ? 'bg-blue-500 hover:bg-blue-400 focus-visible:outline-blue-500' : 'bg-gray-400 focus-visible:outline-gray-500 cursor-not-allowed']">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" data-slot="icon">
                    <path fill-rule="evenodd" d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
                </svg>
            </button>

            <!-- dropdown menu -->
            <Transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95">
                <div v-if="isShowingMenu" v-click-outside="hideMenu" class="absolute bottom-0 -ml-11 right-0 ml-0 z-10 mb-10 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div class="py-1">
                        <button @click="setDeliveryMethod(null)" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap border-b">Send Automatically</button>
                        <button @click="setDeliveryMethod('direct')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Send over Direct Link</button>
                        <button @click="setDeliveryMethod('opportunistic')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Send Opportunistically</button>
                        <button @click="setDeliveryMethod('propagated')" type="button" class="w-full block text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 whitespace-nowrap">Send to Propagation Node</button>
                    </div>
                </div>
            </Transition>

        </div>

    </div>
</template>

<script>
export default {
    name: 'SendMessageButton',
    props: {
        deliveryMethod: String,
        canSendMessage: Boolean,
        isSendingMessage: Boolean,
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
        setDeliveryMethod(deliveryMethod) {
            this.$emit("delivery-method-changed", deliveryMethod);
            this.hideMenu();
        },
        send() {
            this.$emit("send");
        },
    },
}
</script>
