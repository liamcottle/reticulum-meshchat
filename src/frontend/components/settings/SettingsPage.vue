<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- appearance -->
            <div class="bg-white rounded shadow dark:bg-zinc-950">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold dark:border-zinc-700 dark:text-zinc-200">
                    Appearance
                </div>
                <div class="divide-y text-gray-900 dark:divide-zinc-800 dark:text-zinc-200">
                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input 
                                    v-model="config.dark_mode" 
                                    @change="onDarkModeChange" 
                                    type="checkbox" 
                                    class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 
                                           dark:border-zinc-700 dark:bg-zinc-900 dark:focus:ring-blue-500"
                                >
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900 dark:text-zinc-200">
                                Enable Dark Mode
                            </label>
                        </div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            Enables dark mode for the application
                        </div>
                    </div>
                </div>
            </div>

            <!-- interfaces -->
            <div class="bg-white rounded shadow dark:bg-zinc-950">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold dark:border-zinc-700 dark:text-zinc-200">
                    Interfaces
                </div>
                <div class="divide-y text-gray-900 dark:divide-zinc-800 dark:text-zinc-200">
                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input 
                                    v-model="config.show_suggested_community_interfaces" 
                                    @change="onShowSuggestedCommunityInterfacesChange" 
                                    type="checkbox" 
                                    class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 
                                           dark:border-zinc-700 dark:bg-zinc-900 dark:focus:ring-blue-500"
                                >
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900 dark:text-zinc-200">
                                Show Community Interfaces
                            </label>
                        </div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            When enabled, community interfaces will be shown on the Add Interface page.
                        </div>
                    </div>
                </div>
            </div>

            <!-- messages -->
            <div class="bg-white rounded shadow dark:bg-zinc-950">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold dark:border-zinc-700 dark:text-zinc-200">
                    Messages
                </div>
                <div class="divide-y text-gray-900 dark:divide-zinc-800 dark:text-zinc-200">
                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input 
                                    v-model="config.auto_resend_failed_messages_when_announce_received" 
                                    @change="onAutoResendFailedMessagesWhenAnnounceReceivedChange" 
                                    type="checkbox" 
                                    class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 
                                           dark:border-zinc-700 dark:bg-zinc-900 dark:focus:ring-blue-500"
                                >
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900 dark:text-zinc-200">
                                Auto resend
                            </label>
                        </div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            When enabled, failed messages will auto resend when an announce is received from the intended destination.
                        </div>
                    </div>
                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input 
                                    v-model="config.allow_auto_resending_failed_messages_with_attachments" 
                                    @change="onAllowAutoResendingFailedMessagesWithAttachmentsChange" 
                                    type="checkbox" 
                                    class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 
                                           dark:border-zinc-700 dark:bg-zinc-900 dark:focus:ring-blue-500"
                                >
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900 dark:text-zinc-200">
                                Allow resending with attachments
                            </label>
                        </div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            When enabled, failed messages that have attachments are allowed to auto resend.
                        </div>
                    </div>
                </div>
            </div>

            <!-- propagation nodes -->
            <div class="bg-white rounded shadow dark:bg-zinc-950">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold dark:border-zinc-700 dark:text-zinc-200">
                    Propagation Nodes
                </div>
                <div class="divide-y text-gray-900 dark:divide-zinc-800 dark:text-zinc-200">
                    <div class="p-2">
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            <ul class="list-disc list-inside">
                                <li>When you send a message, the intended recipient may be offline and your message will fail to send.</li>
                                <li>Instead, messages can be sent to propagation nodes, which store the messages and allow recipients to retrieve them when they're next online.</li>
                                <li>Propagation nodes automatically peer and sync messages with each other, creating an encrypted, distributed message store.</li>
                                <li>By default, propagation nodes store messages for up to 30 days. If the recipient hasn't retrieved it by then, the message will be lost.</li>
                                <li>At this time, delivery reports are unavailable for messages sent to propagation nodes.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>


<script>
import Utils from "../../js/Utils";
import WebSocketConnection from "../../js/WebSocketConnection";

export default {
    name: 'SettingsPage',
    data() {
        return {
            config: {
                auto_resend_failed_messages_when_announce_received: null,
                allow_auto_resending_failed_messages_with_attachments: null,
                auto_send_failed_messages_to_propagation_node: null,
                show_suggested_community_interfaces: null,
                lxmf_local_propagation_node_enabled: null,
                lxmf_preferred_propagation_node_destination_hash: null,
            },
        };
    },
    beforeUnmount() {

        // stop listening for websocket messages
        WebSocketConnection.off("message", this.onWebsocketMessage);

    },
    mounted() {

        // listen for websocket messages
        WebSocketConnection.on("message", this.onWebsocketMessage);

        this.getConfig();

    },
    methods: {
        async onWebsocketMessage(message) {
            const json = JSON.parse(message.data);
            switch(json.type){
                case 'config': {
                    this.config = json.config;
                    break;
                }
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
        async updateConfig(config) {
            try {
                const response = await window.axios.patch("/api/v1/config", config);
                this.config = response.data.config;
            } catch(e) {
                alert("Failed to save config!");
                console.log(e);
            }
        },
        async onAutoResendFailedMessagesWhenAnnounceReceivedChange() {
            await this.updateConfig({
                "auto_resend_failed_messages_when_announce_received": this.config.auto_resend_failed_messages_when_announce_received,
            });
        },
        async onAllowAutoResendingFailedMessagesWithAttachmentsChange() {
            await this.updateConfig({
                "allow_auto_resending_failed_messages_with_attachments": this.config.allow_auto_resending_failed_messages_with_attachments,
            });
        },
        async onAutoSendFailedMessagesToPropagationNodeChange() {
            await this.updateConfig({
                "auto_send_failed_messages_to_propagation_node": this.config.auto_send_failed_messages_to_propagation_node,
            });
        },
        async onShowSuggestedCommunityInterfacesChange() {
            await this.updateConfig({
                "show_suggested_community_interfaces": this.config.show_suggested_community_interfaces,
            });
        },
        async onDarkModeChange() {
            await this.updateConfig({
                "dark_mode": this.config.dark_mode,
            });
        },
        async onLxmfPreferredPropagationNodeDestinationHashChange() {
            await this.updateConfig({
                "lxmf_preferred_propagation_node_destination_hash": this.config.lxmf_preferred_propagation_node_destination_hash,
            });
        },
        async onLxmfLocalPropagationNodeEnabledChange() {
            await this.updateConfig({
                "lxmf_local_propagation_node_enabled": this.config.lxmf_local_propagation_node_enabled,
            });
        },
        async onLxmfPreferredPropagationNodeAutoSyncIntervalSecondsChange() {
            await this.updateConfig({
                "lxmf_preferred_propagation_node_auto_sync_interval_seconds": this.config.lxmf_preferred_propagation_node_auto_sync_interval_seconds,
            });
        },
        formatSecondsAgo: function(seconds) {
            return Utils.formatSecondsAgo(seconds);
        },
    },
}
</script>
