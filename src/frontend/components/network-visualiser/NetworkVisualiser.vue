<template>
    <div class="flex-1 h-full min-w-full sm:min-w-[500px] relative">

        <!-- network -->
        <div id="network" class="w-full h-full"></div>

        <!-- loading -->
        <div v-if="isLoading" class="absolute flex top-0 bottom-0 left-0 right-0 bg-gray-100">
            <div class="flex flex-col mx-auto my-auto">
                <div class="mx-auto">
                    <svg class="animate-spin h-6 w-6 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </div>
                <div>Loading {{ loadingProgress }}%</div>
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
            isLoading: false,
            loadingProgress: 0,
            reloadInterval: null,
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

            this.isLoading = true;

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

            // update loading progress
            this.network.on("stabilizationProgress", (event) => {

                // calculate percentage stabilized
                this.loadingProgress = Math.floor((event.iterations / event.total) * 100);

            });

            // update network
            await this.update();

            // stabilise the network a bit after first load
            this.network.stabilize();
            this.isLoading = false;

            // auto update network
            this.reloadInterval = setInterval(() => {
                this.update();
            }, 10000);

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

                const node = {
                    id: entry.hash,
                    group: "announce",
                    size: 20,
                };

                if(announce.aspect === "lxmf.delivery"){

                    const name = announce.app_data ? atob(announce.app_data) : "Anonymous Peer";

                    node.shape = "circularImage";
                    node.image = entry.hops === 1 ? "/assets/images/network-visualiser/user_1hop.png" : "/assets/images/network-visualiser/user.png";

                    node.label = name;
                    node.title = [
                        `Name: ${name}`,
                        `Aspect: ${announce.aspect}`,
                        `Identity: ${announce.identity_hash}`,
                        `Destination: ${announce.destination_hash}`,
                        `Path: ${entry.hops} ${entry.hops === 1 ? 'Hop' : 'Hops'} via ${entry.interface}`,
                        `Announced At: ${announce.updated_at}`,
                    ].join("\n");

                }

                if(announce.aspect === "nomadnetwork.node"){

                    const name = announce.app_data ? atob(announce.app_data) : "Anonymous Node";

                    node.shape = "circularImage";
                    node.image = entry.hops === 1 ? "/assets/images/network-visualiser/server_1hop.png" : "/assets/images/network-visualiser/server.png";

                    node.label = name;
                    node.title = [
                        `Name: ${name}`,
                        `Aspect: ${announce.aspect}`,
                        `Identity: ${announce.identity_hash}`,
                        `Destination: ${announce.destination_hash}`,
                        `Path: ${entry.hops} ${entry.hops === 1 ? 'Hop' : 'Hops'} via ${entry.interface}`,
                        `Announced At: ${announce.updated_at}`,
                    ].join("\n");

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

            // update nodes
            const oldNodeIds = this.nodes.map((node) => node.id);
            const newNodeIds = newNodes.map((node) => node.id);
            this.nodes.update(newNodes);

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
                    this.edges.remove(oldNodeId);
                }
            }

        },
        processNewEdges(newEdges) {

            // update edges
            const oldEdgeIds = this.edges.map((edge) => edge.id);
            const newEdgeIds = newEdges.map((edge) => edge.id);
            this.edges.update(newEdges);

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

        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
        formatBitsPerSecond: function(bits) {
            return Utils.formatBitsPerSecond(bits);
        },
    },
}
</script>
