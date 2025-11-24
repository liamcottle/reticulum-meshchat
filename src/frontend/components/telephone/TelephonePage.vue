<template>
    <div class="flex w-full h-full bg-gray-100 dark:bg-zinc-950" :class="{'dark': config?.theme === 'dark'}">
        <div class="mx-auto my-auto w-full max-w-xl p-4">

            <div v-if="activeCall" class="flex">
                <div class="mx-auto my-auto">

                    <div class="text-center">
                        <div>

                            <!-- icon -->
                            <div class="flex mb-4">
                                <div class="mx-auto bg-gray-300 dark:bg-zinc-700 text-gray-500 dark:text-gray-400 p-4 rounded-full">
                                    <MaterialDesignIcon icon-name="account" class="size-12"/>
                                </div>
                            </div>

                            <!-- name -->
                            <div class="text-xl font-semibold text-gray-500 dark:text-zinc-100">
                                <span v-if="activeCall.remote_identity_name != null">{{ activeCall.remote_identity_name }}</span>
                                <span v-else>Unknown</span>
                            </div>

                            <!-- identity hash -->
                            <div v-if="activeCall.remote_identity_hash != null" class="text-gray-500 dark:text-zinc-100">
                                {{ Utils.formatDestinationHash(activeCall.remote_identity_hash) }}
                            </div>

                        </div>

                        <!-- call status -->
                        <div class="text-gray-500 dark:text-zinc-100 mb-4">
                            <span v-if="activeCall.is_incoming && activeCall.status === 4">Incoming Call</span>
                            <span v-else>
                                <span v-if="activeCall.status === 0">Busy...</span>
                                <span v-else-if="activeCall.status === 1">Rejected...</span>
                                <span v-else-if="activeCall.status === 2">Calling...</span>
                                <span v-else-if="activeCall.status === 3">Available...</span>
                                <span v-else-if="activeCall.status === 4">Ringing...</span>
                                <span v-else-if="activeCall.status === 5">Connecting...</span>
                                <span v-else-if="activeCall.status === 6">Connected</span>
                                <span v-else>Status: {{ activeCall.status }}</span>
                            </span>
                        </div>

                        <!-- actions -->
                        <div class="mx-auto space-x-2">

                            <!-- answer call -->
                            <button v-if="activeCall.is_incoming && activeCall.status === 4" title="Answer Call" @click="answerCall" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-green-500 p-2 text-sm font-semibold text-white shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-500">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.716 3.223a1.5 1.5 0 0 1-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 0 0 6.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 0 1 1.767-1.052l3.223.716A1.5 1.5 0 0 1 18 15.352V16.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 8.326 13.019 13.019 0 0 1 2 5V3.5Z" clip-rule="evenodd" />
                                </svg>
                                <span class="ml-1">Accept</span>
                            </button>

                            <!-- hangup call -->
                            <button title="Hangup Call" @click="hangupCall" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-red-500 p-2 text-sm font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 rotate-[135deg] translate-y-0.5">
                                    <path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.716 3.223a1.5 1.5 0 0 1-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 0 0 6.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 0 1 1.767-1.052l3.223.716A1.5 1.5 0 0 1 18 15.352V16.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 8.326 13.019 13.019 0 0 1 2 5V3.5Z" clip-rule="evenodd" />
                                </svg>
                                <span class="ml-1">
                                    <span v-if="activeCall.is_incoming && activeCall.status === 4">Decline</span>
                                    <span v-else>Hang Up</span>
                                </span>
                            </button>

                        </div>

                    </div>

                </div>
            </div>

            <div v-else class="w-full space-y-2">

                <!-- dialer -->
                <div class="border rounded-xl bg-white shadow w-full overflow-hidden dark:border-zinc-900">
                    <div class="flex border-b border-gray-300 text-gray-700 p-2 dark:bg-zinc-800 dark:text-white dark:border-zinc-600">
                        <div class="my-auto mr-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 dark:text-white">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                            </svg>
                        </div>
                        <div class="my-auto">Telephone</div>
                    </div>
                    <div class="flex border-b border-gray-300 text-gray-900 p-2 space-x-2 dark:bg-zinc-700 dark:text-zinc-100 dark:border-zinc-600">
                        <div class="my-auto">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 8.25h15m-16.5 7.5h15m-1.8-13.5-3.9 19.5m-2.1-19.5-3.9 19.5" />
                            </svg>
                        </div>
                        <div class="flex-1">
                            <input v-model="destinationHash" type="text" placeholder="Enter Destination Hash" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-zinc-800 dark:border-zinc-700 dark:text-zinc-100">
                        </div>
                        <button @click="initiateCall(destinationHash)" :disabled="isInitiatingCall" type="button" :class="[ isInitiatingCall ? 'bg-gray-400 focus-visible:outline-gray-500' : 'bg-green-500 hover:bg-green-400 focus-visible:outline-green-500' ]" class="my-auto inline-flex items-center gap-x-1 rounded-md p-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
                            <span v-if="isInitiatingCall">
                                <span>Calling...</span>
                            </span>
                            <span v-else>Initiate Call</span>
                        </button>
                    </div>
                    <div class="border-b border-gray-300 text-gray-900 p-2 space-y-2 dark:bg-zinc-700 dark:text-zinc-100 dark:border-zinc-600">
                        <div class="flex space-x-2">
                            <div class="my-auto">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
                                </svg>
                            </div>
                            <div class="w-full">
                                <select v-model="selectedInputDevice" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                    <option v-for="inputDevice in inputDevices" :value="inputDevice">{{ inputDevice }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            <div class="my-auto">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
                                </svg>
                            </div>
                            <div class="w-full">
                                <select v-model="selectedOutputDevice" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                    <option v-for="outputDevice in outputDevices" :value="outputDevice">{{ outputDevice }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            <div class="my-auto">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" />
                                </svg>
                            </div>
                            <div class="w-full">
                                <select v-model="selectedAudioProfileId" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-zinc-900 dark:border-zinc-600 dark:text-white dark:focus:ring-blue-600 dark:focus:border-blue-600">
                                    <option v-for="audioProfile in audioProfiles" :value="audioProfile.id">{{ audioProfile.name }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="flex p-1 dark:bg-zinc-700 dark:border-zinc-600">
                        <div>
                            <div class='dark:text-white'>My Identity Hash</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-100">{{ myIdentityHash || "Unknown" }}</div>
                        </div>
                        <div class="ml-auto my-auto mr-1">
                            <a @click="announce" href="javascript:void(0)" class="rounded-full">
                                <div class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded-full">
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M8.288 15.038a5.25 5.25 0 0 1 7.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 0 1 1.06 0Z" />
                                        </svg>
                                    </div>
                                    <div class="my-auto mx-1 text-sm">Announce</div>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- active call -->
                <div v-if="activeCall" class="border rounded-xl bg-white shadow w-full overflow-hidden  dark:bg-zinc-800 dark:border-zinc-600 dark:text-zinc-100">
                    <div class="flex border-b border-gray-300 text-gray-700 p-2 dark:text-zinc-100">
                        <div class="my-auto mr-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                            </svg>
                        </div>
                        <div class="my-auto">
                            <span v-if="activeCall.is_incoming">Incoming Call</span>
                            <span v-if="activeCall.is_outgoing">Outgoing Call</span>
                        </div>
                    </div>
                    <div class="divide-y">
                        <div class="flex p-2">
                            <div class="mr-2 my-auto">
                                <div class="bg-gray-100 p-2 rounded-full">
                                    <svg v-if="activeCall.is_outgoing" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                        <path d="M3.5 2A1.5 1.5 0 0 0 2 3.5V5c0 1.149.15 2.263.43 3.326a13.022 13.022 0 0 0 9.244 9.244c1.063.28 2.177.43 3.326.43h1.5a1.5 1.5 0 0 0 1.5-1.5v-1.148a1.5 1.5 0 0 0-1.175-1.465l-3.223-.716a1.5 1.5 0 0 0-1.767 1.052l-.267.933c-.117.41-.555.643-.95.48a11.542 11.542 0 0 1-6.254-6.254c-.163-.395.07-.833.48-.95l.933-.267a1.5 1.5 0 0 0 1.052-1.767l-.716-3.223A1.5 1.5 0 0 0 4.648 2H3.5ZM16.5 4.56l-3.22 3.22a.75.75 0 1 1-1.06-1.06l3.22-3.22h-2.69a.75.75 0 0 1 0-1.5h4.5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0V4.56Z" />
                                    </svg>
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                        <path d="M3.5 2A1.5 1.5 0 0 0 2 3.5V5c0 1.149.15 2.263.43 3.326a13.022 13.022 0 0 0 9.244 9.244c1.063.28 2.177.43 3.326.43h1.5a1.5 1.5 0 0 0 1.5-1.5v-1.148a1.5 1.5 0 0 0-1.175-1.465l-3.223-.716a1.5 1.5 0 0 0-1.767 1.052l-.267.933c-.117.41-.555.643-.95.48a11.542 11.542 0 0 1-6.254-6.254c-.163-.395.07-.833.48-.95l.933-.267a1.5 1.5 0 0 0 1.052-1.767l-.716-3.223A1.5 1.5 0 0 0 4.648 2H3.5ZM16.72 2.22a.75.75 0 1 1 1.06 1.06L14.56 6.5h2.69a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75v-4.5a.75.75 0 0 1 1.5 0v2.69l3.22-3.22Z" />
                                    </svg>
                                </div>
                            </div>
                            <div>
                                <div>
                                    <span v-if="activeCall.remote_identity_name != null">{{ activeCall.remote_identity_name }}</span>
                                    <span v-else-if="activeCall.remote_identity_hash != null">{{ Utils.formatDestinationHash(activeCall.remote_identity_hash) }}</span>
                                    <span v-else>Unknown</span>
                                </div>
                                <div class="text-sm text-gray-500 dark:text-zinc-100">
                                    <span>
                                        <span v-if="activeCall.status === 0">Busy...</span>
                                        <span v-else-if="activeCall.status === 1">Rejected...</span>
                                        <span v-else-if="activeCall.status === 2">Calling...</span>
                                        <span v-else-if="activeCall.status === 3">Available...</span>
                                        <span v-else-if="activeCall.status === 4">Ringing...</span>
                                        <span v-else-if="activeCall.status === 5">Connecting...</span>
                                        <span v-else-if="activeCall.status === 6">Connected</span>
                                        <span v-else>Status: {{ activeCall.status }}</span>
                                    </span>
                                </div>
                            </div>
                            <div class="flex space-x-2 ml-auto my-auto mx-2">

                                <!-- answer call -->
                                <button v-if="activeCall.is_incoming && activeCall.status === 4" title="Answer Call" @click="answerCall" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-full bg-green-500 p-2 text-sm font-semibold text-white shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-500">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                        <path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.716 3.223a1.5 1.5 0 0 1-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 0 0 6.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 0 1 1.767-1.052l3.223.716A1.5 1.5 0 0 1 18 15.352V16.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 8.326 13.019 13.019 0 0 1 2 5V3.5Z" clip-rule="evenodd" />
                                    </svg>
                                </button>

                                <!-- hangup call -->
                                <button title="Hangup Call" @click="hangupCall" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-full bg-red-500 p-2 text-sm font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 rotate-[135deg] translate-y-0.5">
                                        <path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.716 3.223a1.5 1.5 0 0 1-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 0 0 6.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 0 1 1.767-1.052l3.223.716A1.5 1.5 0 0 1 18 15.352V16.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 8.326 13.019 13.019 0 0 1 2 5V3.5Z" clip-rule="evenodd" />
                                    </svg>
                                </button>

                            </div>
                        </div>
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
    name: 'TelephonePage',
    components: {MaterialDesignIcon},
    computed: {
        Utils() {
            return Utils;
        }
    },
    data() {
        return {

            config: null,
            myIdentityHash: null,
            activeCall: null,

            destinationHash: null,
            isInitiatingCall: false,

            selectedInputDevice: null,
            selectedOutputDevice: null,
            inputDevices: [],
            outputDevices: [],

            selectedAudioProfileId: null,
            audioProfiles: [],

        };
    },
    mounted: function() {

        // update config
        this.getConfig();
        this.getAudioDevices();
        this.getAudioProfiles();
        this.getTelephoneStatus();

        // update telephone status every second
        setInterval(() => {
            this.getTelephoneStatus();
        }, 1000);

        // parse url params
        var queryParams = new URLSearchParams(location.search);
        var queryDestinationHash = queryParams.get("destination_hash");

        // autofill destination hash to call when query param provided in url
        if(queryDestinationHash){
            this.destinationHash = queryDestinationHash;
        }

    },
    methods: {
        async initiateCall(destinationHash) {

            // do nothing if already initiating call
            if(this.isInitiatingCall){
                alert("Call is already initiating...");
                return;
            }

            // make sure call hash provided
            if(!destinationHash) {
                alert("Enter destination hash to call.");
                return;
            }

            // make sure input device provided
            if(!this.selectedInputDevice) {
                alert("Please select input microphone.");
                return;
            }

            // make sure output device provided
            if(!this.selectedOutputDevice) {
                alert("Please select output speakers.");
                return;
            }

            // make sure audio profile provided
            if(!this.selectedAudioProfileId) {
                alert("Please select audio quality.");
                return;
            }

            // show loading
            this.isInitiatingCall = true;

            try {

                // initiate call
                await axios.get(`/api/v1/telephone/call/${destinationHash}`, {
                    params: {
                        timeout: 15, // how long to attempt to initiate call
                        input_device_name: this.selectedInputDevice,
                        output_device_name: this.selectedOutputDevice,
                        audio_profile_id: this.selectedAudioProfileId,
                    },
                });

                // fetch status
                await this.getTelephoneStatus();

            } catch(e) {

                console.log(e);

                // show error message from response, or fallback to default
                const message = e.response?.data?.message ?? "failed to initiate call";
                alert(message);

            } finally {
                // hide loading
                this.isInitiatingCall = false;
            }

        },
        async answerCall() {
            try {

                // answer call
                await axios.get(`/api/v1/telephone/answer`);

                // update ui
                await this.getTelephoneStatus();

            } catch(e) {
                // ignore error answering call
            }
        },
        async hangupCall() {

            try {

                // hangup call
                await axios.get(`/api/v1/telephone/hangup`);

                // update ui
                await this.getTelephoneStatus();

            } catch(e) {
                // ignore error hanging up call
            }

        },
        async getConfig() {
            try {

                // fetch calls
                const response = await axios.get("/api/v1/config");

                // update ui
                this.config = response.data.config;
                this.myIdentityHash = response.data.config.identity_hash;

            } catch(e) {
                // do nothing on error
                console.error(e);
            }
        },
        async getAudioDevices() {
            try {

                // fetch audio devices
                const response = await axios.get("/api/v1/telephone/audio-devices");

                // update ui
                this.selectedInputDevice = response.data.default_input_device;
                this.selectedOutputDevice = response.data.default_output_device;
                this.inputDevices = response.data.input_devices;
                this.outputDevices = response.data.output_devices;

            } catch(e) {
                // do nothing on error
                console.error(e);
            }
        },
        async getAudioProfiles() {
            try {

                // fetch audio profiles
                const response = await axios.get("/api/v1/telephone/audio-profiles");

                // update ui
                this.selectedAudioProfileId = response.data.default_audio_profile_id;
                this.audioProfiles = response.data.audio_profiles;

            } catch(e) {
                // do nothing on error
                console.error(e);
            }
        },
        async getTelephoneStatus() {
            try {

                // fetch calls
                const response = await axios.get("/api/v1/telephone/status");

                // update ui
                this.activeCall = response.data.active_call;

            } catch(e) {
                // do nothing on error
                console.error(e);
            }
        },
        async announce() {
            try {
                await window.axios.get(`/api/v1/announce`);
            } catch(e) {
                alert("failed to announce");
                console.log(e);
            }
        },
    },
}
</script>
