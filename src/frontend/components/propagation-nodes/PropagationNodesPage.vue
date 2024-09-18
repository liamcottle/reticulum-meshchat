<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">

        <!-- header -->
        <div class="flex bg-white p-2 shadow">
            <div class="my-auto">
                <div class="font-semibold">Propagation Nodes</div>
                <div class="text-sm">Showing {{ propagationNodes.length }} recently heard nodes.</div>
            </div>
            <div class="ml-auto my-auto">
                <button @click="loadPropagationNodes" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                    Reload
                </button>
            </div>
        </div>

        <!-- propagation nodes -->
        <div class="overflow-y-auto p-2 space-y-2">
            <div v-for="propagationNode of propagationNodes" class="border rounded bg-white shadow">
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
                        <span v-if="config.lxmf_preferred_propagation_node_destination_hash === propagationNode.destination_hash">
                            <span> • <span class="text-green-500">Preferred</span></span>
                        </span>
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
}
</script>
