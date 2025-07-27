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
                        <div class="ml-auto my-auto">
                            <DropDownMenu>
                                <template v-slot:button>
                                    <IconButton class="bg-transparent dark:bg-transparent">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                                        </svg>
                                    </IconButton>
                                </template>
                                <template v-slot:items>

                                    <!-- rename button -->
                                    <DropDownMenuItem @click="onRenameFavourite(favourite)">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                                            <path fill-rule="evenodd" d="M5.25 2.25a3 3 0 0 0-3 3v4.318a3 3 0 0 0 .879 2.121l9.58 9.581c.92.92 2.39 1.186 3.548.428a18.849 18.849 0 0 0 5.441-5.44c.758-1.16.492-2.629-.428-3.548l-9.58-9.581a3 3 0 0 0-2.122-.879H5.25ZM6.375 7.5a1.125 1.125 0 1 0 0-2.25 1.125 1.125 0 0 0 0 2.25Z" clip-rule="evenodd" />
                                        </svg>
                                        <span>Rename Favourite</span>
                                    </DropDownMenuItem>

                                    <!-- remove favourite button -->
                                    <div>
                                        <DropDownMenuItem @click="onRemoveFavourite(favourite)">
                                            <svg class="size-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                                                <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z" clip-rule="evenodd" />
                                            </svg>
                                            <span class="text-red-500">Remove Favourite</span>
                                        </DropDownMenuItem>
                                    </div>

                                </template>
                            </DropDownMenu>
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
import DropDownMenu from "../DropDownMenu.vue";
import IconButton from "../IconButton.vue";
import DropDownMenuItem from "../DropDownMenuItem.vue";

export default {
    name: 'NomadNetworkSidebar',
    components: {DropDownMenuItem, IconButton, DropDownMenu, MaterialDesignIcon},
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
        onRenameFavourite(favourite) {
            this.$emit("rename-favourite", favourite);
        },
        onRemoveFavourite(favourite) {
            this.$emit("remove-favourite", favourite);
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
