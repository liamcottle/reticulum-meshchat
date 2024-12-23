<template>
    <div class="flex flex-col w-80 min-w-80">

        <!-- tabs -->
        <div class="bg-white dark:bg-zinc-950 border-b border-r border-gray-200 dark:border-zinc-700">
            <div class="-mb-px flex">
                <div @click="tab = 'conversations'" class="w-full border-b-2 py-3 px-1 text-center text-sm font-medium cursor-pointer" :class="[ tab === 'conversations' ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 dark:hover:border-zinc-600 hover:text-gray-700 dark:hover:text-gray-300']">Conversations</div>
                <div @click="tab = 'announces'" class="w-full border-b-2 py-3 px-1 text-center text-sm font-medium cursor-pointer" :class="[ tab === 'announces' ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 dark:hover:border-zinc-600 hover:text-gray-700 dark:hover:text-gray-300']">Announces</div>
            </div>
        </div>

        <!-- conversations -->
        <div v-if="tab === 'conversations'" class="flex-1 flex flex-col bg-white dark:bg-zinc-950 border-r border-gray-200 dark:border-zinc-700 overflow-hidden">

            <!-- search -->
            <div v-if="conversations.length > 0" class="p-1 border-b border-gray-300 dark:border-zinc-700">
                <input v-model="conversationsSearchTerm" type="text" :placeholder="`Search ${conversations.length} Conversations...`" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-blue-500 dark:focus:border-blue-600 block w-full p-2.5">
            </div>

            <!-- peers -->
            <div class="flex h-full overflow-y-auto">
                <div v-if="searchedConversations.length > 0" class="w-full">
                    <div @click="onConversationClick(conversation)" v-for="conversation of searchedConversations" class="flex cursor-pointer p-2 border-l-2" :class="[ conversation.destination_hash === selectedDestinationHash ? 'bg-gray-100 dark:bg-zinc-700 border-blue-500 dark:border-blue-400' : 'bg-white dark:bg-zinc-950 border-transparent hover:bg-gray-50 dark:hover:bg-zinc-700 hover:border-gray-200 dark:hover:border-zinc-600' ]">
                        <div class="my-auto mr-2">
                            <div v-if="conversation.lxmf_user_icon" class="p-2 rounded" :style="{ 'color': conversation.lxmf_user_icon.foreground_colour, 'background-color': conversation.lxmf_user_icon.background_colour }">
                                <MaterialDesignIcon :icon-name="conversation.lxmf_user_icon.icon_name" class="w-6 h-6"/>
                            </div>
                            <div v-else class="bg-gray-200 dark:bg-zinc-700 text-gray-500 dark:text-gray-400 p-2 rounded">
                                <MaterialDesignIcon icon-name="account-outline" class="w-6 h-6"/>
                            </div>
                        </div>
                        <div class="mr-auto">
                            <div class="text-gray-900 dark:text-gray-100" :class="{ 'font-semibold': conversation.is_unread || conversation.failed_messages_count > 0 }">{{ conversation.custom_display_name ?? conversation.display_name }}</div>
                            <div class="text-gray-500 dark:text-gray-400 text-sm">{{ formatTimeAgo(conversation.updated_at) }}</div>
                        </div>
                        <div v-if="conversation.is_unread" class="my-auto ml-2 mr-2">
                            <div class="bg-blue-500 dark:bg-blue-400 rounded-full p-1"></div>
                        </div>
                        <div v-else-if="conversation.failed_messages_count" class="my-auto ml-2 mr-2">
                            <div class="bg-red-500 dark:bg-red-400 rounded-full p-1"></div>
                        </div>
                    </div>
                </div>
                <div v-else class="mx-auto my-auto text-center leading-5">

                    <!-- no conversations at all -->
                    <div v-if="conversations.length === 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H6.911a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Conversations</div>
                        <div>Discover peers on the Announces tab</div>
                    </div>

                    <!-- is searching, but no results -->
                    <div v-if="conversationsSearchTerm !== '' && conversations.length > 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Search Results</div>
                        <div>Your search didn't match any Conversations!</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- discover -->
        <div v-if="tab === 'announces'" class="flex-1 flex flex-col bg-white dark:bg-zinc-950 border-r border-gray-200 dark:border-zinc-700 overflow-hidden">

            <!-- search -->
            <div v-if="peersCount > 0" class="p-1 border-b border-gray-300 dark:border-zinc-700">
                <input v-model="peersSearchTerm" type="text" :placeholder="`Search ${peersCount} recent announces...`" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-blue-500 dark:focus:border-blue-600 block w-full p-2.5">
            </div>

            <!-- peers -->
            <div class="flex h-full overflow-y-auto">
                <div v-if="searchedPeers.length > 0" class="w-full">
                    <div @click="onPeerClick(peer)" v-for="peer of searchedPeers" class="flex cursor-pointer p-2 border-l-2" :class="[ peer.destination_hash === selectedDestinationHash ? 'bg-gray-100 dark:bg-zinc-700 border-blue-500 dark:border-blue-400' : 'bg-white dark:bg-zinc-950 border-transparent hover:bg-gray-50 dark:hover:bg-zinc-700 hover:border-gray-200 dark:hover:border-zinc-600' ]">
                        <div class="my-auto mr-2">
                            <div v-if="peer.lxmf_user_icon" class="p-2 rounded" :style="{ 'color': peer.lxmf_user_icon.foreground_colour, 'background-color': peer.lxmf_user_icon.background_colour }">
                                <MaterialDesignIcon :icon-name="peer.lxmf_user_icon.icon_name" class="w-6 h-6"/>
                            </div>
                            <div v-else class="bg-gray-200 dark:bg-zinc-700 text-gray-500 dark:text-gray-400 p-2 rounded">
                                <MaterialDesignIcon icon-name="account-outline" class="w-6 h-6"/>
                            </div>
                        </div>
                        <div>
                            <div class="text-gray-900 dark:text-gray-100">{{ peer.custom_display_name ?? peer.display_name }}</div>
                            <div class="flex space-x-1 text-gray-500 dark:text-gray-400 text-sm">

                                <!-- time ago -->
                                <span class="flex my-auto space-x-1">
                                    {{ formatTimeAgo(peer.updated_at) }}
                                </span>

                                <!-- hops away (only shown for peers heard directly) -->
                                <span v-if="peer.hops != null && (peer.hops === 0 || peer.hops === 1)" class="flex my-auto text-sm text-gray-500 space-x-1">
                                    <span>• Direct</span>
                                </span>

                                <!-- snr (only shown for peers directly heard on rf) -->
                                <span v-if="peer.snr != null && (peer.hops === 0 || peer.hops === 1)" class="flex my-auto space-x-1">
                                    <span>•</span>
                                    <span>SNR {{ peer.snr }}</span>
                                </span>

                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="mx-auto my-auto text-center leading-5">

                    <!-- no peers at all -->
                    <div v-if="peersCount === 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Peers Discovered</div>
                        <div>Waiting for someone to announce!</div>
                    </div>

                    <!-- is searching, but no results -->
                    <div v-if="peersSearchTerm !== '' && peersCount > 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Search Results</div>
                        <div>Your search didn't match any Peers!</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import MaterialDesignIcon from "../MaterialDesignIcon.vue";

export default {
    name: 'MessagesSidebar',
    components: {MaterialDesignIcon},
    props: {
        peers: Object,
        conversations: Array,
        selectedDestinationHash: String,
    },
    data() {
        return {
            tab: "conversations",
            conversationsSearchTerm: "",
            peersSearchTerm: "",
        };
    },
    methods: {
        onConversationClick(conversation) {
            this.$emit("conversation-click", conversation);
        },
        onPeerClick(peer) {
            this.$emit("peer-click", peer);
        },
        formatTimeAgo: function(datetimeString) {
            return Utils.formatTimeAgo(datetimeString);
        },
    },
    computed: {
        searchedConversations() {
            return this.conversations.filter((conversation) => {
                const search = this.conversationsSearchTerm.toLowerCase();
                const matchesDisplayName = conversation.display_name.toLowerCase().includes(search);
                const matchesCustomDisplayName = conversation.custom_display_name?.toLowerCase()?.includes(search) === true;
                const matchesDestinationHash = conversation.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesCustomDisplayName || matchesDestinationHash;
            });
        },
        peersCount() {
            return Object.keys(this.peers).length;
        },
        peersOrderedByLatestAnnounce() {
            const peers = Object.values(this.peers);
            return peers.sort(function(peerA, peerB) {
                // order by updated_at desc
                const peerAUpdatedAt = new Date(peerA.updated_at).getTime();
                const peerBUpdatedAt = new Date(peerB.updated_at).getTime();
                return peerBUpdatedAt - peerAUpdatedAt;
            });
        },
        searchedPeers() {
            return this.peersOrderedByLatestAnnounce.filter((peer) => {
                const search = this.peersSearchTerm.toLowerCase();
                const matchesDisplayName = peer.display_name.toLowerCase().includes(search);
                const matchesCustomDisplayName = peer.custom_display_name?.toLowerCase()?.includes(search) === true;
                const matchesDestinationHash = peer.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesCustomDisplayName || matchesDestinationHash;
            });
        },
    },
}
</script>
