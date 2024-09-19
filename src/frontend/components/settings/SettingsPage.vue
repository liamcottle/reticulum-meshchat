<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- interfaces -->
            <div class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">Interfaces</div>
                <div class="divide-y text-gray-900">

                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input v-model="config.show_suggested_community_interfaces" @change="onShowSuggestedCommunityInterfacesChange" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300">
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900">Show Community Interfaces</label>
                        </div>
                        <div class="text-sm text-gray-700">When enabled, community interfaces will be shown on the Add Interface page.</div>
                    </div>

                </div>
            </div>

            <!-- messages -->
            <div class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">Messages</div>
                <div class="divide-y text-gray-900">

                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input v-model="config.auto_resend_failed_messages_when_announce_received" @change="onAutoResendFailedMessagesWhenAnnounceReceivedChange" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300">
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900">Auto resend</label>
                        </div>
                        <div class="text-sm text-gray-700">When enabled, failed messages will auto resend when an announce is received from the intended destination.</div>
                    </div>

                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input v-model="config.allow_auto_resending_failed_messages_with_attachments" @change="onAllowAutoResendingFailedMessagesWithAttachmentsChange" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300">
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900">Allow resending with attachments</label>
                        </div>
                        <div class="text-sm text-gray-700">When enabled, failed messages that have attachments are allowed to auto resend.</div>
                    </div>

                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input v-model="config.auto_send_failed_messages_to_propagation_node" @change="onAutoSendFailedMessagesToPropagationNodeChange" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300">
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900">Auto send to propagation node</label>
                        </div>
                        <div class="text-sm text-gray-700">When enabled, messages that fail to send will be sent to the configured propagation node.</div>
                    </div>

                </div>
            </div>

            <!-- propagation nodes -->
            <div class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">
                    <div class="my-auto mr-auto">Propagation Nodes</div>
                    <div class="my-auto">
                        <RouterLink :to="{ name: 'propagation-nodes' }" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                            Browse Nodes
                        </RouterLink>
                    </div>
                </div>
                <div class="divide-y text-gray-900">

                    <div class="p-2">
                        <div class="text-sm text-gray-700">
                            <ul class="list-disc list-inside">
                                <li>When you send a message, the intended recipient may be offline and your message will fail to send.</li>
                                <li>Instead, messages can be sent to propagation nodes, which store the messages and allow recipients to retrieve them when they're next online.</li>
                                <li>Propagation nodes automatically peer and sync messages with each other, creating an encrypted, distributed message store.</li>
                                <li>By default, propagation nodes store messages for up to 30 days. If the recipient hasn't retrieved it by then, the message will be lost.</li>
                                <li>At this time, delivery reports are unavailable for messages sent to propagation nodes.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="p-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input v-model="config.lxmf_local_propagation_node_enabled" @change="onLxmfLocalPropagationNodeEnabledChange" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300">
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900">Local Propagation Node</label>
                        </div>
                        <div class="text-sm text-gray-700">When enabled, MeshChat will run a Propagation Node and announce it with the following address for other clients to use.</div>
                        <div class="flex">
                            <input disabled v-model="config.lxmf_local_propagation_node_address_hash" type="text" class="bg-gray-200 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                        </div>
                    </div>

                    <div class="p-2">
                        <div class="text-sm font-medium text-gray-900">Preferred Propagation Node</div>
                        <div class="flex">
                            <input v-model="config.lxmf_preferred_propagation_node_destination_hash" @input="onLxmfPreferredPropagationNodeDestinationHashChange" type="text" placeholder="Destination Hash. e.g: a39610c89d18bb48c73e429582423c24" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                        </div>
                        <div class="text-sm text-gray-700">This is the propagation node your messages will be sent to and retrieved from.</div>
                    </div>

                    <div class="p-2">
                        <div class="text-sm font-medium text-gray-900">Auto Sync Interval</div>
                        <div class="flex">
                            <select v-model="config.lxmf_preferred_propagation_node_auto_sync_interval_seconds" @change="onLxmfPreferredPropagationNodeAutoSyncIntervalSecondsChange" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                                <option value="0">Disabled</option>
                                <option value="900">Every 15 Minutes</option>
                                <option value="1800">Every 30 Minutes</option>
                                <option value="3600">Every 1 Hour</option>
                                <option value="10800">Every 3 Hours</option>
                                <option value="21600">Every 6 Hours</option>
                                <option value="43200">Every 12 Hours</option>
                                <option value="86400">Every 24 Hours</option>
                            </select>
                        </div>
                        <div class="text-sm text-gray-700">
                            <span v-if="config.lxmf_preferred_propagation_node_last_synced_at">Last Synced: {{ formatSecondsAgo(config.lxmf_preferred_propagation_node_last_synced_at) }}</span>
                            <span v-else>Last Synced: Never</span>
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
