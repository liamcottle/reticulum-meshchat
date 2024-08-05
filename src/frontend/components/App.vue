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
                    <div class="font-bold">Reticulum MeshChat</div>
                    <div class="text-sm">Developed by <a target="_blank" href="https://liamcottle.com" class="text-blue-500">Liam Cottle</a></div>
                </div>
                <div class="flex my-auto ml-auto mr-0 sm:mr-2 space-x-1 sm:space-x-2">
                    <button @click="startNewLXMFConversation" type="button" class="rounded-full">
                    <span class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded-full">
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                            </svg>
                        </span>
                        <span class="my-auto mx-1 text-sm">Compose</span>
                    </span>
                    </button>
                </div>
            </div>
        </div>

        <!-- middle -->
        <div class="flex h-full w-full overflow-auto">

            <!-- sidebar -->
            <div class="bg-white flex w-72 min-w-72 flex-col">
                <div class="flex grow flex-col overflow-y-auto border-r border-gray-200 bg-white">

                    <!-- navigation -->
                    <div class="flex-1">
                        <ul class="py-2 pr-2 space-y-1">

                            <!-- messages -->
                            <li>
                                <button @click="tab = 'messages'" type="button" :class="[ tab === 'messages' ? 'bg-blue-100 text-blue-800 group:text-blue-800 hover:bg-blue-100' : '']" class="w-full text-gray-800 hover:bg-gray-100 group flex gap-x-3 rounded-r-full p-2 mr-2 text-sm leading-6 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
                                    <span class="my-auto">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                                        </svg>
                                    </span>
                                    <span class="my-auto">Messages</span>
                                    <span v-if="unreadConversationsCount > 0" class="my-auto ml-auto mr-2">{{ unreadConversationsCount }}</span>
                                </button>
                            </li>

                            <!-- nomad network -->
                            <li>
                                <button @click="tab = 'nomadnetwork'" type="button" :class="[ tab === 'nomadnetwork' ? 'bg-blue-100 text-blue-800 group:text-blue-800 hover:bg-blue-100' : '']" class="w-full text-gray-800 hover:bg-gray-100 group flex gap-x-3 rounded-r-full p-2 mr-2 text-sm leading-6 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
                                    <span class="my-auto">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
                                        </svg>
                                    </span>
                                    <span class="my-auto">Nomad Network</span>
                                </button>
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

                            <!-- network -->
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

            <!-- messages sidebar -->
            <MessagesSidebar
                v-if="tab === 'messages'"
                :conversations="conversations"
                :peers="peers"
                :selected-destination-hash="selectedPeer?.destination_hash"
                @conversation-click="onConversationClick"
                @peer-click="onPeerClick"/>

            <!-- nomadnetwork sidebar -->
            <NomadNetworkSidebar
                v-if="tab === 'nomadnetwork'"
                :nodes="nodes"
                :selected-destination-hash="selectedNode?.destination_hash"
                @node-click="onNodeClick"/>

            <!-- main view -->
            <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px]">

                <RouterView/>

                <!-- messages tab -->
                <ConversationViewer
                    v-if="tab === 'messages'"
                    ref="conversation-viewer"
                    :my-lxmf-address-hash="config?.lxmf_address_hash"
                    :selected-peer="selectedPeer"
                    :conversations="conversations"
                    @close="selectedPeer = null"
                    @reload-conversations="getConversations"/>

                <!-- nomadnetwork tab -->
                <template v-if="tab === 'nomadnetwork'">

                    <!-- node -->
                    <div v-if="selectedNode" class="m-2 flex flex-col h-full border rounded-xl bg-white shadow overflow-hidden">

                        <!-- header -->
                        <div class="flex p-2 border-b border-gray-300">

                            <!-- node info -->
                            <div class="my-auto">
                                <span class="font-semibold">{{ selectedNode.name }}</span>
                                <span v-if="selectedNodePath" @click="onDestinationPathClick(selectedNodePath)" class="text-sm cursor-pointer"> - {{ selectedNodePath.hops }} {{ selectedNodePath.hops === 1 ? 'hop' : 'hops' }} away</span>
                            </div>

                            <!-- close button -->
                            <div class="my-auto ml-auto mr-2">
                                <div @click="selectedNode = null" class="cursor-pointer">
                                    <div class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-1 rounded-full">
                                        <div>
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                                <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                                            </svg>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                        <!-- browser navigation -->
                        <div class="flex w-full border-gray-300 border-b p-2">
                            <button @click="loadNodePage(selectedNode.destination_hash, '/page/index.mu')" type="button" class="my-auto text-gray-500 bg-gray-200 hover:bg-gray-300 rounded p-1 cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z" clip-rule="evenodd" />
                                </svg>
                            </button>
                            <button @click="reloadNodePage" type="button" class="ml-1 my-auto text-gray-500 bg-gray-200 hover:bg-gray-300 rounded p-1 cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.433a.75.75 0 0 0 0-1.5H3.989a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39Zm1.23-3.723a.75.75 0 0 0 .219-.53V2.929a.75.75 0 0 0-1.5 0V5.36l-.31-.31A7 7 0 0 0 3.239 8.188a.75.75 0 1 0 1.448.389A5.5 5.5 0 0 1 13.89 6.11l.311.31h-2.432a.75.75 0 0 0 0 1.5h4.243a.75.75 0 0 0 .53-.219Z" clip-rule="evenodd" />
                                </svg>
                            </button>
                            <button @click="loadPreviousNodePage" type="button" :disabled="nodePagePathHistory.length === 0" :class="[ nodePagePathHistory.length > 0 ? 'text-gray-500 bg-gray-200 hover:bg-gray-300' : 'text-gray-400 bg-gray-100']" class="ml-1 my-auto rounded p-1 cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M17 10a.75.75 0 0 1-.75.75H5.612l4.158 3.96a.75.75 0 1 1-1.04 1.08l-5.5-5.25a.75.75 0 0 1 0-1.08l5.5-5.25a.75.75 0 1 1 1.04 1.08L5.612 9.25H16.25A.75.75 0 0 1 17 10Z" clip-rule="evenodd" />
                                </svg>
                            </button>
                            <div class="my-auto mx-2 w-full">
                                <input v-model="nodePagePathUrlInput" @keyup.enter="onNodePageUrlClick(nodePagePathUrlInput)" type="text" placeholder="Enter Destination URL" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2.5 py-1.5">
                            </div>
                            <button @click="onNodePageUrlClick(nodePagePathUrlInput)" type="button" class="my-auto text-gray-500 bg-gray-200 hover:bg-gray-300 rounded p-1 cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clip-rule="evenodd" />
                                </svg>
                            </button>
                        </div>

                        <!-- page content -->
                        <div class="h-full overflow-y-scroll p-3 bg-black text-white">
                            <div class="flex" v-if="isLoadingNodePage">
                                <div class="my-auto">
                                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                </div>
                                <div class="my-auto">Loading {{ nodePageProgress }}%</div>
                            </div>
                            <pre v-else v-html="nodePageContent" class="h-full text-wrap"></pre>
                        </div>

                        <!-- file download bottom bar -->
                        <div v-if="isDownloadingNodeFile" class="flex w-full border-gray-300 border-t p-2">
                            <div class="my-auto mr-2">
                                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            </div>
                            <div class="my-auto">Downloading: {{ nodeFilePath }} ({{ nodeFileProgress }}%)</div>
                        </div>

                    </div>

                    <!-- no node selected -->
                    <div v-else class="flex flex-col mx-auto my-auto text-center leading-5">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Active Node</div>
                        <div>Select a Node to start browsing!</div>
                    </div>

                </template>

            </div>

        </div>

    </div>
</template>

<script>
import SidebarLink from "./SidebarLink.vue";
import MessagesSidebar from "./messages/MessagesSidebar.vue";
import NomadNetworkSidebar from "./nomadnetwork/NomadNetworkSidebar.vue";
import ConversationViewer from "./messages/ConversationViewer.vue";
import DialogUtils from "../js/DialogUtils";

export default {
    name: 'App',
    components: {
        ConversationViewer,
        NomadNetworkSidebar,
        MessagesSidebar,
        SidebarLink,
    },
    data() {
        return {

            isWebsocketConnected: false,
            autoReconnectWebsocket: true,

            isShowingMyIdentitySection: true,
            isShowingAnnounceSection: true,
            isShowingCallsSection: true,

            displayName: "Anonymous Peer",
            config: null,
            appInfo: null,

            audioCalls: [],
            lxmfDeliveryAnnounces: [],

            tab: "messages",

            peers: {},
            selectedPeer: null,

            nodes: {},
            selectedNode: null,
            selectedNodePath: null,

            conversations: [],

            isLoadingNodePage: false,
            nodePageRequestSequence: 0,
            nodePagePath: null,
            nodePagePathUrlInput: null,
            nodePageContent: null,
            nodePageProgress: 0,
            nodePagePathHistory: [],
            nodePageCache: {},

            isDownloadingNodeFile: false,
            nodeFilePath: null,
            nodeFileProgress: 0,

            nomadnetPageDownloadCallbacks: {},
            nomadnetFileDownloadCallbacks: {},

        };
    },
    mounted() {

        this.getAppInfo();
        this.connectWebsocket();
        this.getLxmfDeliveryAnnounces();
        this.getNomadnetworkNodeAnnounces();
        this.getConversations();

        // fixme: this is called by the micron-parser.js
        window.onNodePageUrlClick = (url) => {
            this.onNodePageUrlClick(url);
        };

        // update calls list
        this.updateCallsList();

        // update info every few seconds
        setInterval(() => {
            this.updateCallsList();
            this.getConversations();
        }, 3000);

    },
    methods: {
        connectWebsocket: function() {

            // connect to websocket
            this.ws = new WebSocket(location.origin.replace(/^http/, 'ws') + "/ws");

            this.ws.addEventListener('open', () => {
                this.isWebsocketConnected = true;
            });

            this.ws.addEventListener('close', () => {
                this.isWebsocketConnected = false;
                if(this.autoReconnectWebsocket){
                    setTimeout(() => {
                        this.connectWebsocket();
                    }, 1000);
                }
            });

            // handle data from reticulum
            this.ws.onmessage = (message) => {
                const json = JSON.parse(message.data);
                switch(json.type){
                    case 'config': {
                        this.config = json.config;
                        this.displayName = json.config.display_name;
                        break;
                    }
                    case 'announce': {
                        const aspect = json.announce.aspect;
                        if(aspect === "lxmf.delivery"){
                            this.updatePeerFromAnnounce(json.announce);
                        } else if(aspect === "nomadnetwork.node"){
                            this.updateNodeFromAnnounce(json.announce);
                        }
                        break;
                    }
                    case 'announced': {
                        // we just announced, update config so we can show the new last updated at
                        this.getConfig();
                        break;
                    }
                    case 'incoming_audio_call': {
                        Notification.requestPermission().then((result) => {
                            if(result === "granted"){
                                new window.Notification("Incoming Call", {
                                    body: "Someone is calling you.",
                                    tag: "new_audio_call", // only ever show one notification at a time
                                });
                            }
                        });
                        break;
                    }
                    case 'lxmf.delivery': {

                        // pass lxmf message to conversation viewer
                        const conversationViewer = this.$refs["conversation-viewer"];
                        if(conversationViewer){
                            conversationViewer.onLxmfMessageReceived(json.lxmf_message);
                        }

                        break;

                    }
                    case 'lxmf_message_created': {

                        // pass lxmf message to conversation viewer
                        const conversationViewer = this.$refs["conversation-viewer"];
                        if(conversationViewer){
                            conversationViewer.onLxmfMessageCreated(json.lxmf_message);
                        }

                        break;

                    }
                    case 'lxmf_message_state_updated': {

                        // pass lxmf message to conversation viewer
                        const conversationViewer = this.$refs["conversation-viewer"];
                        if(conversationViewer){
                            conversationViewer.onLxmfMessageUpdated(json.lxmf_message);
                        }

                        break;

                    }
                    case 'lxmf_message_deleted': {

                        // pass lxmf message hash to conversation viewer
                        const conversationViewer = this.$refs["conversation-viewer"];
                        if(conversationViewer){
                            conversationViewer.onLxmfMessageDeleted(json.hash);
                        }

                        break;

                    }
                    case 'nomadnet.page.download': {

                        // get data from server
                        const nomadnetPageDownload = json.nomadnet_page_download;

                        // find download callbacks
                        const getNomadnetPageDownloadCallbackKey = this.getNomadnetPageDownloadCallbackKey(nomadnetPageDownload.destination_hash, nomadnetPageDownload.page_path);
                        const nomadnetPageDownloadCallback = this.nomadnetPageDownloadCallbacks[getNomadnetPageDownloadCallbackKey];
                        if(!nomadnetPageDownloadCallback){
                            console.log("did not find nomadnet page download callback for key: " + getNomadnetPageDownloadCallbackKey);
                            return;
                        }

                        // handle success
                        if(nomadnetPageDownload.status === "success" && nomadnetPageDownloadCallback.onSuccessCallback){
                            nomadnetPageDownloadCallback.onSuccessCallback(nomadnetPageDownload.page_content);
                            delete this.nomadnetPageDownloadCallbacks[getNomadnetPageDownloadCallbackKey];
                            return;
                        }

                        // handle failure
                        if(nomadnetPageDownload.status === "failure" && nomadnetPageDownloadCallback.onFailureCallback){
                            nomadnetPageDownloadCallback.onFailureCallback(nomadnetPageDownload.failure_reason);
                            delete this.nomadnetPageDownloadCallbacks[getNomadnetPageDownloadCallbackKey];
                            return;
                        }

                        // handle progress
                        if(nomadnetPageDownload.status === "progress" && nomadnetPageDownloadCallback.onProgressCallback){
                            nomadnetPageDownloadCallback.onProgressCallback(nomadnetPageDownload.progress);
                            return;
                        }

                        break;

                    }
                    case 'nomadnet.file.download': {

                        // get data from server
                        const nomadnetFileDownload = json.nomadnet_file_download;

                        // find download callbacks
                        const getNomadnetFileDownloadCallbackKey = this.getNomadnetFileDownloadCallbackKey(nomadnetFileDownload.destination_hash, nomadnetFileDownload.file_path);
                        const nomadnetFileDownloadCallback = this.nomadnetFileDownloadCallbacks[getNomadnetFileDownloadCallbackKey];
                        if(!nomadnetFileDownloadCallback){
                            console.log("did not find nomadnet file download callback for key: " + getNomadnetFileDownloadCallbackKey);
                            return;
                        }

                        // handle success
                        if(nomadnetFileDownload.status === "success" && nomadnetFileDownloadCallback.onSuccessCallback){
                            nomadnetFileDownloadCallback.onSuccessCallback(nomadnetFileDownload.file_name, nomadnetFileDownload.file_bytes);
                            delete this.nomadnetFileDownloadCallbacks[getNomadnetFileDownloadCallbackKey];
                            return;
                        }

                        // handle failure
                        if(nomadnetFileDownload.status === "failure" && nomadnetFileDownloadCallback.onFailureCallback){
                            nomadnetFileDownloadCallback.onFailureCallback(nomadnetFileDownload.failure_reason);
                            delete this.nomadnetFileDownloadCallbacks[getNomadnetFileDownloadCallbackKey];
                            return;
                        }

                        // handle progress
                        if(nomadnetFileDownload.status === "progress" && nomadnetFileDownloadCallback.onProgressCallback){
                            nomadnetFileDownloadCallback.onProgressCallback(nomadnetFileDownload.progress);
                            return;
                        }

                        break;

                    }
                }
            };

        },
        disconnectWebsocket: function() {
            if(this.ws){
                this.ws.close();
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

            // do nothing if not connected to websocket
            if(!this.isWebsocketConnected){
                return;
            }

            try {
                this.ws.send(JSON.stringify({
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
        async startNewLXMFConversation() {

            // ask for destination address
            const destinationHash = await this.prompt("Enter LXMF Address");
            if(!destinationHash){
                return;
            }

            this.openLXMFConversation(destinationHash);

        },
        openLXMFConversation(destinationHash) {

            // attempt to find existing peer so we can show their name
            const existingPeer = this.peers[destinationHash];
            if(existingPeer){
                this.onPeerClick(existingPeer);
                return;
            }

            // simple attempt to prevent garbage input
            if(destinationHash.length !== 32){
                DialogUtils.alert("Invalid Address");
                return;
            }

            // we didn't find an existing peer, so just use an unknown name
            this.onPeerClick({
                name: "Unknown Peer",
                destination_hash: destinationHash,
            });

        },
        downloadNomadNetFile(destinationHash, filePath, onSuccessCallback, onFailureCallback, onProgressCallback) {

            // do nothing if not connected to websocket
            if(!this.isWebsocketConnected){
                DialogUtils.alert("Not connected to WebSocket!");
                return;
            }

            try {

                // set callbacks for nomadnet filePath download
                this.nomadnetFileDownloadCallbacks[this.getNomadnetFileDownloadCallbackKey(destinationHash, filePath)] = {
                    onSuccessCallback: onSuccessCallback,
                    onFailureCallback: onFailureCallback,
                    onProgressCallback: onProgressCallback,
                };

                // ask reticulum to download file from nomadnet
                this.ws.send(JSON.stringify({
                    "type": "nomadnet.file.download",
                    "nomadnet_file_download": {
                        "destination_hash": destinationHash,
                        "file_path": filePath,
                    },
                }));

            } catch(e) {
                console.error(e);
            }

        },
        downloadNomadNetPage(destinationHash, pagePath, onSuccessCallback, onFailureCallback, onProgressCallback) {

            // do nothing if not connected to websocket
            if(!this.isWebsocketConnected){
                DialogUtils.alert("Not connected to WebSocket!");
                return;
            }

            try {

                // set callbacks for nomadnet page download
                this.nomadnetPageDownloadCallbacks[this.getNomadnetPageDownloadCallbackKey(destinationHash, pagePath)] = {
                    onSuccessCallback: onSuccessCallback,
                    onFailureCallback: onFailureCallback,
                    onProgressCallback: onProgressCallback,
                };

                // ask reticulum to download page from nomadnet
                this.ws.send(JSON.stringify({
                    "type": "nomadnet.page.download",
                    "nomadnet_page_download": {
                        "destination_hash": destinationHash,
                        "page_path": pagePath,
                    },
                }));

            } catch(e) {
                console.error(e);
            }

        },
        async getLxmfDeliveryAnnounces() {
            try {

                // fetch announces for "lxmf.delivery" aspect
                const response = await window.axios.get(`/api/v1/announces`, {
                    params: {
                        aspect: "lxmf.delivery",
                    },
                });

                // update ui
                const lxmfDeliveryAnnounces = response.data.announces;
                for(const lxmfDeliveryAnnounce of lxmfDeliveryAnnounces){
                    this.updatePeerFromAnnounce(lxmfDeliveryAnnounce);
                }

            } catch(e) {
                // do nothing if failed to load announces
                console.log(e);
            }
        },
        async getNomadnetworkNodeAnnounces() {
            try {

                // fetch announces for "nomadnetwork.node" aspect
                const response = await window.axios.get(`/api/v1/announces`, {
                    params: {
                        aspect: "nomadnetwork.node",
                    },
                });

                // update ui
                const nodeAnnounces = response.data.announces;
                for(const nodeAnnounce of nodeAnnounces){
                    this.updateNodeFromAnnounce(nodeAnnounce);
                }

            } catch(e) {
                // do nothing if failed to load announces
                console.log(e);
            }
        },
        async getConversations() {
            try {
                const response = await window.axios.get(`/api/v1/lxmf/conversations`);
                this.conversations = response.data.conversations;
            } catch(e) {
                // do nothing if failed to load conversations
                console.log(e);
            }
        },
        async getNodePath(destinationHash) {

            // clear previous known path
            this.selectedNodePath = null;

            try {

                // get path to destination
                const response = await window.axios.get(`/api/v1/destination/${destinationHash}/path`);

                // update ui
                this.selectedNodePath = response.data.path;

            } catch(e) {
                console.log(e);
            }

        },
        decodeBase64ToUtf8String: function(base64) {
            // support for decoding base64 as a utf8 string to support emojis and cyrillic characters etc
            return decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
        },
        getPeerNameFromAppData: function(appData) {
            try {
                // app data should be peer name, and our server provides it base64 encoded
                return this.decodeBase64ToUtf8String(appData);
            } catch(e){
                return "Anonymous Peer";
            }
        },
        getNodeNameFromAppData: function(appData) {
            try {
                // app data should be node name, and our server provides it base64 encoded
                return this.decodeBase64ToUtf8String(appData);
            } catch(e){
                return "Anonymous Node";
            }
        },
        updatePeerFromAnnounce: function(announce) {
            this.peers[announce.destination_hash] = {
                ...announce,
                // helper property for easily grabbing peer name from app data
                name: this.getPeerNameFromAppData(announce.app_data),
            };
        },
        updateNodeFromAnnounce: function(announce) {
            this.nodes[announce.destination_hash] = {
                ...announce,
                // helper property for easily grabbing node name from app data
                name: this.getNodeNameFromAppData(announce.app_data),
            };
        },
        async loadNodePage(destinationHash, pagePath, addToHistory = true, loadFromCache = true) {

            // get new sequence for this page load
            const seq = ++this.nodePageRequestSequence;

            // get previous page path
            const previousNodePagePath = this.nodePagePath;

            // update ui
            this.isLoadingNodePage = true;
            this.nodePagePath = `${destinationHash}:${pagePath}`;
            this.nodePageContent = null;
            this.nodePageProgress = 0;

            // update url bar
            this.nodePagePathUrlInput = this.nodePagePath;

            // update node path
            this.getNodePath(destinationHash);

            // add to previous page to history if we are not loading that previous page
            if(addToHistory && previousNodePagePath != null && previousNodePagePath !== this.nodePagePath){
                this.nodePagePathHistory.push(previousNodePagePath);
            }

            // check if we can load this page from the cache
            if(loadFromCache){

                // load from cache
                const nodePagePathCacheKey = `${destinationHash}:${pagePath}`;
                const cachedNodePageContent = this.nodePageCache[nodePagePathCacheKey];

                // if page is cache, we can just return it now
                if(cachedNodePageContent != null){
                    this.nodePageContent = cachedNodePageContent;
                    this.isLoadingNodePage = false;
                    return;
                }

            }

            this.downloadNomadNetPage(destinationHash, pagePath, (pageContent) => {

                // do nothing if callback is for a previous request
                if(seq !== this.nodePageRequestSequence){
                    console.log("ignoring page content callback for previous page request")
                    return;
                }

                // convert micron to html if page ends with .mu extension
                // otherwise, we will just serve the content as is
                if(pagePath.endsWith(".mu")){
                    this.nodePageContent = MicronParser.convertMicronToHtml(pageContent);
                } else {
                    this.nodePageContent = pageContent;
                }

                // update cache
                const nodePagePathCacheKey = `${destinationHash}:${pagePath}`;
                this.nodePageCache[nodePagePathCacheKey] = this.nodePageContent;

                // update page content
                this.isLoadingNodePage = false;

                // update node path
                this.getNodePath(destinationHash);

            }, (failureReason) => {

                // do nothing if callback is for a previous request
                if(seq !== this.nodePageRequestSequence){
                    console.log("ignoring failure callback for previous page request")
                    return;
                }

                // update page content
                this.nodePageContent = `Failed loading page: ${failureReason}`;
                this.isLoadingNodePage = false;

                // update node path
                this.getNodePath(destinationHash);

            }, (progress) => {

                // do nothing if callback is for a previous request
                if(seq !== this.nodePageRequestSequence){
                    console.log("ignoring progress callback for previous page request")
                    return;
                }

                // update page content
                this.nodePageProgress = Math.round(progress * 100);

            });
        },
        async reloadNodePage() {

            // reload current node page without adding to history and without using cache
            this.onNodePageUrlClick(this.nodePagePath, false, false);

        },
        async loadPreviousNodePage() {

            // get the previous path from history, or do nothing
            const previousNodePagePath = this.nodePagePathHistory.pop();
            if(!previousNodePagePath){
                return;
            }

            // load the page
            this.onNodePageUrlClick(previousNodePagePath, false);

        },
        parseNomadnetworkUrl: function(url) {

            // parse relative urls
            if(url.startsWith(":")){
                return {
                    destination_hash: null, // node hash was not in provided url
                    path: url.substring(1), // remove leading ":"
                };
            }

            // parse absolute urls such as 00000000000000000000000000000000:/page/index.mu
            if(url.includes(":")){

                // parse destination hash and url
                const [destinationHash, relativeUrl] = url.split(":");

                // ensure destination is expected length
                if(destinationHash.length === 32){
                    return {
                        destination_hash: destinationHash,
                        path: relativeUrl,
                    };
                }

            }

            // parse node id only
            if(url.length === 32){
                return {
                    destination_hash: url,
                    path: "/page/index.mu",
                };
            }

            // unsupported url
            return null;

        },
        onNodePageUrlClick: function(url, addToHistory = true, useCache = true) {

            // open http urls in new tab
            if(url.startsWith("http://") || url.startsWith("https://")){
                window.open(url, "_blank");
                return;
            }

            // lxmf urls should open the conversation
            if(url.startsWith("lxmf@")){
                const destinationHash = url.replace("lxmf@", "");
                if(destinationHash.length === 32){
                    this.openLXMFConversation(destinationHash);
                    return;
                }
            }

            // attempt to parse url
            const parsedUrl = this.parseNomadnetworkUrl(url);
            if(parsedUrl != null){

                // use parsed destination hash, or fallback to selected node destination hash
                const destinationHash = parsedUrl.destination_hash || this.selectedNode.destination_hash;

                // download file
                if(parsedUrl.path.startsWith("/file/")){

                    // prevent simultaneous downloads
                    if(this.isDownloadingNodeFile){
                        DialogUtils.alert("An existing download is in progress. Please wait for it to finish beforing starting another download.");
                        return;
                    }

                    // update ui
                    this.isDownloadingNodeFile = true;
                    this.nodeFilePath = parsedUrl.path.split("/").pop();
                    this.nodeFileProgress = 0;

                    // start file download
                    this.downloadNomadNetFile(destinationHash, parsedUrl.path, (fileName, fileBytesBase64) => {

                        // no longer downloading
                        this.isDownloadingNodeFile = false;

                        // download file to browser
                        this.downloadFileFromBase64(fileName, fileBytesBase64);

                    }, (failureReason) => {

                        // no longer downloading
                        this.isDownloadingNodeFile = false;

                        // show error message
                        DialogUtils.alert(`Failed to download file: ${failureReason}`);

                    }, (progress) => {
                        this.nodeFileProgress = Math.round(progress * 100);
                    });

                    return;

                }

                // update selected node, so relative urls work correctly when returned by the new node
                this.selectedNode = this.nodes[destinationHash] || {
                    name: "Unknown Node",
                    destination_hash: destinationHash,
                };

                // navigate to node page
                this.loadNodePage(destinationHash, parsedUrl.path, addToHistory, useCache);
                return;

            }

            // unsupported url
            DialogUtils.alert("unsupported url: " + url);

        },
        downloadFileFromBase64: async function(fileName, fileBytesBase64) {

            // create blob from base64 encoded file bytes
            const byteCharacters = atob(fileBytesBase64);
            const byteNumbers = new Array(byteCharacters.length);
            for(let i = 0; i < byteCharacters.length; i++){
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray]);

            // create object url for blob
            const objectUrl = URL.createObjectURL(blob);

            // create link element to download blob
            const link = document.createElement('a');
            link.href = objectUrl;
            link.download = fileName;
            link.style.display = "none";
            document.body.append(link);

            // click link to download file in browser
            link.click();

            // link element is no longer needed
            link.remove();

            // revoke object url to clear memory
            setTimeout(() => URL.revokeObjectURL(objectUrl), 10000);

        },
        onPeerClick: function(peer) {
            this.selectedPeer = peer;
            this.tab = "messages";
        },
        onNodeClick: function(node) {
            this.selectedNode = node;
            this.tab = "nomadnetwork";
            this.loadNodePage(node.destination_hash, "/page/index.mu");
        },
        onConversationClick: function(conversation) {

            // object must stay compatible with format of peers
            this.onPeerClick(conversation);

            // mark conversation as read
            this.$refs["conversation-viewer"].markConversationAsRead(conversation);

        },
        parseSeconds: function(secondsToFormat) {
            secondsToFormat = Number(secondsToFormat);
            var days = Math.floor(secondsToFormat / (3600 * 24));
            var hours = Math.floor((secondsToFormat % (3600 * 24)) / 3600);
            var minutes = Math.floor((secondsToFormat % 3600) / 60);
            var seconds = Math.floor(secondsToFormat % 60);
            return {
                days: days,
                hours: hours,
                minutes: minutes,
                seconds: seconds,
            };
        },
        formatTimeAgo: function(datetimeString) {
            const millisecondsAgo = Date.now() - new Date(datetimeString).getTime();
            const secondsAgo = Math.round(millisecondsAgo / 1000);
            return this.formatSeconds(secondsAgo);
        },
        formatSecondsAgo: function(seconds) {
            const secondsAgo = Math.round((Date.now() / 1000) - seconds);
            return this.formatSeconds(secondsAgo);
        },
        formatSeconds: function(seconds) {

            const parsedSeconds = this.parseSeconds(seconds);

            if(parsedSeconds.days > 0){
                if(parsedSeconds.days === 1){
                    return "1 day ago";
                } else {
                    return parsedSeconds.days + " days ago";
                }
            }

            if(parsedSeconds.hours > 0){
                if(parsedSeconds.hours === 1){
                    return "1 hour ago";
                } else {
                    return parsedSeconds.hours + " hours ago";
                }
            }

            if(parsedSeconds.minutes > 0){
                if(parsedSeconds.minutes === 1){
                    return "a minute ago";
                } else {
                    return parsedSeconds.minutes + " minutes ago";
                }
            }

            if(parsedSeconds.seconds <= 1){
                return "a second ago";
            } else {
                return parsedSeconds.seconds + " seconds ago";
            }

        },
        getNomadnetPageDownloadCallbackKey: function(destinationHash, pagePath) {
            return `${destinationHash}:${pagePath}`;
        },
        getNomadnetFileDownloadCallbackKey: function(destinationHash, filePath) {
            return `${destinationHash}:${filePath}`;
        },
        formatBytes: function(bytes) {

            if(bytes === 0){
                return '0 Bytes';
            }

            const k = 1024;
            const decimals = 0;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

            const i = Math.floor(Math.log(bytes) / Math.log(k));

            return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];

        },
        onDestinationPathClick: function(path) {
            DialogUtils.alert(`${path.hops} ${ path.hops === 1 ? 'hop' : 'hops' } away via ${path.next_hop_interface}`);
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
        async prompt(message) {
            if(window.electron){
                // running inside electron, use ipc prompt
                return await window.electron.prompt(message);
            } else {
                // running inside normal browser, use browser prompt
                return window.prompt(message);
            }
        },
    },
    computed: {
        isElectron() {
            return window.electron != null;
        },
        isMobile() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        },
        unreadConversationsCount() {
            return this.conversations.filter((conversation) => {
                return conversation.is_unread;
            }).length;
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
    },
}
</script>
