<template>

    <!-- peer selected -->
    <div v-if="selectedPeer" class="m-2 flex flex-col h-full border rounded-xl bg-white shadow overflow-hidden">

        <!-- header -->
        <div class="flex p-2 border-b border-gray-300">

            <!-- peer info -->
            <div>
                <div @click="updateCustomDisplayName" class="flex cursor-pointer">
                    <div v-if="selectedPeer.custom_display_name != null" class="my-auto mr-1" title="Custom Display Name">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6Z" />
                        </svg>
                    </div>
                    <div class="my-auto font-semibold" :title="selectedPeer.display_name">{{ selectedPeer.custom_display_name ?? selectedPeer.display_name }}</div>
                </div>
                <div class="text-sm"><{{ selectedPeer.destination_hash }}> <span v-if="selectedPeerPath" @click="onDestinationPathClick(selectedPeerPath)" class="cursor-pointer">{{ selectedPeerPath.hops }} {{ selectedPeerPath.hops === 1 ? 'hop' : 'hops' }} away</span></div>
            </div>

            <!-- call button -->
            <div class="ml-auto my-auto mr-2">
                <a :href="`call.html?destination_hash=${selectedPeer.destination_hash}`" target="_blank" class="cursor-pointer">
                    <div class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                            </svg>
                        </div>
                    </div>
                </a>
            </div>

            <!-- delete button -->
            <div class="my-auto mr-2">
                <div @click="deleteConversation" class="cursor-pointer">
                    <div class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- close button -->
            <div class="my-auto mr-2">
                <div @click="close" class="cursor-pointer">
                    <div class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-2 rounded-full">
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                                <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <!-- chat items -->
        <div @scroll="onMessagesScroll" id="messages" class="h-full overflow-y-scroll">

            <div v-if="selectedPeerChatItems.length > 0" class="flex flex-col flex-col-reverse p-3">

                <div v-for="chatItem of selectedPeerChatItemsReversed" class="flex flex-col max-w-xl mt-3" :class="{ 'ml-auto pl-4 md:pl-16 items-end': chatItem.is_outbound, 'mr-auto pr-4 md:pr-16 items-start': !chatItem.is_outbound }">

                    <!-- message content -->
                    <div @click="onChatItemClick(chatItem)" class="border border-gray-300 rounded-xl shadow overflow-hidden" :class="[ chatItem.lxmf_message.state === 'failed' ? 'bg-red-500 text-white' : chatItem.is_outbound ? 'bg-[#3b82f6] text-white' : 'bg-[#efefef]' ]">

                        <div class="w-full space-y-0.5 px-2.5 py-1">

                            <!-- content -->
                            <div v-if="chatItem.lxmf_message.content" style="white-space:pre-wrap;word-break:break-word;font-family:inherit;">{{ chatItem.lxmf_message.content }}</div>

                            <!-- image field -->
                            <div v-if="chatItem.lxmf_message.fields?.image">
                                <img @click.stop="openImage(`data:image/${chatItem.lxmf_message.fields.image.image_type};base64,${chatItem.lxmf_message.fields.image.image_bytes}`)" :src="`data:image/${chatItem.lxmf_message.fields.image.image_type};base64,${chatItem.lxmf_message.fields.image.image_bytes}`" class="w-full rounded-md cursor-pointer"/>
                            </div>

                            <!-- audio field -->
                            <div v-if="chatItem.lxmf_message.fields?.audio" class="pb-1">

                                <!-- audio is loaded -->
                                <audio v-if="lxmfMessageAudioAttachmentCache[chatItem.lxmf_message.hash]" controls class="shadow rounded-full" style="height:54px;">
                                    <source :src="lxmfMessageAudioAttachmentCache[chatItem.lxmf_message.hash]" type="audio/wav"/>
                                </audio>

                                <!-- audio is not yet loaded -->
                                <!-- min height to make sure audio player doesn't cause height increase after loading -->
                                <div v-else style="min-height:54px;" class="flex">
                                    <button @click="downloadFileFromBase64('audio.bin', chatItem.lxmf_message.fields.audio.audio_bytes)" type="button" class="my-auto flex border border-gray-300 hover:bg-gray-100 rounded px-2 py-1 text-sm text-gray-700 font-semibold cursor-pointer space-x-2 bg-[#efefef]">
                                        <span class="my-auto">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                              <path stroke-linecap="round" stroke-linejoin="round" d="m9 9 10.5-3m0 6.553v3.75a2.25 2.25 0 0 1-1.632 2.163l-1.32.377a1.803 1.803 0 1 1-.99-3.467l2.31-.66a2.25 2.25 0 0 0 1.632-2.163Zm0 0V2.25L9 5.25v10.303m0 0v3.75a2.25 2.25 0 0 1-1.632 2.163l-1.32.377a1.803 1.803 0 0 1-.99-3.467l2.31-.66A2.25 2.25 0 0 0 9 15.553Z" />
                                            </svg>
                                        </span>
                                        <span class="my-auto w-full">
                                            Unsupported Audio (mode {{ chatItem.lxmf_message.fields.audio.audio_mode }})
                                        </span>
                                        <span class="my-auto">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                                            </svg>
                                        </span>
                                    </button>
                                </div>

                            </div>

                            <!-- file attachment fields -->
                            <div v-if="chatItem.lxmf_message.fields?.file_attachments" class="space-y-1">
                                <a @click.stop target="_blank" :download="file_attachment.file_name" :href="`data:application/octet-stream;base64,${file_attachment.file_bytes}`" v-for="file_attachment of chatItem.lxmf_message.fields?.file_attachments ?? []" class="flex border border-gray-300 hover:bg-gray-100 rounded px-2 py-1 text-sm text-gray-700 font-semibold cursor-pointer space-x-2 bg-[#efefef]">
                                    <div class="my-auto">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13"></path>
                                        </svg>
                                    </div>
                                    <div class="my-auto w-full">{{ file_attachment.file_name }}</div>
                                    <div class="my-auto">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                                        </svg>
                                    </div>
                                </a>
                            </div>

                        </div>

                        <!-- actions -->
                        <div v-if="chatItem.is_actions_expanded" class="border-t p-1 bg-[#efefef] text-white">

                            <!-- delete message -->
                            <button @click.stop="deleteChatItem(chatItem)" type="button" class="inline-flex items-center gap-x-1 rounded-md bg-red-500 px-2 py-1 text-xs font-semibold text-white shadow-sm hover:bg-red-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">
                                Delete
                            </button>

                        </div>

                    </div>

                    <!-- message state -->
                    <div v-if="chatItem.is_outbound" class="flex text-right" :class="[ chatItem.lxmf_message.state === 'failed' ? 'text-red-500' : 'text-gray-500' ]">
                        <div class="flex ml-auto space-x-1">

                            <!-- state label -->
                            <div class="my-auto">
                                <span @click="showSentMessageInfo(chatItem.lxmf_message)" class="space-x-1 cursor-pointer">
                                    <span>{{ chatItem.lxmf_message.state }}</span>
                                    <span v-if="chatItem.lxmf_message.state === 'outbound' && chatItem.lxmf_message.delivery_attempts >= 1">(attempt {{ chatItem.lxmf_message.delivery_attempts + 1 }})</span>
                                    <span v-if="chatItem.lxmf_message.state === 'sent' && chatItem.lxmf_message.method === 'opportunistic' && chatItem.lxmf_message.delivery_attempts >= 1">(attempt {{ chatItem.lxmf_message.delivery_attempts }})</span>
                                    <span v-if="chatItem.lxmf_message.state === 'sent' && chatItem.lxmf_message.method === 'propagated'">to propagation node</span>
                                    <span v-if="chatItem.lxmf_message.state === 'sending'">{{ chatItem.lxmf_message.progress.toFixed(0) }}%</span>
                                </span>
                                <a v-if="chatItem.lxmf_message.state === 'failed'" @click="retrySendingMessage(chatItem)" class="ml-1 cursor-pointer underline text-blue-500">retry?</a>
                            </div>

                            <!-- delivered icon -->
                            <div v-if="chatItem.lxmf_message.state === 'delivered'" class="my-auto">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd" />
                                </svg>
                            </div>

                            <!-- failed icon -->
                            <div v-else-if="chatItem.lxmf_message.state === 'failed'" class="my-auto">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                                    <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
                                </svg>
                            </div>

                            <!-- fallback icon -->
                            <div v-else class="my-auto">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                            </div>

                        </div>
                    </div>

                    <!-- inbound message info -->
                    <div v-if="!chatItem.is_outbound" class="text-xs text-gray-500 mt-0.5 flex flex-col">

                        <!-- received timestamp -->
                        <span @click="showReceivedMessageInfo(chatItem.lxmf_message)" class="cursor-pointer">{{ formatTimeAgo(chatItem.lxmf_message.created_at) }}</span>

                    </div>

                </div>

                <!-- load previous -->
                <button v-show="!isLoadingPrevious && hasMorePrevious" id="load-previous" @click="loadPrevious" type="button" class="flex space-x-2 mx-auto bg-gray-200 px-3 py-1 hover:bg-gray-300 rounded-full shadow">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m15 11.25-3-3m0 0-3 3m3-3v7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    <span>Load Previous</span>
                </button>

            </div>

        </div>

        <!-- send message -->
        <div class="w-full border-gray-300 border-t p-2">
            <div class="mx-auto">

                <!-- message composer -->
                <div>

                    <!-- image attachment -->
                    <div v-if="newMessageImage" class="mb-2">
                        <div class="w-32 h-32 rounded shadow border relative overflow-hidden">

                            <!-- image preview -->
                            <img v-if="newMessageImageUrl" :src="newMessageImageUrl" class="w-full h-full"/>

                            <!-- remove button (top right) -->
                            <div class="absolute top-0 right-0 p-1">
                                <div @click="removeImageAttachment" class="cursor-pointer">
                                    <div class="flex text-gray-700 bg-gray-100 hover:bg-gray-200 p-1 rounded-full">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
                                            <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                                        </svg>
                                    </div>
                                </div>
                            </div>

                            <!-- image size (bottom left) -->
                            <div class="absolute bottom-0 left-0 p-1">
                                <div class="bg-gray-100 rounded border text-sm px-1">{{ formatBytes(newMessageImage.size) }}</div>
                            </div>

                        </div>
                    </div>

                    <!-- audio attachment -->
                    <div v-if="newMessageAudio" class="mb-2">
                        <div class="flex flex-wrap gap-1">
                            <div class="flex border border-gray-300 rounded text-gray-700 divide-x divide-gray-300 overflow-hidden">

                                <div class="flex p-1">

                                    <!-- audio preview -->
                                    <div>
                                        <audio controls class="h-10">
                                            <source :src="newMessageAudio.audio_wav_url" type="audio/wav"/>
                                        </audio>
                                    </div>

                                    <!-- encoded file size -->
                                    <div class="my-auto px-1 text-sm text-gray-500">
                                        {{ formatBytes(newMessageAudio.audio_blob.size) }}
                                    </div>

                                </div>

                                <!-- remove audio attachment -->
                                <div @click="removeAudioAttachment" class="flex my-auto text-sm text-gray-500 h-full px-1 hover:bg-gray-200 cursor-pointer">
                                    <svg class="w-5 h-5 my-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                    </svg>
                                </div>

                            </div>
                        </div>
                    </div>

                    <!-- file attachments -->
                    <div v-if="newMessageFiles.length > 0" class="mb-2">
                        <div class="flex flex-wrap gap-1">
                            <div v-for="file in newMessageFiles" class="flex border border-gray-300 rounded text-gray-700 divide-x divide-gray-300 overflow-hidden">
                                <div class="my-auto px-1">
                                    <span class="mr-1">{{ file.name }}</span>
                                    <span class="my-auto text-sm text-gray-500">{{ formatBytes(file.size) }}</span>
                                </div>
                                <div @click="removeFileAttachment(file)" class="flex my-auto text-sm text-gray-500 h-full px-1 hover:bg-gray-200 cursor-pointer">
                                    <svg class="w-5 h-5 my-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- text input -->
                    <textarea
                        id="message-input"
                        :readonly="isSendingMessage"
                        v-model="newMessageText"
                        @keydown.enter.exact.native.prevent="onEnterPressed"
                        @keydown.enter.shift.exact.native.prevent="onShiftEnterPressed"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        rows="3"
                        placeholder="Send a message..."></textarea>

                    <!-- action button -->
                    <div class="flex mt-2">

                        <!-- add files -->
                        <button @click="addFilesToMessage" type="button" class="my-auto mr-1 inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                                <path fill-rule="evenodd" d="M5.625 1.5H9a3.75 3.75 0 0 1 3.75 3.75v1.875c0 1.036.84 1.875 1.875 1.875H16.5a3.75 3.75 0 0 1 3.75 3.75v7.875c0 1.035-.84 1.875-1.875 1.875H5.625a1.875 1.875 0 0 1-1.875-1.875V3.375c0-1.036.84-1.875 1.875-1.875ZM12.75 12a.75.75 0 0 0-1.5 0v2.25H9a.75.75 0 0 0 0 1.5h2.25V18a.75.75 0 0 0 1.5 0v-2.25H15a.75.75 0 0 0 0-1.5h-2.25V12Z" clip-rule="evenodd" />
                                <path d="M14.25 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 16.5 7.5h-1.875a.375.375 0 0 1-.375-.375V5.25Z" />
                            </svg>
                            <span class="ml-1 hidden sm:inline-block">Add Files</span>
                        </button>

                        <!-- add image -->
                        <button @click="addImageToMessage" type="button" class="my-auto mr-1 inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                                <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 0 1 2.25-2.25h16.5A2.25 2.25 0 0 1 22.5 6v12a2.25 2.25 0 0 1-2.25 2.25H3.75A2.25 2.25 0 0 1 1.5 18V6ZM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0 0 21 18v-1.94l-2.69-2.689a1.5 1.5 0 0 0-2.12 0l-.88.879.97.97a.75.75 0 1 1-1.06 1.06l-5.16-5.159a1.5 1.5 0 0 0-2.12 0L3 16.061Zm10.125-7.81a1.125 1.125 0 1 1 2.25 0 1.125 1.125 0 0 1-2.25 0Z" clip-rule="evenodd" />
                            </svg>
                            <span class="ml-1 hidden sm:inline-block">Add Image</span>
                        </button>

                        <!-- add audio -->
                        <div>
                            <AddAudioButton
                                :is-recording-audio-attachment="isRecordingAudioAttachment"
                                @start-recording="startRecordingAudioAttachment($event)"
                                @stop-recording="stopRecordingAudioAttachment">
                                <span>Recording: {{ audioAttachmentRecordingDuration }}</span>
                            </AddAudioButton>
                        </div>

                        <!-- send message -->
                        <button @click="sendMessage" :disabled="!canSendMessage" type="button" class="ml-auto my-auto inline-flex items-center gap-x-1 rounded-md px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2" :class="[ canSendMessage ? 'bg-blue-500 hover:bg-blue-400 focus-visible:outline-blue-500' : 'bg-gray-400 focus-visible:outline-gray-500 cursor-not-allowed']">
                            <span v-if="isSendingMessage">Sending...</span>
                            <span v-else>Send</span>
                        </button>

                    </div>

                </div>

            </div>
        </div>

        <!-- hidden file input for selecting files -->
        <input ref="image-input" @change="onImageInputChange" type="file" accept="image/*" style="display:none"/>
        <input ref="file-input" @change="onFileInputChange" type="file" multiple style="display:none"/>

    </div>

    <!-- no peer selected -->
    <div v-else class="flex flex-col mx-auto my-auto text-center leading-5">
        <div class="mx-auto mb-1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
            </svg>
        </div>
        <div class="font-semibold">No Active Chat</div>
        <div>Select a Peer to start chatting!</div>
    </div>

</template>

<script>
import Utils from "../../js/Utils";
import DialogUtils from "../../js/DialogUtils";
import NotificationUtils from "../../js/NotificationUtils";
import WebSocketConnection from "../../js/WebSocketConnection";
import AddAudioButton from "./AddAudioButton.vue";

export default {
    name: 'ConversationViewer',
    components: {
        AddAudioButton,
    },
    props: {
        myLxmfAddressHash: String,
        selectedPeer: Object,
        conversations: Array,
    },
    data() {
        return {

            selectedPeerPath: null,

            lxmfMessagesRequestSequence: 0,
            chatItems: [],

            isLoadingPrevious: false,
            hasMorePrevious: true,

            newMessageText: "",
            newMessageImage: null,
            newMessageImageUrl: null,
            newMessageAudio: null,
            newMessageFiles: [],
            isSendingMessage: false,
            autoScrollOnNewMessage: true,

            isRecordingAudioAttachment: false,
            audioAttachmentMicrophoneRecorder: null,
            audioAttachmentRecordingStartedAt: null,
            audioAttachmentRecordingDuration: null,
            audioAttachmentRecordingTimer: null,
            lxmfMessageAudioAttachmentCache: {},
            lxmfAudioModeToCodec2ModeMap: {
                // https://github.com/markqvist/LXMF/blob/master/LXMF/LXMF.py#L21
                0x01: "450PWB", // AM_CODEC2_450PWB
                0x02: "450", // AM_CODEC2_450
                0x03: "700C", // AM_CODEC2_700C
                0x04: "1200", // AM_CODEC2_1200
                0x05: "1300", // AM_CODEC2_1300
                0x06: "1400", // AM_CODEC2_1400
                0x07: "1600", // AM_CODEC2_1600
                0x08: "2400", // AM_CODEC2_2400
                0x09: "3200", // AM_CODEC2_3200
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

    },
    methods: {
        close() {
            this.$emit("close");
        },
        onMessagesScroll(event) {

            // check if messages is scrolled to bottom
            const element = event.target;
            const isAtBottom = element.scrollTop === (element.scrollHeight - element.offsetHeight);

            // we want to auto scroll if user is at bottom of messages list
            this.autoScrollOnNewMessage = isAtBottom;

            // load previous when scrolling near top of page
            if(element.scrollTop <= 500){
                this.loadPrevious();
            }

        },
        async initialLoad() {

            // reset
            this.chatItems = [];
            this.hasMorePrevious = true;
            if(!this.selectedPeer){
                return;
            }

            this.getPeerPath();

            // load 1 page of previous messages
            await this.loadPrevious();

            // scroll to bottom
            this.scrollMessagesToBottom();

        },
        async loadPrevious() {

            // do nothing if already loading
            if(this.isLoadingPrevious){
                return;
            }

            this.isLoadingPrevious = true;

            try {

                const seq = ++this.lxmfMessagesRequestSequence;

                // fetch lxmf messages from "us to destination" and from "destination to us"
                const pageSize = 30;
                const response = await window.axios.get(`/api/v1/lxmf-messages/conversation/${this.selectedPeer.destination_hash}`, {
                    params: {
                        count: pageSize,
                        order: "desc",
                        after_id: this.oldestMessageId,
                    },
                });

                // do nothing if response is for a previous request
                if(seq !== this.lxmfMessagesRequestSequence){
                    console.log("ignoring response for previous lxmf messages request")
                    return;
                }

                // convert lxmf messages to chat items
                const chatItems = [];
                const lxmfMessages = response.data.lxmf_messages;
                for(const lxmfMessage of lxmfMessages){
                    chatItems.push({
                        "type": "lxmf_message",
                        "is_outbound": this.myLxmfAddressHash === lxmfMessage.source_hash,
                        "lxmf_message": lxmfMessage,
                    });
                }

                // add messages to start of existing messages
                for(const chatItem of chatItems){
                    this.chatItems.unshift(chatItem);
                }

                // no more previous to load if received items is less than expected page size
                if(chatItems.length < pageSize){
                    this.hasMorePrevious = false;
                }

            } catch(e) {
                // do nothing
            } finally {
                this.isLoadingPrevious = false;
            }

        },
        async onWebsocketMessage(message) {
            const json = JSON.parse(message.data);
            switch(json.type){
                case 'lxmf.delivery': {
                    this.onLxmfMessageReceived(json.lxmf_message);
                    await this.getPeerPath();
                    break;
                }
                case 'lxmf_message_created': {
                    this.onLxmfMessageCreated(json.lxmf_message);
                    await this.getPeerPath();
                    break;
                }
                case 'lxmf_message_state_updated': {
                    this.onLxmfMessageUpdated(json.lxmf_message);
                    break;
                }
                case 'lxmf_message_deleted': {
                    this.onLxmfMessageDeleted(json.hash);
                    break;
                }
            }
        },
        onLxmfMessageReceived(lxmfMessage) {

            // add inbound message to ui
            this.chatItems.push({
                "type": "lxmf_message",
                "lxmf_message": lxmfMessage,
            });

            // if inbound message is for a conversation we are currently looking at, mark it as read
            if(lxmfMessage.source_hash === this.selectedPeer?.destination_hash){

                // find conversation
                const conversation = this.findConversation(this.selectedPeer.destination_hash);
                if(conversation){
                    this.markConversationAsRead(conversation);
                }

            }

            // show notification for new messages if window is not focussed
            if(!document.hasFocus()){
                NotificationUtils.showNewMessageNotification();
            }

            // auto scroll to bottom if we want to
            if(this.autoScrollOnNewMessage){
                this.scrollMessagesToBottom();
            }

        },
        onLxmfMessageCreated(lxmfMessage) {

            // add new outbound lxmf message from server
            // todo check if received message is for this conversation
            if(!this.isLxmfMessageInUi(lxmfMessage.hash)){
                this.chatItems.push({
                    "type": "lxmf_message",
                    "lxmf_message": lxmfMessage,
                    "is_outbound": true,
                });
            }

        },
        onLxmfMessageUpdated(lxmfMessage) {

            // find existing chat item by lxmf message hash
            const lxmfMessageHash = lxmfMessage.hash;
            const chatItemIndex = this.chatItems.findIndex((chatItem) => chatItem.lxmf_message?.hash === lxmfMessageHash);
            if(chatItemIndex === -1){
                console.log("did not find existing chat item index for lxmf message hash: " + lxmfMessage.hash);
                return;
            }

            // update lxmf message from server, while ensuring ui updates from nested object change
            this.chatItems[chatItemIndex].lxmf_message = lxmfMessage;

        },
        onLxmfMessageDeleted(hash) {
            if(hash){
                // remove existing chat item by lxmf message hash
                this.chatItems = this.chatItems.filter((item) => {
                    return item.lxmf_message?.hash !== hash;
                });
            }
        },
        async getPeerPath() {

            // clear previous known path
            this.selectedPeerPath = null;

            if(this.selectedPeer){
                try {

                    // get path to destination
                    const response = await window.axios.get(`/api/v1/destination/${this.selectedPeer.destination_hash}/path`);

                    // update ui
                    this.selectedPeerPath = response.data.path;

                } catch(e) {
                    console.log(e);
                }
            }

        },
        onDestinationPathClick(path) {
            DialogUtils.alert(`${path.hops} ${ path.hops === 1 ? 'hop' : 'hops' } away via ${path.next_hop_interface}`);
        },
        scrollMessagesToBottom: function() {
            // next tick waits for the ui to have the new elements added
            this.$nextTick(() => {
                // set timeout with zero millis seems to fix issue where it doesn't scroll all the way to the bottom...
                setTimeout(() => {
                    const container = document.getElementById("messages");
                    if(container){
                        container.scrollTop = container.scrollHeight;
                    }
                }, 0);
            });
        },
        isLxmfMessageInUi: function(hash) {
            return this.chatItems.findIndex((chatItem) => chatItem.lxmf_message?.hash === hash) !== -1;
        },
        async getCustomDisplayName() {
            if(this.selectedPeer){
                try {

                    // get custom display name
                    const response = await window.axios.get(`/api/v1/destination/${this.selectedPeer.destination_hash}/custom-display-name`);

                    // update ui
                    this.selectedPeer.custom_display_name = response.data.custom_display_name;

                } catch(e) {
                    console.log(e);
                }
            }
        },
        async updateCustomDisplayName() {

            // do nothing if no peer selected
            if(!this.selectedPeer){
                return;
            }

            // ask user for new display name
            const displayName = await DialogUtils.prompt("Enter a custom display name");
            if(displayName == null){
                return;
            }

            try {

                // update display name on server
                await axios.post(`/api/v1/destination/${this.selectedPeer.destination_hash}/custom-display-name/update`, {
                    display_name: displayName,
                });

                // update display name in ui
                await this.getCustomDisplayName();

                // reload conversations (so conversations list updates name)
                this.$emit("reload-conversations");

            } catch(e) {
                console.log(e);
                DialogUtils.alert("Failed to update display name");
            }

        },
        async deleteConversation() {

            // do nothing if no peer selected
            if(!this.selectedPeer){
                return;
            }

            // ask user to confirm deleting conversation history
            if(!confirm("Are you sure you want to delete all messages from this conversation? This can not be undone!")){
                return;
            }

            // delete all lxmf messages from "us to destination" and from "destination to us"
            try {
                await window.axios.delete(`/api/v1/lxmf-messages/conversation/${this.selectedPeer.destination_hash}`);
            } catch(e) {
                DialogUtils.alert("failed to delete conversation");
                console.log(e);
            }

            // reload conversation
            await this.initialLoad();

            // reload conversations
            this.$emit("reload-conversations");

        },
        onChatItemClick: function(chatItem) {
            if(!chatItem.is_actions_expanded){
                chatItem.is_actions_expanded = true;
            } else {
                chatItem.is_actions_expanded = false;
            }
        },
        openImage: async function(url) {

            // convert data uri to blob
            const blob = await (await fetch(url)).blob();

            // create blob url
            const fileUrl = window.URL.createObjectURL(blob);

            // open new tab
            window.open(fileUrl);

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
        async processAudioForSelectedPeerChatItems() {
            for(const chatItem of this.selectedPeerChatItems){

                // skip if no audio
                if(!chatItem.lxmf_message?.fields?.audio){
                    continue;
                }

                // skip if audio already cached
                if(this.lxmfMessageAudioAttachmentCache[chatItem.lxmf_message.hash]){
                    continue;
                }

                // decode audio to blob url
                const objectUrl = await this.decodeLxmfAudioFieldToBlobUrl(chatItem.lxmf_message.fields.audio);
                if(!objectUrl){
                    continue;
                }

                // update audio cache
                this.lxmfMessageAudioAttachmentCache[chatItem.lxmf_message.hash] = objectUrl;

            }
        },
        async decodeLxmfAudioFieldToBlobUrl(audioField) {
            try {

                // get audio mode and audio bytes from audio field
                const audioMode = audioField.audio_mode;
                const audioBytes = audioField.audio_bytes;

                // handle opus: AM_OPUS_OGG
                if(audioMode === 0x10){
                    return this.decodeOpusAudioToBlobUrl(audioField.audio_bytes);
                }

                // determine codec2 mode, or skip if unknown
                const codecMode = this.lxmfAudioModeToCodec2ModeMap[audioMode];
                if(!codecMode){
                    console.log("unsupported audio mode: " + audioMode)
                    return null;
                }

                // convert base64 to uint8 array
                const encoded = this.base64ToArrayBuffer(audioBytes);

                // decode codec2 audio
                const decoded = await Codec2Lib.runDecode(codecMode, new Uint8Array(encoded));

                // convert decoded codec2 to wav audio
                const wavAudio = await Codec2Lib.rawToWav(decoded);

                // create blob from wav audio
                const blob = new Blob([wavAudio], {
                    type: "audio/wav",
                });

                // create object url for blob
                return URL.createObjectURL(blob);

            } catch(e) {
                // failed to decode lxmf audio field
                console.log(e);
                return null;
            }
        },
        async decodeOpusAudioToBlobUrl(audioBytes) {
            try {

                // convert base64 to uint8 array
                const opusAudioBytes = this.base64ToArrayBuffer(audioBytes);

                // create blob from opus audio
                const blob = new Blob([opusAudioBytes], {
                    type: "audio/opus",
                });

                // create object url for blob
                return URL.createObjectURL(blob);

            } catch(e) {
                // failed to decode opus audio
                console.log(e);
                return null;
            }
        },
        base64ToArrayBuffer: function(base64) {
            return Uint8Array.from(atob(base64), c => c.charCodeAt(0));
        },
        async deleteChatItem(chatItem, shouldConfirm = true) {
            try {

                // ask user to confirm deleting message
                if(shouldConfirm && !confirm("Are you sure you want to delete this message? This can not be undone!")){
                    return;
                }

                // make sure it's an lxmf message
                if(chatItem.type !== "lxmf_message"){
                    return;
                }

                // delete lxmf message from server
                await window.axios.delete(`/api/v1/lxmf-messages/${chatItem.lxmf_message.hash}`);

                // remove lxmf message from chat items using hash, as other pending items might not have an id yet
                this.chatItems = this.chatItems.filter((item) => {
                    return item.lxmf_message?.hash !== chatItem.lxmf_message.hash;
                });

            } catch(e) {
                // do nothing if failed to delete message
            }
        },
        async sendMessage() {

            // do nothing if can't send message
            if(!this.canSendMessage){
                return;
            }

            // do nothing if no peer selected
            if(!this.selectedPeer){
                return;
            }

            this.isSendingMessage = true;

            try {

                // build fields
                const fields = {};

                // add file attachments
                var fileAttachmentsTotalSize = 0;
                if(this.newMessageFiles.length > 0){
                    const fileAttachments = [];
                    for(const file of this.newMessageFiles){
                        fileAttachmentsTotalSize += file.size;
                        fileAttachments.push({
                            "file_name": file.name,
                            "file_bytes": Utils.arrayBufferToBase64(await file.arrayBuffer()),
                        });
                    }
                    fields["file_attachments"] = fileAttachments;
                }

                // add image attachment
                var imageTotalSize = 0;
                if(this.newMessageImage){
                    imageTotalSize = this.newMessageImage.size;
                    fields["image"] = {
                        // Reticulum sends image type as "jpg" or "png" and not "image/jpg" or "image/png"
                        "image_type": this.newMessageImage.type.replace("image/", ""),
                        "image_bytes": Utils.arrayBufferToBase64(await this.newMessageImage.arrayBuffer()),
                    };
                }

                // add audio attachment
                var audioTotalSize = 0;
                if(this.newMessageAudio){
                    audioTotalSize = this.newMessageAudio.size;
                    fields["audio"] = {
                        "audio_mode": this.newMessageAudio.audio_mode,
                        "audio_bytes": Utils.arrayBufferToBase64(await this.newMessageAudio.audio_blob.arrayBuffer()),
                    };
                }

                // calculate estimated message size in bytes
                const contentSize = this.newMessageText.length;
                const totalMessageSize = contentSize + fileAttachmentsTotalSize + imageTotalSize + audioTotalSize;

                // ask user if they still want to send message if it may be rejected by sender
                if(totalMessageSize > 1000 * 900){ // actual limit in LXMF Router is 1mb
                    if(!confirm(`Your message exceeds 900KB (It's ${this.formatBytes(totalMessageSize)}). It may be rejected by the recipient unless they have increased their delivery limit. Do you want to try sending anyway?`)){
                        return;
                    }
                }

                // send message to reticulum
                const response = await window.axios.post(`/api/v1/lxmf-messages/send`, {
                    "lxmf_message": {
                        "destination_hash": this.selectedPeer.destination_hash,
                        "content": this.newMessageText,
                        "fields": fields,
                    },
                });

                // add outbound message to ui
                if(!this.isLxmfMessageInUi(response.data.lxmf_message.hash)){
                    this.chatItems.push({
                        "type": "lxmf_message",
                        "lxmf_message": response.data.lxmf_message,
                        "is_outbound": true,
                    });
                }

                // always scroll to bottom since we just sent a message
                this.scrollMessagesToBottom();

                // clear message inputs
                this.newMessageText = "";
                this.newMessageImage = null;
                this.newMessageImageUrl = null;
                this.newMessageAudio = null;
                this.newMessageFiles = [];
                this.clearImageInput();
                this.clearFileInput();

            } catch(e) {

                // show error
                const message = e.response?.data?.message ?? "failed to send message";
                DialogUtils.alert(message);
                console.log(e);

            } finally {
                this.isSendingMessage = false;
            }

        },
        async retrySendingMessage(chatItem) {

            // force delete existing message
            await this.deleteChatItem(chatItem, false);

            try {

                // send message to reticulum
                const response = await window.axios.post(`/api/v1/lxmf-messages/send`, {
                    "lxmf_message": {
                        "destination_hash": chatItem.lxmf_message.destination_hash,
                        "content": chatItem.lxmf_message.content,
                        "fields": chatItem.lxmf_message.fields,
                    },
                });

                // add outbound message to ui
                if(!this.isLxmfMessageInUi(response.data.lxmf_message.hash)){
                    this.chatItems.push({
                        "type": "lxmf_message",
                        "lxmf_message": response.data.lxmf_message,
                        "is_outbound": true,
                    });
                }

                // always scroll to bottom since we just sent a message
                this.scrollMessagesToBottom();

            } catch(e) {

                // show error
                const message = e.response?.data?.message ?? "failed to send message";
                DialogUtils.alert(message);
                console.log(e);

            }

        },
        formatTimeAgo: function(datetimeString) {
            return Utils.formatTimeAgo(datetimeString);
        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
        onFileInputChange: function(event) {
            for(const file of event.target.files){
                this.newMessageFiles.push(file);
            }
        },
        clearFileInput: function() {
            this.$refs["file-input"].value = null;
        },
        removeImageAttachment: function() {
            this.newMessageImage = null;
            this.newMessageImageUrl = null;
        },
        onImageInputChange: function(event) {
            if(event.target.files.length > 0){

                // update selected file
                this.newMessageImage = event.target.files[0];

                // update image url when file is read
                const fileReader = new FileReader();
                fileReader.onload = (event) => {
                    this.newMessageImageUrl = event.target.result
                }

                // convert image to data url
                fileReader.readAsDataURL(this.newMessageImage);

                // clear image input to allow selecting the same file after user removed it
                this.clearImageInput();

            }
        },
        clearImageInput: function() {
            this.$refs["image-input"].value = null;
        },
        async startRecordingAudioAttachment(args) {

            // do nothing if already recording
            if(this.isRecordingAudioAttachment){
                return;
            }

            // ask user to confirm recording new audio attachment, if an existing audio attachment exists
            if(this.newMessageAudio && !confirm("An audio recording is already attached. A new recording will replace it. Do you want to continue?")){
                return;
            }

            // handle selected codec
            switch(args.codec){
                case "codec2": {

                    // start recording microphone
                    this.audioAttachmentMicrophoneRecorder = new Codec2MicrophoneRecorder();
                    this.audioAttachmentMicrophoneRecorder.codec2Mode = args.mode;
                    this.audioAttachmentRecordingStartedAt = Date.now();
                    this.isRecordingAudioAttachment = await this.audioAttachmentMicrophoneRecorder.start();

                    // update recording time in ui every second
                    this.audioAttachmentRecordingDuration = Utils.formatMinutesSeconds(0);
                    this.audioAttachmentRecordingTimer = setInterval(() => {
                        const recordingDurationMillis = Date.now() - this.audioAttachmentRecordingStartedAt;
                        const recordingDurationSeconds = recordingDurationMillis / 1000;
                        this.audioAttachmentRecordingDuration = Utils.formatMinutesSeconds(recordingDurationSeconds);
                    }, 1000);

                    // alert if failed to start recording
                    if(!this.isRecordingAudioAttachment){
                        DialogUtils.alert("failed to start recording");
                    }

                    break;

                }
                default: {
                    DialogUtils.alert(`Unhandled microphone recorder codec: ${args.codec}`);
                    break;
                }
            }

        },
        async stopRecordingAudioAttachment() {

            // clear audio recording timer
            clearInterval(this.audioAttachmentRecordingTimer);

            // do nothing if not recording
            if(!this.isRecordingAudioAttachment){
                return;
            }

            // stop recording microphone and get audio
            this.isRecordingAudioAttachment = false;
            const audio = await this.audioAttachmentMicrophoneRecorder.stop();

            // do nothing if no audio was provided
            if(audio.length === 0){
                return;
            }

            // decode codec2 audio back to wav so we can show a preview audio player before user sends it
            const codec2Mode = this.audioAttachmentMicrophoneRecorder.codec2Mode;
            const decoded = await Codec2Lib.runDecode(codec2Mode, new Uint8Array(audio));

            // convert decoded codec2 to wav audio and create a blob
            const wavAudio = await Codec2Lib.rawToWav(decoded);
            const wavBlob = new Blob([wavAudio], {
                type: "audio/wav",
            });

            // determine audio mode
            var audioMode = null;
            switch(codec2Mode){
                case "1200": {
                    audioMode = 0x04; // LXMF.AM_CODEC2_1200
                    break;
                }
                case "3200": {
                    audioMode = 0x09; // LXMF.AM_CODEC2_3200
                    break;
                }
                default: {
                    DialogUtils.alert(`Unhandled microphone recorder codec2Mode: ${codec2Mode}`);
                    return;
                }
            }

            // update message audio attachment
            this.newMessageAudio = {
                audio_mode: audioMode,
                audio_blob: new Blob([audio]),
                audio_wav_url: URL.createObjectURL(wavBlob),
            };

        },
        removeAudioAttachment: function() {

            // ask user to confirm removing audio attachment
            if(!confirm("Are you sure you want to remove this audio attachment?")){
                return;
            }

            // remove audio
            this.newMessageAudio = null;

        },
        removeFileAttachment: function(file) {
            this.newMessageFiles = this.newMessageFiles.filter((newMessageFile) => {
                return newMessageFile !== file;
            });
        },
        addNewLine: function() {
            this.newMessageText += "\n";
        },
        onEnterPressed: function() {

            // add new line on mobile
            if(this.isMobile){
                this.addNewLine();
                return;
            }

            // send message on desktop
            this.sendMessage();

        },
        onShiftEnterPressed: function() {
            this.addNewLine();
        },
        addFilesToMessage: function() {
            this.$refs["file-input"].click();
        },
        addImageToMessage: function() {
            this.$refs["image-input"].click();
        },
        findConversation: function(destinationHash) {
            return this.conversations.find((conversation) => {
                return conversation.destination_hash === destinationHash;
            });
        },
        async markConversationAsRead(conversation) {

            // manually mark conversation read in memory to avoid delay updating ui
            conversation.is_unread = false;

            // mark conversation as read on server
            try {
                await window.axios.get(`/api/v1/lxmf/conversations/${conversation.destination_hash}/mark-as-read`);
            } catch(e) {
                // do nothing if failed to mark as read
                console.log(e);
            }

            // reload conversations
            this.$emit("reload-conversations");

        },
        showSentMessageInfo: function(lxmfMessage) {
            DialogUtils.alert([
                `Created: ${Utils.convertUnixMillisToLocalDateTimeString(lxmfMessage.timestamp * 1000)}`,
                `Method: ${lxmfMessage.method ?? "unknown"}`,
            ].join("\n"));
        },
        showReceivedMessageInfo: function(lxmfMessage) {

            // basic info
            const info = [
                `Sent: ${Utils.convertUnixMillisToLocalDateTimeString(lxmfMessage.timestamp * 1000)}`,
                `Received: ${Utils.convertDateTimeToLocalDateTimeString(new Date(lxmfMessage.created_at))}`,
                `Method: ${lxmfMessage.method ?? "unknown"}`,
            ];

            // add signal quality if available
            if(lxmfMessage.quality != null){
                info.push(`Signal Quality: ${lxmfMessage.quality}%`);
            }

            // add rssi if available
            if(lxmfMessage.rssi != null){
                info.push(`RSSI: ${lxmfMessage.rssi}dBm`);
            }

            // add snr if available
            if(lxmfMessage.snr != null){
                info.push(`SNR: ${lxmfMessage.snr}dB`);
            }

            // show message info
            DialogUtils.alert(info.join("\n"));

        },
    },
    computed: {
        isMobile() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        },
        canSendMessage() {

            // can't send if empty message
            const messageText = this.newMessageText.trim();
            if(messageText == null || messageText === ""){
                return false;
            }

            // can't send if already sending
            if(this.isSendingMessage){
                return false;
            }

            return true;

        },
        selectedPeerChatItems() {

            // get all chat items related to the selected peer
            if(this.selectedPeer){
                return this.chatItems.filter((chatItem) => {

                    if(chatItem.type === "lxmf_message"){
                        const isFromSelectedPeer = chatItem.lxmf_message.source_hash === this.selectedPeer.destination_hash;
                        const isToSelectedPeer = chatItem.lxmf_message.destination_hash === this.selectedPeer.destination_hash;
                        return isFromSelectedPeer || isToSelectedPeer;
                    }

                    return false;


                });
            }

            // no peer, so no chat items!
            return [];

        },
        selectedPeerChatItemsReversed() {
            // ensure a copy of the array is returned in reverse order
            return this.selectedPeerChatItems.map((message) => message).reverse();
        },
        oldestMessageId() {

            if(this.selectedPeerChatItems.length > 0){
                return this.selectedPeerChatItems[0].lxmf_message.id;
            }

            return null;

        },
    },
    watch: {
        selectedPeer() {
            this.initialLoad();
        },
        async selectedPeerChatItems() {

            // chat items for selected peer changed, so lets process any available audio
            await this.processAudioForSelectedPeerChatItems();

        },
    },
}
</script>
