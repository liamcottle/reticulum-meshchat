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

            <!-- delete message history button -->
            <DropDownMenuItem @click="onDeleteMessageHistory">
                <svg class="size-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z" clip-rule="evenodd" />
                </svg>
                <span class="text-red-500">Delete Message History</span>
            </DropDownMenuItem>

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
    },
}
</script>
