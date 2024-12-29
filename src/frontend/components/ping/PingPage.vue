<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="flex flex-col h-full space-y-2 p-2 overflow-y-auto">

            <!-- appearance -->
            <div class="bg-white dark:bg-zinc-800 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-gray-200 p-2 font-semibold">Ping</div>
                <div class="dark:divide-zinc-700 text-gray-900 dark:text-gray-100 p-2">
                    Only lxmf.delivery destinations can be pinged.
                </div>
            </div>

            <!-- inputs -->
            <div class="bg-white dark:bg-zinc-800 rounded shadow">
                <div class="divide-y divide-gray-300 dark:divide-zinc-700 text-gray-900 dark:text-gray-100">

                    <div class="p-2">
                        <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Destination Hash</div>
                        <div class="flex">
                            <input v-model="destinationHash" type="text" placeholder="e.g: 7b746057a7294469799cd8d7d429676a" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-600 dark:focus:border-blue-600 block w-full p-2.5">
                        </div>
                    </div>

                    <div class="p-2">
                        <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Ping Timeout (seconds)</div>
                        <div class="flex">
                            <input v-model="timeout" type="number" placeholder="Timeout" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-600 dark:focus:border-blue-600 block w-full p-2.5">
                        </div>
                    </div>

                    <div class="p-2 space-x-1">
                        <button v-if="!isRunning" @click="start" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:bg-zinc-700 dark:text-white dark:hover:bg-zinc-600 dark:focus-visible:outline-zinc-500">
                            Start
                        </button>
                        <button v-if="isRunning" @click="stop" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:bg-zinc-700 dark:text-white dark:hover:bg-zinc-600 dark:focus-visible:outline-zinc-500">
                            Stop
                        </button>
                        <button @click="clear" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:bg-zinc-700 dark:text-white dark:hover:bg-zinc-600 dark:focus-visible:outline-zinc-500">
                            Clear Results
                        </button>
                        <button @click="dropPath" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-red-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
                            Drop Path
                        </button>
                    </div>

                </div>
            </div>

            <!-- results -->
            <div class="flex flex-col h-full bg-white dark:bg-zinc-800 rounded shadow overflow-hidden min-h-52">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-gray-200 p-2 font-semibold">Results</div>
                <div id="results" class="flex flex-col h-full bg-black text-white dark:bg-zinc-800 dark:text-gray-200 p-2 overflow-y-auto overflow-x-auto font-mono whitespace-nowrap">
                    <div v-for="pingResult of pingResults" class="w-fit">{{ pingResult }}</div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import {CanceledError} from "axios";
import DialogUtils from "../../js/DialogUtils";

export default {
    name: 'PingPage',
    data() {
        return {
            isRunning: false,
            destinationHash: null,
            timeout: 10,
            seq: 0,
            pingResults: [],
            abortController: null,
        };
    },
    beforeUnmount() {
        this.stop();
    },
    methods: {
        async start() {

            // do nothing if already running
            if(this.isRunning){
                return;
            }

            // simple check to ensure destination hash is valid
            if(this.destinationHash == null || this.destinationHash.length !== 32){
                DialogUtils.alert("Invalid Destination Hash!");
                return;
            }

            // simple check to ensure destination hash is valid
            if(this.timeout == null || this.timeout < 0){
                DialogUtils.alert("Timeout must be a number!");
                return;
            }

            // we are now running ping
            this.seq = 0;
            this.isRunning = true;
            this.abortController = new AbortController();

            // run ping until stopped
            while(this.isRunning){

                // run ping
                await this.ping();

                // wait a bit before running next ping
                await this.sleep(1000);

            }

        },
        async stop() {
            this.isRunning = false;
            this.abortController.abort();
        },
        async clear() {
            this.pingResults = [];
        },
        async sleep(millis) {
            return new Promise((resolve, reject) => setTimeout(resolve, millis));
        },
        async ping() {
            try {

                this.seq++;

                // ping destination
                const response = await window.axios.get(`/api/v1/ping/${this.destinationHash}/lxmf.delivery`, {
                    signal: this.abortController.signal,
                    params: {
                        timeout: this.timeout,
                    },
                });

                const pingResult = response.data.ping_result;
                const rttMilliseconds = (pingResult.rtt * 1000).toFixed(3);
                const rttDurationString = `${rttMilliseconds}ms`;

                const info = [
                    `seq=${this.seq}`,
                    `duration=${rttDurationString}`,
                    `hops_there=${pingResult.hops_there}`,
                    `hops_back=${pingResult.hops_back}`,
                ];

                // add rssi if available
                if(pingResult.rssi != null){
                    info.push(`rssi=${pingResult.rssi}dBm`);
                }

                // add snr if available
                if(pingResult.snr != null){
                    info.push(`snr=${pingResult.snr}dB`);
                }

                // add signal quality if available
                if(pingResult.quality != null){
                    info.push(`quality=${pingResult.quality}%`);
                }

                // add receiving interface
                info.push(`via=${pingResult.receiving_interface}`);

                // update ui
                this.addPingResult(info.join(" "));

            } catch(e) {

                // ignore cancelled error
                if(e instanceof CanceledError){
                    return;
                }

                console.log(e);

                // add ping error to results
                const message = e.response?.data?.message ?? e;
                this.addPingResult(`seq=${this.seq} error=${message}`);

            }
        },
        async dropPath() {

            // simple check to ensure destination hash is valid
            if(this.destinationHash == null || this.destinationHash.length !== 32){
                DialogUtils.alert("Invalid Destination Hash!");
                return;
            }

            try {
                const response = await window.axios.post(`/api/v1/destination/${this.destinationHash}/drop-path`);
                DialogUtils.alert(response.data.message);
            } catch(e) {
                console.log(e);
                const message = e.response?.data?.message ?? `Failed to drop path: ${e}`;
                DialogUtils.alert(message);
            }

        },
        addPingResult(result) {
            this.pingResults.push(result);
            this.scrollPingResultsToBottom();
        },
        scrollPingResultsToBottom: function() {
            // next tick waits for the ui to have the new elements added
            this.$nextTick(() => {
                // set timeout with zero millis seems to fix issue where it doesn't scroll all the way to the bottom...
                setTimeout(() => {
                    const container = document.getElementById("results");
                    if(container){
                        container.scrollTop = container.scrollHeight;
                    }
                }, 0);
            });
        },
    },
}
</script>
