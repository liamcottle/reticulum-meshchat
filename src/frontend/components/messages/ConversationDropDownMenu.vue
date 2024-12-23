<template>
    <DropDownMenu>
        <template v-slot:button>
            <IconButton>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                </svg>
            </IconButton>
        </template>
        <template v-slot:items>

            <!-- call button -->
            <a :href="`call.html?destination_hash=${peer.destination_hash}`" target="_blank">
                <DropDownMenuItem>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                        <path fill-rule="evenodd" d="M1.5 4.5a3 3 0 0 1 3-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 0 1-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 0 0 6.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 0 1 1.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 0 1-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 6.75V4.5Z" clip-rule="evenodd" />
                    </svg>
                    <span>Start a Call</span>
                </DropDownMenuItem>
            </a>

            <!-- ping button -->
            <DropDownMenuItem @click="onPingDestination">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                    <path fill-rule="evenodd" d="M14.615 1.595a.75.75 0 0 1 .359.852L12.982 9.75h7.268a.75.75 0 0 1 .548 1.262l-10.5 11.25a.75.75 0 0 1-1.272-.71l1.992-7.302H3.75a.75.75 0 0 1-.548-1.262l10.5-11.25a.75.75 0 0 1 .913-.143Z" clip-rule="evenodd" />
                </svg>
                <span>Ping Destination</span>
            </DropDownMenuItem>

            <!-- set custom display name button -->
            <DropDownMenuItem @click="onSetCustomDisplayName">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                    <path fill-rule="evenodd" d="M5.25 2.25a3 3 0 0 0-3 3v4.318a3 3 0 0 0 .879 2.121l9.58 9.581c.92.92 2.39 1.186 3.548.428a18.849 18.849 0 0 0 5.441-5.44c.758-1.16.492-2.629-.428-3.548l-9.58-9.581a3 3 0 0 0-2.122-.879H5.25ZM6.375 7.5a1.125 1.125 0 1 0 0-2.25 1.125 1.125 0 0 0 0 2.25Z" clip-rule="evenodd" />
                </svg>
                <span>Set Custom Display Name</span>
            </DropDownMenuItem>

            <!-- delete message history button -->
            <div class="border-t">
                <DropDownMenuItem @click="onDeleteMessageHistory">
                    <svg class="size-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-red-500">Delete Message History</span>
                </DropDownMenuItem>
            </div>

        </template>
    </DropDownMenu>
</template>

<script>
import DropDownMenu from "../DropDownMenu.vue";
import DropDownMenuItem from "../DropDownMenuItem.vue";
import IconButton from "../IconButton.vue";
import DialogUtils from "../../js/DialogUtils";

export default {
    name: 'ConversationDropDownMenu',
    components: {
        IconButton,
        DropDownMenuItem,
        DropDownMenu,
    },
    props: {
        peer: Object,
    },
    emits: [
        "conversation-deleted",
        "set-custom-display-name",
    ],
    methods: {
        async onDeleteMessageHistory() {

            // ask user to confirm deleting conversation history
            if(!confirm("Are you sure you want to delete all messages in this conversation? This can not be undone!")){
                return;
            }

            // delete all lxmf messages from "us to destination" and from "destination to us"
            try {
                await window.axios.delete(`/api/v1/lxmf-messages/conversation/${this.peer.destination_hash}`);
            } catch(e) {
                DialogUtils.alert("failed to delete conversation");
                console.log(e);
            }

            // fire callback
            this.$emit("conversation-deleted");

        },
        async onSetCustomDisplayName() {
            this.$emit("set-custom-display-name");
        },
        async onPingDestination() {
            try {

                // ping destination
                const response = await window.axios.get(`/api/v1/ping/${this.peer.destination_hash}/lxmf.delivery`, {
                    params: {
                        timeout: 30,
                    },
                });

                const pingResult = response.data.ping_result;
                const rttMilliseconds = (pingResult.rtt * 1000).toFixed(3);
                const rttDurationString = `${rttMilliseconds} ms`;

                const info = [
                    `Valid reply from ${this.peer.destination_hash}`,
                    `Duration: ${rttDurationString}`,
                    `Hops There: ${pingResult.hops_there}`,
                    `Hops Back: ${pingResult.hops_back}`,
                ];

                // add signal quality if available
                if(pingResult.quality != null){
                    info.push(`Signal Quality: ${pingResult.quality}%`);
                }

                // add rssi if available
                if(pingResult.rssi != null){
                    info.push(`RSSI: ${pingResult.rssi}dBm`);
                }

                // add snr if available
                if(pingResult.snr != null){
                    info.push(`SNR: ${pingResult.snr}dB`);
                }

                // show result
                DialogUtils.alert(info.join("\n"));

            } catch(e) {
                console.log(e);
                const message = e.response?.data?.message ?? "Ping failed. Try again later";
                DialogUtils.alert(message);
            }
        },
    },
}
</script>
