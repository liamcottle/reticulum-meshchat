<template>
    <div class="flex-1 h-full min-w-full sm:min-w-[500px] relative">

        <!-- network -->
        <div id="network" class="w-full h-full"></div>

        <!-- controls -->
        <div class="absolute flex bottom-0 left-0 bg-gray-100 p-2">
            <div class="bg-white rounded shadow min-w-52">
                <div @click="isShowingControls = !isShowingControls" class="flex text-gray-700 p-2 cursor-pointer">
                    <div class="my-auto">Reticulum Network</div>
                    <div class="flex ml-auto">
                        <button @click.stop="update" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-1 py-0.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                            </svg>
                        </button>
                    </div>
                </div>
                <div v-if="isShowingControls" class="divide-y text-gray-900 border-t border-gray-300">
                    <div class="px-1 py-2">
                        <div class="flex items-start">
                            <div class="flex items-center h-5">
                                <input v-model="autoReload" type="checkbox" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300">
                            </div>
                            <label class="ml-2 text-sm font-medium text-gray-900">Auto Update (5 sec)</label>
                        </div>
                    </div>
                    <div class="p-1">
                        <div>Interfaces</div>
                        <div class="text-sm text-gray-700">{{ onlineInterfaces.length }} Online, {{ offlineInterfaces.length }} Offline</div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style>
.vis-tooltip {
    color: white !important;
    background: rgba(0, 0, 0, 0.75) !important;
}
</style>

<script>
import "vis-network/styles/vis-network.css";
import { Network } from "vis-network";
import { DataSet } from "vis-data";
import Utils from "../../js/Utils";
export default {
    name: 'NetworkVisualiser',
    data() {
        return {
            config: null,
            autoReload: false,
            reloadInterval: null,
            isShowingControls: true,
            interfaces: [],
            pathTable: [],
            announces: {},
            network: null,
            nodes: new DataSet(),
            edges: new DataSet(),
        };
    },
    beforeUnmount() {
        clearInterval(this.reloadInterval);
    },
    mounted() {
        this.init();
    },
    methods: {
        async getInterfaceStats() {
            try {
                const response = await axios.get(`/api/v1/interface-stats`);
                this.interfaces = response.data.interface_stats?.interfaces ?? [];
            } catch(e) {
                console.log(e);
            }
        },
        async getPathTable() {
            try {
                const response = await axios.get(`/api/v1/path-table`);
                this.pathTable = response.data.path_table;
            } catch(e) {
                console.log(e);
            }
        },
        async getConfig() {
            try {
                const response = await axios.get("/api/v1/config");
                this.config = response.data.config;
            } catch(e) {
                console.error(e);
            }
        },
        async getAnnounces() {
            try {

                // fetch announces
                const response = await window.axios.get(`/api/v1/announces`);

                // cache announces
                this.announces = {};
                for(const announce of response.data.announces){
                    this.announces[announce.destination_hash] = announce;
                }

            } catch(e) {
                // do nothing if failed to load announces
                console.log(e);
            }
        },
        async init() {

            // create network ui
            const container = document.getElementById("network");
            this.network = new Network(container, {
                nodes: this.nodes,
                edges: this.edges,
            }, {
                interaction: {
                    tooltipDelay: 0, // show tooltip instantly on hover
                },
                layout: {
                    // always layout nodes the same way across reloads if nothing changed
                    randomSeed: 1,
                },
                nodes: {
                    color: {
                        border: "#000000",
                        highlight: {
                            border: "#000000",
                        },
                    },
                },
                physics: {
                    barnesHut: {
                        gravitationalConstant: -5000,
                        // centralGravity: 0,
                        // springConstant: 0.1,
                        // damping: 0.15,
                    },
                    // maxVelocity: 150,
                    // minVelocity: 0.25,
                },
                groups: {
                    "me": {
                        shape: "image",
                        image: "/assets/images/reticulum_logo_512.png",
                    },
                    "interface": {

                    },
                    "announce": {

                    },
                },
            });

            // update network
            await this.update();

            // fit network after initial load
            setTimeout(() => {
                this.network.fit({
                    animation: true,
                });
            }, 2000);

            // auto reload
            this.reloadInterval = setInterval(this.onAutoReload, 5000);

        },
        async onAutoReload() {

            // do nothing if auto reload disabled
            if(!this.autoReload){
                return;
            }

            // do nothing if already updating
            if(this.isUpdating){
                return;
            }

            // auto reload
            try {
                this.isUpdating = true;
                await this.update();
            } finally {
                this.isUpdating = false;
            }

        },
        async update() {

            await this.getConfig();
            await this.getInterfaceStats();
            await this.getPathTable();
            await this.getAnnounces();

            const nodes = [];
            const edges = [];

            // add me
            nodes.push({
                id: "me",
                group: "me",
                size: 60,
                label: this.config?.display_name ?? "This Device",
                title: [
                    `${this.config?.display_name ?? 'This Device'}`,
                    `Identity: ${this.config?.identity_hash ?? 'Unknown'}`,
                ].join("\n"),
                font: {
                    color: "#000000",
                    background: "#ffffff",
                },
            });

            // add interfaces
            for(const entry of this.interfaces){

                // determine label
                var label = entry.interface_name ?? entry.name;

                // we want to show the full info for LocalServerInterface
                // we also want to show the full info instead of just "Client on Name" for TCPServerInterface clients
                if(entry.type === "LocalServerInterface" || entry.parent_interface_name != null){
                    label = entry.name;
                }

                const node = {
                    id: entry.name,
                    group: "interface",
                    label: label,
                    title: [
                        entry.name,
                        `State: ${entry.status ? 'Online' : 'Offline'}`,
                        `Bitrate: ${this.formatBitsPerSecond(entry.bitrate)}`,
                        `TX: ${this.formatBytes(entry.txb)}`,
                        `RX: ${this.formatBytes(entry.rxb)}`,
                    ].join("\n"),
                    size: 30,
                    font: {
                        color: "#000000",
                        background: '#ffffff',
                    },
                    shape: "circularImage",
                    image: entry.status ? "/assets/images/network-visualiser/interface_connected.png" : "/assets/images/network-visualiser/interface_disconnected.png",
                };

                // add interface node
                nodes.push(node);

                // add edge to interface
                if(entry.parent_interface_name){
                    // add edge from parent interface to interface
                    edges.push({
                        id: `${entry.parent_interface_name}~${entry.name}`,
                        from: entry.parent_interface_name,
                        to: entry.name,
                        color: "transparent",
                        length: 300,
                        background: {
                            enabled: true,
                            color: entry.status ? "#22c55e" : "#ef4444",
                        },
                    });
                } else {
                    // add edge from me to interface
                    edges.push({
                        id: `me~${entry.name}`,
                        from: "me",
                        to: entry.name,
                        color: "transparent",
                        length: 300,
                        background: {
                            enabled: true,
                            color: entry.status ? "#22c55e" : "#ef4444",
                        },
                    });
                }

            }

            // add paths for announces
            for(const entry of this.pathTable){

                // skip this path if hops are unknown
                if(entry.hops == null){
                    continue;
                }

                // find what announced this path, or skip showing it for now
                const announce = this.announces[entry.hash];
                if(!announce){
                    continue;
                }

                // skip announces if we don't want to show them
                const aspectsToShow = ["lxmf.delivery", "nomadnetwork.node"];
                if(!aspectsToShow.includes(announce.aspect)){
                    continue;
                }

                const node = {
                    id: entry.hash,
                    group: "announce",
                    size: 20,
                };

                if(announce.aspect === "lxmf.delivery"){

                    const name = announce.custom_display_name ?? announce.display_name;

                    node.shape = "circularImage";
                    node.image = entry.hops === 1 ? "/assets/images/network-visualiser/user_1hop.png" : "/assets/images/network-visualiser/user.png";

                    node.label = name;
                    node.title = [
                        `Name: ${announce.display_name}`,
                        announce.custom_display_name != null ? `Custom Name: ${announce.custom_display_name}` : null,
                        `Aspect: ${announce.aspect}`,
                        `Identity: ${announce.identity_hash}`,
                        `Destination: ${announce.destination_hash}`,
                        `Path: ${entry.hops} ${entry.hops === 1 ? 'Hop' : 'Hops'} via ${entry.interface}`,
                        `Announced At: ${announce.updated_at}`,
                    ].filter((line) => line != null).join("\n");

                }

                if(announce.aspect === "nomadnetwork.node"){

                    const name = announce.custom_display_name ?? announce.display_name;

                    node.shape = "circularImage";
                    node.image = entry.hops === 1 ? "/assets/images/network-visualiser/server_1hop.png" : "/assets/images/network-visualiser/server.png";

                    node.label = name;
                    node.title = [
                        `Name: ${announce.display_name}`,
                        announce.custom_display_name != null ? `Custom Name: ${announce.custom_display_name}` : null,
                        `Aspect: ${announce.aspect}`,
                        `Identity: ${announce.identity_hash}`,
                        `Destination: ${announce.destination_hash}`,
                        `Path: ${entry.hops} ${entry.hops === 1 ? 'Hop' : 'Hops'} via ${entry.interface}`,
                        `Announced At: ${announce.updated_at}`,
                    ].filter((line) => line != null).join("\n");

                }

                // add node
                nodes.push(node);

                // add edge from interface to announced aspect
                edges.push({
                    id: `${entry.interface}~${entry.hash}`,
                    from: entry.interface,
                    to: entry.hash,
                    color: "gray",
                });

            }

            // process nodes and edges
            this.processNewNodes(nodes);
            this.processNewEdges(edges);

        },
        processNewNodes(newNodes) {

            // determine old and new nodes
            const oldNodeIds = this.nodes.map((node) => node.id);
            const newNodeIds = newNodes.map((node) => node.id);

            // log new nodes
            for(const newNodeId of newNodeIds){
                if(!oldNodeIds.includes(newNodeId)){
                    console.log("Added Node: " + newNodeId);
                }
            }

            // remove old nodes that no longer exist
            for(const oldNodeId of oldNodeIds){
                if(!newNodeIds.includes(oldNodeId)){
                    console.log("Removed Node: " + oldNodeId);
                    this.nodes.remove(oldNodeId);
                }
            }

            // update nodes
            this.nodes.update(newNodes);

        },
        processNewEdges(newEdges) {

            // determine old and new edges
            const oldEdgeIds = this.edges.map((edge) => edge.id);
            const newEdgeIds = newEdges.map((edge) => edge.id);

            // log new edges
            for(const newEdgeId of newEdgeIds){
                if(!oldEdgeIds.includes(newEdgeId)){
                    console.log("Added Edge: " + newEdgeId);
                }
            }

            // remove old edges that no longer exist
            for(const oldEdgeId of oldEdgeIds){
                if(!newEdgeIds.includes(oldEdgeId)){
                    console.log("Removed Edge: " + oldEdgeId);
                    this.edges.remove(oldEdgeId);
                }
            }

            // update edges
            this.edges.update(newEdges);

        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
        formatBitsPerSecond: function(bits) {
            return Utils.formatBitsPerSecond(bits);
        },
    },
    computed: {
        onlineInterfaces() {
            return this.interfaces.filter((iface) => {
                return iface.status;
            });
        },
        offlineInterfaces() {
            return this.interfaces.filter((iface) => {
                return !iface.status;
            });
        },
    },
}
</script>
