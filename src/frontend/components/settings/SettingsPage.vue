<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- failed messages -->
            <div class="bg-white rounded shadow">
                <div class="flex border-b border-gray-300 text-gray-700 p-2 font-semibold">Failed Messages</div>
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

                </div>
            </div>

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

        </div>
    </div>
</template>

<script>
export default {
    name: 'SettingsPage',
    data() {
        return {
            config: {
                auto_resend_failed_messages_when_announce_received: null,
                allow_auto_resending_failed_messages_with_attachments: null,
                show_suggested_community_interfaces: null,
            },
        };
    },
    mounted() {
        this.getConfig();
    },
    methods: {
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
        async onShowSuggestedCommunityInterfacesChange() {
            await this.updateConfig({
                "show_suggested_community_interfaces": this.config.show_suggested_community_interfaces,
            });
        },
    },
}
</script>
