<template>
    <div class="flex-1 h-full min-w-full sm:min-w-[500px] relative">

        <!-- network -->
        <div id="network" class="w-full h-full"></div>

        <!-- loading -->
        <div v-if="isLoading" class="absolute flex top-0 bottom-0 left-0 right-0">
            <div class="mx-auto my-auto">
                <svg class="animate-spin h-6 w-6 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
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
import Utils from "../../js/Utils";
export default {
    name: 'NetworkVisualiser',
    data() {
        return {
            config: null,
            isLoading: false,
            interfaces: [],
            pathTable: [],
            announces: {},
        };
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
                alert("failed to load interface stats");
                console.log(e);
            }
        },
        async getPathTable() {
            try {
                const response = await axios.get(`/api/v1/path-table`);
                this.pathTable = response.data.path_table;
            } catch(e) {
                alert("failed to load path table");
                console.log(e);
            }
        },
        async getConfig() {
            try {
                const response = await axios.get("/api/v1/config");
                this.config = response.data.config;
            } catch(e) {
                alert("failed to load config");
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
            await this.update();
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

                const node = {
                    id: entry.name,
                    group: "interface",
                    label: entry.name,
                    title: [
                        `Interface`,
                        `Name: ${entry.name}`,
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

                // add edge from me to interface
                edges.push({
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
                    node.image = "/assets/images/network-visualiser/user.png";

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
                    node.image = "/assets/images/network-visualiser/server.png";

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
                    from: entry.interface,
                    to: entry.hash,
                    color: "gray",
                });

            }

            // create network ui
            const container = document.getElementById("network");
            const network = new Network(container, {
                nodes: nodes,
                edges: edges,
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
                    },
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

            // hide loading once done
            network.on("stabilized", () => {
                this.isLoading = false;
            });

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
