<template>
    <div class="h-screen w-full flex flex-col">

        <!-- header -->
        <div class="flex bg-white p-2 border-gray-300 border-b">
            <div class="flex w-full">
                <div class="hidden sm:flex my-auto border border-gray-300 rounded-md w-10 h-10 mr-3 shadow bg-gray-50">
                    <div class="flex mx-auto my-auto">
                        <img class="w-9 h-9" src="/assets/images/logo.png "/>
                    </div>
                </div>
                <div class="my-auto">
                    <div @click="onAppNameClick" class="font-bold cursor-pointer">Reticulum MeshChat</div>
                    <div class="text-sm">Developed by <a target="_blank" href="https://liamcottle.com" class="text-blue-500">Liam Cottle</a></div>
                </div>
                <div class="flex my-auto ml-auto mr-0 sm:mr-2 space-x-1 sm:space-x-2">
                    <button @click="syncPropagationNode" type="button" class="rounded-full">
                        <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded-full">
                            <span :class="{ 'animate-spin': isSyncingPropagationNode }">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                                </svg>
                            </span>
                            <span class="hidden sm:inline-block my-auto mx-1 text-sm">Sync Messages</span>
                        </span>
                    </button>
                    <button @click="composeNewMessage" type="button" class="rounded-full">
                        <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded-full">
                            <span>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                                </svg>
                            </span>
                            <span class="hidden sm:inline-block my-auto mx-1 text-sm">Compose</span>
                        </span>
                    </button>
                </div>
            </div>
        </div>

        <!-- middle -->
        <div ref="middle" class="flex h-full w-full overflow-auto">

            <!-- sidebar -->
            <div class="bg-white flex w-72 min-w-72 flex-col">
                <div class="flex grow flex-col overflow-y-auto border-r border-gray-200 bg-white">

                    <!-- navigation -->
                    <div class="flex-1">
                        <ul class="py-2 pr-2 space-y-1">

                            <!-- messages -->
                            <li>
                                <SidebarLink :to="{ name: 'messages' }">
                                    <template v-slot:icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                                        </svg>
                                    </template>
                                    <template v-slot:text>
                                        <span>Messages</span>
                                        <span v-if="unreadConversationsCount > 0" class="ml-auto mr-2">{{ unreadConversationsCount }}</span>
                                    </template>
                                </SidebarLink>
                            </li>

                            <!-- nomad network -->
                            <li>
                                <SidebarLink :to="{ name: 'nomadnetwork' }">
                                    <template v-slot:icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
                                        </svg>
                                    </template>
                                    <template v-slot:text>Nomad Network</template>
                                </SidebarLink>
                            </li>

                            <!-- interfaces -->
                            <li>
                                <SidebarLink :to="{ name: 'interfaces' }">
                                    <template v-slot:icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 256 256">
                                            <path d="M232,112H136V88h8a16,16,0,0,0,16-16V40a16,16,0,0,0-16-16H112A16,16,0,0,0,96,40V72a16,16,0,0,0,16,16h8v24H24a8,8,0,0,0,0,16H56v32H48a16,16,0,0,0-16,16v32a16,16,0,0,0,16,16H80a16,16,0,0,0,16-16V176a16,16,0,0,0-16-16H72V128H184v32h-8a16,16,0,0,0-16,16v32a16,16,0,0,0,16,16h32a16,16,0,0,0,16-16V176a16,16,0,0,0-16-16h-8V128h32a8,8,0,0,0,0-16ZM112,40h32V72H112ZM80,208H48V176H80Zm128,0H176V176h32Z"></path>
                                        </svg>
                                    </template>
                                    <template v-slot:text>Interfaces</template>
                                </SidebarLink>
                            </li>

                            <!-- network visualiser -->
                            <li>
                                <SidebarLink :to="{ name: 'network-visualiser' }">
                                    <template v-slot:icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="w-6 h-6">
                                            <path d="M200,152a31.84,31.84,0,0,0-19.53,6.68l-23.11-18A31.65,31.65,0,0,0,160,128c0-.74,0-1.48-.08-2.21l13.23-4.41A32,32,0,1,0,168,104c0,.74,0,1.48.08,2.21l-13.23,4.41A32,32,0,0,0,128,96a32.59,32.59,0,0,0-5.27.44L115.89,81A32,32,0,1,0,96,88a32.59,32.59,0,0,0,5.27-.44l6.84,15.4a31.92,31.92,0,0,0-8.57,39.64L73.83,165.44a32.06,32.06,0,1,0,10.63,12l25.71-22.84a31.91,31.91,0,0,0,37.36-1.24l23.11,18A31.65,31.65,0,0,0,168,184a32,32,0,1,0,32-32Zm0-64a16,16,0,1,1-16,16A16,16,0,0,1,200,88ZM80,56A16,16,0,1,1,96,72,16,16,0,0,1,80,56ZM56,208a16,16,0,1,1,16-16A16,16,0,0,1,56,208Zm56-80a16,16,0,1,1,16,16A16,16,0,0,1,112,128Zm88,72a16,16,0,1,1,16-16A16,16,0,0,1,200,200Z"></path>
                                        </svg>
                                    </template>
                                    <template v-slot:text>Network Visualiser</template>
                                </SidebarLink>
                            </li>

                            <!-- settings -->
                            <li>
                                <SidebarLink :to="{ name: 'settings' }">
                                    <template v-slot:icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                        </svg>
                                    </template>
                                    <template v-slot:text>Settings</template>
                                </SidebarLink>
                            </li>

                            <!-- info -->
                            <li>
                                <SidebarLink :to="{ name: 'about' }">
                                    <template v-slot:icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                                        </svg>
                                    </template>
                                    <template v-slot:text>About</template>
                                </SidebarLink>
                            </li>

                        </ul>
                    </div>

                    <div>

                        <!-- my identity -->
                        <div v-if="config" class="bg-white border-t">
                            <div @click="isShowingMyIdentitySection = !isShowingMyIdentitySection" class="flex text-gray-700 p-2 cursor-pointer">
                                <div class="my-auto mr-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                    </svg>
                                </div>
                                <div class="my-auto">My Identity</div>
                                <div class="ml-auto">
                                    <button @click.stop="saveIdentitySettings" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                        Save
                                    </button>
                                </div>
                            </div>
                            <div v-if="isShowingMyIdentitySection" class="divide-y text-gray-900 border-t border-gray-300">
                                <div class="p-1">
                                    <input v-model="displayName" type="text" placeholder="Display Name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                                </div>
                                <div class="p-1">
                                    <div>Identity Hash</div>
                                    <div class="text-sm text-gray-700">{{ config.identity_hash }}</div>
                                </div>
                                <div class="p-1">
                                    <div>LXMF Address</div>
                                    <div class="text-sm text-gray-700">{{ config.lxmf_address_hash }}</div>
                                </div>
                            </div>
                        </div>

                        <!-- auto announce -->
                        <div v-if="config" class="bg-white border-t">
                            <div @click="isShowingAnnounceSection = !isShowingAnnounceSection" class="flex text-gray-700 p-2 cursor-pointer">
                                <div class="my-auto mr-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M9.348 14.652a3.75 3.75 0 0 1 0-5.304m5.304 0a3.75 3.75 0 0 1 0 5.304m-7.425 2.121a6.75 6.75 0 0 1 0-9.546m9.546 0a6.75 6.75 0 0 1 0 9.546M5.106 18.894c-3.808-3.807-3.808-9.98 0-13.788m13.788 0c3.808 3.807 3.808 9.98 0 13.788M12 12h.008v.008H12V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                                    </svg>
                                </div>
                                <div class="my-auto">Announce</div>
                                <div class="ml-auto">
                                    <button @click.stop="sendAnnounce" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                        Announce Now
                                    </button>
                                </div>
                            </div>
                            <div v-if="isShowingAnnounceSection" class="divide-y text-gray-900 border-t border-gray-300">
                                <div class="p-1">
                                    <select v-model="config.auto_announce_interval_seconds" @change="onAnnounceIntervalSecondsChange" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                                        <option value="0">Disabled</option>
                                        <option value="900">Every 15 Minutes</option>
                                        <option value="1800">Every 30 Minutes</option>
                                        <option value="3600">Every 1 Hour</option>
                                        <option value="10800">Every 3 Hours</option>
                                        <option value="21600">Every 6 Hours</option>
                                        <option value="43200">Every 12 Hours</option>
                                        <option value="86400">Every 24 Hours</option>
                                    </select>
                                    <div class="text-sm text-gray-700">
                                        <span v-if="config.last_announced_at">Last announced: {{ formatSecondsAgo(config.last_announced_at) }}</span>
                                        <span v-else>Last announced: Never</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- audio calls -->
                        <div v-if="config" class="bg-white border-t">
                            <div @click="isShowingCallsSection = !isShowingCallsSection" class="flex text-gray-700 p-2 cursor-pointer">
                                <div class="my-auto mr-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                                    </svg>
                                </div>
                                <div class="my-auto">Calls</div>
                                <div class="ml-auto">
                                    <a @click.stop href="../call.html" target="_blank" class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                                        <span>Open Phone</span>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                            <path fill-rule="evenodd" d="M4.25 5.5a.75.75 0 0 0-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 0 0 .75-.75v-4a.75.75 0 0 1 1.5 0v4A2.25 2.25 0 0 1 12.75 17h-8.5A2.25 2.25 0 0 1 2 14.75v-8.5A2.25 2.25 0 0 1 4.25 4h5a.75.75 0 0 1 0 1.5h-5Z" clip-rule="evenodd" />
                                            <path fill-rule="evenodd" d="M6.194 12.753a.75.75 0 0 0 1.06.053L16.5 4.44v2.81a.75.75 0 0 0 1.5 0v-4.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0 0 1.5h2.553l-9.056 8.194a.75.75 0 0 0-.053 1.06Z" clip-rule="evenodd" />
                                        </svg>
                                    </a>
                                </div>
                            </div>
                            <div v-if="isShowingCallsSection" class="divide-y text-gray-900 border-t border-gray-300">
                                <div class="p-1 flex">
                                    <div>
                                        <div>Status</div>
                                        <div class="text-sm text-gray-700">
                                            <div v-if="activeAudioCalls.length > 0" class="flex space-x-2">
                                                <span v-if="activeInboundAudioCalls.length > 0">{{ activeInboundAudioCalls.length }} Incoming {{ activeInboundAudioCalls.length === 1 ? 'Call' : 'Calls' }}</span>
                                                <span v-else>{{ activeOutboundAudioCalls.length }} Outgoing {{ activeOutboundAudioCalls.length === 1 ? 'Call' : 'Calls' }}</span>
                                            </div>
                                            <div v-else>Hung up, waiting for call...</div>
                                        </div>
                                    </div>
                                    <div v-if="activeAudioCalls.length > 0" class="ml-auto my-auto mr-1 space-x-2">

                                        <!-- view incoming calls -->
                                        <a href="../call.html" target="_blank" title="View Incoming Calls" class="my-auto inline-flex items-center gap-x-1 rounded-full bg-green-500 p-2 text-sm font-semibold text-white shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-500">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
                                                <path fill-rule="evenodd" d="M4.25 5.5a.75.75 0 0 0-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 0 0 .75-.75v-4a.75.75 0 0 1 1.5 0v4A2.25 2.25 0 0 1 12.75 17h-8.5A2.25 2.25 0 0 1 2 14.75v-8.5A2.25 2.25 0 0 1 4.25 4h5a.75.75 0 0 1 0 1.5h-5Z" clip-rule="evenodd" />
                                                <path fill-rule="evenodd" d="M6.194 12.753a.75.75 0 0 0 1.06.053L16.5 4.44v2.81a.75.75 0 0 0 1.5 0v-4.5a.75.75 0 0 0-.75-.75h-4.5a.75.75 0 0 0 0 1.5h2.553l-9.056 8.194a.75.75 0 0 0-.053 1.06Z" clip-rule="evenodd" />
                                            </svg>
                                        </a>

                                        <!-- hangup all calls -->
                                        <button title="Hangup all Calls" @click="hangupAllCalls" type="button" class="my-auto inline-flex items-center gap-x-1 rounded-full bg-red-500 p-2 text-sm font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
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

            <RouterView/>

        </div>

    </div>
</template>

<script>
import SidebarLink from "./SidebarLink.vue";
import DialogUtils from "../js/DialogUtils";
import WebSocketConnection from "../js/WebSocketConnection";
import GlobalState from "../js/GlobalState";
import Utils from "../js/Utils";
import GlobalEmitter from "../js/GlobalEmitter";
import NotificationUtils from "../js/NotificationUtils";

export default {
    name: 'App',
    components: {
        SidebarLink,
    },
    data() {
        return {

            reloadInterval: null,

            isShowingMyIdentitySection: true,
            isShowingAnnounceSection: true,
            isShowingCallsSection: true,

            displayName: "Anonymous Peer",
            config: null,
            appInfo: null,

            audioCalls: [],
            propagationNodeStatus: null,

        };
    },
    beforeUnmount() {

        clearInterval(this.reloadInterval);

        // stop listening for websocket messages
        WebSocketConnection.off("message", this.onWebsocketMessage);

    },
    mounted() {

        // listen for websocket messages
        WebSocketConnection.on("message", this.onWebsocketMessage);

        this.getAppInfo();
        this.updateCallsList();
        this.updatePropagationNodeStatus();

        // update info every few seconds
        this.reloadInterval = setInterval(() => {
            this.updateCallsList();
            this.updatePropagationNodeStatus();
        }, 3000);

    },
    methods: {
        async onWebsocketMessage(message) {
            const json = JSON.parse(message.data);
            switch(json.type){
                case 'config': {
                    this.config = json.config;
                    this.displayName = json.config.display_name;
                    break;
                }
                case 'announced': {
                    // we just announced, update config so we can show the new last updated at
                    this.getConfig();
                    break;
                }
                case 'incoming_audio_call': {
                    NotificationUtils.showIncomingCallNotification();
                    break;
                }
            }
        },
        async getAppInfo() {
            try {
                const response = await window.axios.get(`/api/v1/app/info`);
                this.appInfo = response.data.app_info;
            } catch(e) {
                // do nothing if failed to load app info
                console.log(e);
            }
        },
        async getConfig() {
            try {
                const response = await window.axios.get(`/api/v1/config`);
                this.config = response.data.config;
            } catch(e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        async sendAnnounce() {

            try {
                await window.axios.get(`/api/v1/announce`);
            } catch(e) {
                DialogUtils.alert("failed to announce");
                console.log(e);
            }

            // fetch config so it updates last announced timestamp
            await this.getConfig();

        },
        async updateConfig(config) {
            try {
                WebSocketConnection.send(JSON.stringify({
                    "type": "config.set",
                    "config": config,
                }));
            } catch(e) {
                console.error(e);
            }
        },
        async saveIdentitySettings() {
            await this.updateConfig({
                "display_name": this.displayName,
            });
        },
        async onAnnounceIntervalSecondsChange() {
            await this.updateConfig({
                "auto_announce_interval_seconds": this.config.auto_announce_interval_seconds,
            });
        },
        async composeNewMessage() {

            // go to messages route
            await this.$router.push({ name: "messages" });

            // emit global event handled by MessagesPage
            GlobalEmitter.emit("compose-new-message");

        },
        async syncPropagationNode() {

            // ask to stop syncing if already syncing
            if(this.isSyncingPropagationNode){
                if(confirm("Are you sure you want to stop syncing?")){
                    await this.stopSyncingPropagationNode();
                }
                return;
            }

            // request sync
            try {
                await axios.get("/api/v1/lxmf/propagation-node/sync");
            } catch(e) {
                const errorMessage = e.response?.data?.message ?? "Something went wrong. Try again later.";
                DialogUtils.alert(errorMessage);
                return;
            }

            // update propagation status
            await this.updatePropagationNodeStatus();

            // wait until sync has finished
            const syncFinishedInterval = setInterval(() => {

                // do nothing if still syncing
                if(this.isSyncingPropagationNode){
                    return;
                }

                // finished syncing, stop checking
                clearInterval(syncFinishedInterval);

                // show result
                const status = this.propagationNodeStatus?.state;
                const messagesReceived = this.propagationNodeStatus?.messages_received ?? 0;
                if(status === "complete" || status === "idle"){
                    DialogUtils.alert(`Sync complete. ${messagesReceived} messages received.`);
                } else {
                    DialogUtils.alert(`Sync error: ${status}`);
                }

            }, 500);

        },
        async stopSyncingPropagationNode() {

            // stop sync
            try {
                await axios.get("/api/v1/lxmf/propagation-node/stop-sync");
            } catch(e) {
                // do nothing on error
            }

            // update propagation status
            await this.updatePropagationNodeStatus();

        },
        async updatePropagationNodeStatus() {
            try {
                const response = await axios.get("/api/v1/lxmf/propagation-node/status");
                this.propagationNodeStatus = response.data.propagation_node_status;
            } catch(e) {
                // do nothing on error
            }
        },
        formatSecondsAgo: function(seconds) {
            return Utils.formatSecondsAgo(seconds);
        },
        async updateCallsList() {
            try {

                // fetch calls
                const response = await axios.get("/api/v1/calls");

                // update ui
                this.audioCalls = response.data.audio_calls;

            } catch(e) {
                // do nothing on error
            }
        },
        async hangupAllCalls() {

            // confirm user wants to hang up calls
            if(!confirm("Are you sure you want to hang up all incoming and outgoing calls?")){
                return;
            }

            try {

                // hangup all calls
                await axios.get(`/api/v1/calls/hangup-all`);

                // reload calls list
                await this.updateCallsList();

            } catch(e) {
                // ignore error hanging up call
            }

        },
        onAppNameClick() {
            // user may be on mobile, and is unable to scroll back to sidebar, so let them tap app name to do it
            this.$refs["middle"].scrollTo({
                top: 0,
                left: 0,
                behavior: "smooth",
            });
        },
    },
    computed: {
        unreadConversationsCount() {
            return GlobalState.unreadConversationsCount;
        },
        activeAudioCalls() {
            return this.audioCalls.filter(function(audioCall) {
                return audioCall.is_active;
            });
        },
        activeInboundAudioCalls() {
            return this.activeAudioCalls.filter(function(audioCall) {
                return !audioCall.is_outbound;
            });
        },
        activeOutboundAudioCalls() {
            return this.activeAudioCalls.filter(function(audioCall) {
                return audioCall.is_outbound;
            });
        },
        isSyncingPropagationNode() {
            return [
                "path_requested",
                "link_establishing",
                "link_established",
                "request_sent",
                "receiving",
                "response_received",
            ].includes(this.propagationNodeStatus?.state);
        },
    },
}
</script>
