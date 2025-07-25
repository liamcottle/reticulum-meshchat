<template>
    <div class="flex flex-col w-80 min-w-80">

        <!-- tabs -->
        <div class="bg-white dark:bg-zinc-950 border-b border-r border-gray-200 dark:border-zinc-700">
            <div class="-mb-px flex">
                <div @click="tab = 'favourites'" class="w-full border-b-2 py-3 px-1 text-center text-sm font-medium cursor-pointer" :class="[ tab === 'favourites' ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 dark:hover:border-zinc-600 hover:text-gray-700 dark:hover:text-gray-300']">Favourites</div>
                <div @click="tab = 'announces'" class="w-full border-b-2 py-3 px-1 text-center text-sm font-medium cursor-pointer" :class="[ tab === 'announces' ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 dark:hover:border-zinc-600 hover:text-gray-700 dark:hover:text-gray-300']">Announces</div>
            </div>
        </div>

        <!-- favourites -->
        <div v-if="tab === 'favourites'" class="flex-1 flex flex-col bg-white dark:bg-zinc-950 border-r border-gray-200 dark:border-zinc-700 overflow-hidden">

            <!-- search -->
            <div v-if="favourites.length > 0" class="p-1 border-b border-gray-300 dark:border-zinc-700">
                <input v-model="favouritesSearchTerm" type="text" :placeholder="`Search ${favourites.length} Favourites...`" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-blue-500 dark:focus:border-blue-600 block w-full p-2.5">
            </div>

            <!-- peers -->
            <div class="flex h-full overflow-y-auto">
                <div v-if="searchedFavourites.length > 0" class="w-full">
                    <div @click="onFavouriteClick(favourite)" v-for="favourite of searchedFavourites" class="flex cursor-pointer p-2 border-l-2" :class="[ favourite.destination_hash === selectedDestinationHash ? 'bg-gray-100 dark:bg-zinc-700 border-blue-500 dark:border-blue-400' : 'bg-white dark:bg-zinc-950 border-transparent hover:bg-gray-50 dark:hover:bg-zinc-700 hover:border-gray-200 dark:hover:border-zinc-600' ]">
                        <div class="my-auto mr-2">
                            <div class="bg-gray-200 dark:bg-zinc-800 text-gray-500 dark:text-gray-400 p-2 rounded">
                                <MaterialDesignIcon icon-name="server-network-outline" class="w-6 h-6"/>
                            </div>
                        </div>
                        <div>
                            <div class="text-gray-900 dark:text-gray-100">{{ favourite.display_name }}</div>
                            <div class="text-gray-500 dark:text-gray-400 text-sm">{{ formatDestinationHash(favourite.destination_hash) }}</div>
                        </div>
                    </div>
                </div>
                <div v-else class="mx-auto my-auto text-center leading-5">

                    <!-- no favourites at all -->
                    <div v-if="favourites.length === 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Favourites</div>
                        <div>Discover nodes on the Announces tab.</div>
                    </div>

                    <!-- is searching, but no results -->
                    <div v-if="favouritesSearchTerm !== '' && favourites.length > 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Search Results</div>
                        <div>Your search didn't match any Favourites!</div>
                    </div>

                </div>
            </div>
        </div>

        <!-- announces -->
        <div v-if="tab === 'announces'" class="flex-1 flex flex-col bg-white dark:bg-zinc-950 border-r dark:border-zinc-800 overflow-hidden">
            <!-- search -->
            <div v-if="nodesCount > 0" class="p-1 border-b border-gray-300 dark:border-zinc-800">
                <input 
                    v-model="nodesSearchTerm" 
                    type="text" 
                    :placeholder="`Search ${nodesCount} Nodes...`" 
                    class="bg-gray-50 dark:bg-zinc-900 border border-gray-300 dark:border-zinc-700 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400"
                >
            </div>
            <!-- nodes -->
            <div class="flex h-full overflow-y-auto">
                <div v-if="searchedNodes.length > 0" class="w-full">
                    <div 
                        @click="onNodeClick(node)" 
                        v-for="node of searchedNodes" 
                        class="flex cursor-pointer p-2 border-l-2" 
                        :class="[ 
                            node.destination_hash === selectedDestinationHash 
                                ? 'bg-gray-100 dark:bg-zinc-800 border-blue-500' 
                                : 'bg-white dark:bg-zinc-950 border-transparent hover:bg-gray-50 dark:hover:bg-zinc-900 hover:border-gray-200 dark:hover:border-zinc-700' 
                        ]"
                    >
                        <div class="my-auto mr-2">
                            <div class="bg-gray-200 dark:bg-zinc-800 text-gray-500 dark:text-gray-400 p-2 rounded">
                                <MaterialDesignIcon icon-name="server-network-outline" class="w-6 h-6"/>
                            </div>
                        </div>
                        <div>
                            <div class="text-gray-900 dark:text-gray-100">{{ node.display_name }}</div>
                            <div class="text-gray-500 dark:text-gray-400 text-sm">{{ formatTimeAgo(node.updated_at) }}</div>
                        </div>
                    </div>
                </div>
                <div v-else class="mx-auto my-auto text-center leading-5">
                    <!-- no nodes at all -->
                    <div v-if="nodesCount === 0" class="flex flex-col">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-gray-500 dark:text-gray-400">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                            </svg>
                        </div>
                        <div class="font-semibold text-gray-900 dark:text-gray-100">No Nodes Discovered</div>
                        <div class="text-gray-500 dark:text-gray-400">Waiting for a node to announce!</div>
                    </div>
                    <!-- is searching, but no results -->
                    <div v-if="nodesSearchTerm !== '' && nodesCount > 0" class="flex flex-col">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-gray-500 dark:text-gray-400">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold text-gray-900 dark:text-gray-100">No Search Results</div>
                        <div class="text-gray-500 dark:text-gray-400">Your search didn't match any Nodes!</div>
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
    name: 'NomadNetworkSidebar',
    components: {MaterialDesignIcon},
    props: {
        nodes: Object,
        favourites: Array,
        selectedDestinationHash: String,
    },
    data() {
        return {
            tab: "favourites",
            favouritesSearchTerm: "",
            nodesSearchTerm: "",
        };
    },
    methods: {
        onNodeClick(node) {
            this.$emit("node-click", node);
        },
        onFavouriteClick(favourite) {
            this.onNodeClick(favourite);
        },
        formatTimeAgo: function(datetimeString) {
            return Utils.formatTimeAgo(datetimeString);
        },
        formatDestinationHash: function(destinationHash) {
            return Utils.formatDestinationHash(destinationHash);
        },
    },
    computed: {
        nodesCount() {
            return Object.keys(this.nodes).length;
        },
        nodesOrderedByLatestAnnounce() {
            const nodes = Object.values(this.nodes);
            return nodes.sort(function(nodeA, nodeB) {
                // order by updated_at desc
                const nodeAUpdatedAt = new Date(nodeA.updated_at).getTime();
                const nodeBUpdatedAt = new Date(nodeB.updated_at).getTime();
                return nodeBUpdatedAt - nodeAUpdatedAt;
            });
        },
        searchedNodes() {
            return this.nodesOrderedByLatestAnnounce.filter((node) => {
                const search = this.nodesSearchTerm.toLowerCase();
                const matchesDisplayName = node.display_name.toLowerCase().includes(search);
                const matchesDestinationHash = node.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesDestinationHash;
            });
        },
        searchedFavourites() {
            return this.favourites.filter((favourite) => {
                const search = this.favouritesSearchTerm.toLowerCase();
                const matchesDisplayName = favourite.display_name.toLowerCase().includes(search);
                const matchesCustomDisplayName = favourite.custom_display_name?.toLowerCase()?.includes(search) === true;
                const matchesDestinationHash = favourite.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesCustomDisplayName || matchesDestinationHash;
            });
        },
    },
}
</script>
