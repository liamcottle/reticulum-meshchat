<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">

        <!-- search -->
        <div v-if="propagationNodes.length > 0" class="flex bg-white p-1 border-b border-gray-300">
            <input v-model="searchTerm" type="text" :placeholder="`Search ${propagationNodes.length} Propagation Nodes...`" class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
        </div>

        <!-- propagation nodes -->
        <div class="h-full overflow-y-auto">
            <div v-if="searchedPropagationNodes.length > 0" class="p-2 space-y-2 w-full">
                <div v-for="propagationNode of searchedPropagationNodes" class="border rounded bg-white shadow">
                    <div class="p-1 flex">
                        <div class="my-auto">
                            <div class="font-semibold">{{ propagationNode.operator_display_name ?? "Unknown Operator" }}</div>
                            <div class="text-sm"><{{ propagationNode.destination_hash }}></div>
                        </div>
                        <div class="ml-auto my-auto">
                            <button v-if="config.lxmf_preferred_propagation_node_destination_hash === propagationNode.destination_hash" @click="stopUsingPropagationNode" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-red-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
                                Stop Using Node
                            </button>
                            <button v-else @click="usePropagationNode(propagationNode.destination_hash)" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Set as Preferred
                            </button>
                        </div>
                    </div>
                    <div class="bg-gray-50 p-1">
                        <div class="text-gray-500 text-sm">
                            <span>Announced {{ formatTimeAgo(propagationNode.updated_at) }}</span>
                            <span v-if="propagationNode.is_propagation_enabled === false">
                                <span> • <span class="text-red-500">Disabled by Operator</span></span>
                            </span>
                            <span v-if="config.lxmf_preferred_propagation_node_destination_hash === propagationNode.destination_hash">
                                <span> • <span class="text-green-500">Preferred</span></span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="flex h-full">
                <div class="mx-auto my-auto text-center leading-5">

                    <!-- no propagation nodes at all -->
                    <div v-if="propagationNodes.length === 0" class="flex flex-col">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H6.911a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Propagation Nodes</div>
                        <div>Check back later, once someone has announced.</div>
                        <div class="mt-2">
                            <button @click="loadPropagationNodes" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                Reload
                            </button>
                        </div>
                    </div>

                    <!-- is searching, but no results -->
                    <div v-if="searchTerm !== '' && propagationNodes.length > 0" class="flex flex-col">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Search Results</div>
                        <div>Your search didn't match any Propagation Nodes!</div>
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
    name: 'PropagationNodesPage',
    data() {
        return {
            searchTerm: "",
            propagationNodes: [],
            config: {
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
        this.loadPropagationNodes();

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
        async loadPropagationNodes() {
            try {
                const response = await window.axios.get(`/api/v1/lxmf/propagation-nodes`, {
                    params: {
                        limit: 500,
                    },
                });
                this.propagationNodes = response.data.lxmf_propagation_nodes;
            } catch(e) {
                // do nothing if failed to load
            }
        },
        async usePropagationNode(destination_hash) {
            await this.updateConfig({
                lxmf_preferred_propagation_node_destination_hash: destination_hash,
            });
        },
        async stopUsingPropagationNode() {
            await this.updateConfig({
                lxmf_preferred_propagation_node_destination_hash: null,
            });
        },
        formatTimeAgo: function(datetimeString) {
            return Utils.formatTimeAgo(datetimeString);
        },
    },
    computed: {
        searchedPropagationNodes() {
            return this.propagationNodes.filter((propagationNode) => {
                const search = this.searchTerm.toLowerCase();
                const matchesOperatorDisplayName = propagationNode.operator_display_name?.toLowerCase()?.includes(search) ?? false;
                const matchesDestinationHash = propagationNode.destination_hash.toLowerCase().includes(search);
                return matchesOperatorDisplayName || matchesDestinationHash;
            });
        },
    },
}
</script>
