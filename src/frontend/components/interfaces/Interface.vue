<template>
  <div class="border rounded bg-white shadow dark:bg-zinc-800 dark:border-zinc-700">

    <!-- IFAC info -->
    <div v-if="iface._stats?.ifac_signature != null"
         class="bg-gray-50 p-1 text-sm text-gray-500 space-x-1 border-b dark:bg-zinc-800  dark:border-zinc-700">
      <div class="flex text-sm">
        <div class="my-auto">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-4 text-green-500">
            <path fill-rule="evenodd"
                  d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z"
                  clip-rule="evenodd"/>
          </svg>
        </div>
        <span class="ml-1 my-auto">
                    <span class="text-green-500">{{ iface._stats.ifac_size * 8 }}-bit IFAC</span> with sig <span
            @click="onIFACSignatureClick(iface._stats.ifac_signature)" class="cursor-pointer">&lt;{{
            iface._stats.ifac_signature.slice(0, 6)
          }}...{{ iface._stats.ifac_signature.slice(-6) }}&gt;</span>
                </span>
      </div>
    </div>

    <div class="flex py-2">

      <!-- icon -->
      <div class="my-auto mx-2">

        <svg v-if="iface.type === 'AutoInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
             viewBox="0 0 256 256" class="size-6 dark:text-white">
          <path
              d="M219.31,108.68l-80-80a16,16,0,0,0-22.62,0l-80,80A15.87,15.87,0,0,0,32,120v96a8,8,0,0,0,8,8h64a8,8,0,0,0,8-8V160h32v56a8,8,0,0,0,8,8h64a8,8,0,0,0,8-8V120A15.87,15.87,0,0,0,219.31,108.68ZM208,208H160V152a8,8,0,0,0-8-8H104a8,8,0,0,0-8,8v56H48V120l80-80,80,80Z"></path>
        </svg>

        <svg v-else-if="iface.type === 'RNodeInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
             viewBox="0 0 256 256" class="size-6 dark:text-white">
          <path
              d="M128,88a40,40,0,1,0,40,40A40,40,0,0,0,128,88Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,152Zm73.71,7.14a80,80,0,0,1-14.08,22.2,8,8,0,0,1-11.92-10.67,63.95,63.95,0,0,0,0-85.33,8,8,0,1,1,11.92-10.67,80.08,80.08,0,0,1,14.08,84.47ZM69,103.09a64,64,0,0,0,11.26,67.58,8,8,0,0,1-11.92,10.67,79.93,79.93,0,0,1,0-106.67A8,8,0,1,1,80.29,85.34,63.77,63.77,0,0,0,69,103.09ZM248,128a119.58,119.58,0,0,1-34.29,84,8,8,0,1,1-11.42-11.2,103.9,103.9,0,0,0,0-145.56A8,8,0,1,1,213.71,44,119.58,119.58,0,0,1,248,128ZM53.71,200.78A8,8,0,1,1,42.29,212a119.87,119.87,0,0,1,0-168,8,8,0,1,1,11.42,11.2,103.9,103.9,0,0,0,0,145.56Z"></path>
        </svg>

        <svg
            v-else-if="iface.type === 'TCPClientInterface' || iface.type === 'TCPServerInterface' || iface.type === 'UDPInterface'"
            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256" class="size-6 dark:text-white">
          <path
              d="M128,24h0A104,104,0,1,0,232,128,104.12,104.12,0,0,0,128,24Zm88,104a87.61,87.61,0,0,1-3.33,24H174.16a157.44,157.44,0,0,0,0-48h38.51A87.61,87.61,0,0,1,216,128ZM102,168H154a115.11,115.11,0,0,1-26,45A115.27,115.27,0,0,1,102,168Zm-3.9-16a140.84,140.84,0,0,1,0-48h59.88a140.84,140.84,0,0,1,0,48ZM40,128a87.61,87.61,0,0,1,3.33-24H81.84a157.44,157.44,0,0,0,0,48H43.33A87.61,87.61,0,0,1,40,128ZM154,88H102a115.11,115.11,0,0,1,26-45A115.27,115.27,0,0,1,154,88Zm52.33,0H170.71a135.28,135.28,0,0,0-22.3-45.6A88.29,88.29,0,0,1,206.37,88ZM107.59,42.4A135.28,135.28,0,0,0,85.29,88H49.63A88.29,88.29,0,0,1,107.59,42.4ZM49.63,168H85.29a135.28,135.28,0,0,0,22.3,45.6A88.29,88.29,0,0,1,49.63,168Zm98.78,45.6a135.28,135.28,0,0,0,22.3-45.6h35.66A88.29,88.29,0,0,1,148.41,213.6Z"></path>
        </svg>

        <svg v-else-if="iface.type === 'SerialInterface'" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
             viewBox="0 0 256 256" class="size-6 dark:text-white">
          <path
              d="M252.44,121.34l-48-32A8,8,0,0,0,192,96v24H72V72h33a32,32,0,1,0,0-16H72A16,16,0,0,0,56,72v48H8a8,8,0,0,0,0,16H56v48a16,16,0,0,0,16,16h32v8a16,16,0,0,0,16,16h32a16,16,0,0,0,16-16V176a16,16,0,0,0-16-16H120a16,16,0,0,0-16,16v8H72V136H192v24a8,8,0,0,0,12.44,6.66l48-32a8,8,0,0,0,0-13.32ZM136,48a16,16,0,1,1-16,16A16,16,0,0,1,136,48ZM120,176h32v32H120Zm88-30.95V111l25.58,17Z"></path>
        </svg>

        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"
             class="size-6 dark:text-white">
          <path
              d="M140,180a12,12,0,1,1-12-12A12,12,0,0,1,140,180ZM128,72c-22.06,0-40,16.15-40,36v4a8,8,0,0,0,16,0v-4c0-11,10.77-20,24-20s24,9,24,20-10.77,20-24,20a8,8,0,0,0-8,8v8a8,8,0,0,0,16,0v-.72c18.24-3.35,32-17.9,32-35.28C168,88.15,150.06,72,128,72Zm104,56A104,104,0,1,1,128,24,104.11,104.11,0,0,1,232,128Zm-16,0a88,88,0,1,0-88,88A88.1,88.1,0,0,0,216,128Z"></path>
        </svg>

      </div>

      <!-- interface details -->
      <div>
        <div class="font-semibold leading-5 dark:text-white">{{ iface._name }}</div>
        <div class="text-sm flex space-x-1 dark:text-zinc-100">

          <!-- auto interface -->
          <div v-if="iface.type === 'AutoInterface'">
            {{ iface.type }} • Ethernet and WiFi
          </div>

          <!-- tcp client interface -->
          <div v-else-if="iface.type === 'TCPClientInterface'">
            {{ iface.type }} • {{ iface.target_host }}:{{ iface.target_port }}
          </div>

          <!-- tcp server interface -->
          <div v-else-if="iface.type === 'TCPServerInterface'">
            {{ iface.type }} • {{ iface.listen_ip }}:{{ iface.listen_port }}
          </div>

          <!-- other interface types -->
          <div v-else>{{ iface.type }}</div>

        </div>
      </div>

      <!-- enabled state badge -->
      <div class="ml-auto my-auto mr-2">
        <span v-if="isInterfaceEnabled(iface)"
              class="inline-flex items-center rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">Enabled</span>
        <span v-else
              class="inline-flex items-center rounded-full bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20">Disabled</span>
      </div>

      <!-- enable/disable interface button -->
      <div class="my-auto mr-1">
        <button v-if="isInterfaceEnabled(iface)" @click="disableInterface" type="button" class="cursor-pointer">
                    <span
                        class="flex text-gray-700 bg-gray-100 dark:bg-zinc-600 dark:text-white dark:hover:bg-zinc-700 dark:focus-visible:outline-zinc-500 hover:bg-gray-200 p-2 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                             stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                  d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9"/>
                        </svg>
                    </span>
        </button>
        <button v-else @click="enableInterface" type="button" class="cursor-pointer">
                    <span
                        class="flex text-gray-700 bg-gray-100 dark:bg-zinc-600 dark:text-white dark:hover:bg-zinc-700 dark:focus-visible:outline-zinc-500 hover:bg-gray-200 p-2 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                             stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                  d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9"/>
                        </svg>
                    </span>
        </button>
      </div>

      <div class="my-auto mr-2">
        <DropDownMenu>
          <template v-slot:button>
            <IconButton>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor" class="size-5">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z"/>
              </svg>
            </IconButton>
          </template>
          <template v-slot:items>

            <!-- enable/disable interface button -->
            <div class="border-b dark:border-zinc-700">

              <!-- enable interface button -->
              <DropDownMenuItem v-if="isInterfaceEnabled(iface)" @click="disableInterface">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                  <path fill-rule="evenodd"
                        d="M12 2.25a.75.75 0 0 1 .75.75v9a.75.75 0 0 1-1.5 0V3a.75.75 0 0 1 .75-.75ZM6.166 5.106a.75.75 0 0 1 0 1.06 8.25 8.25 0 1 0 11.668 0 .75.75 0 1 1 1.06-1.06c3.808 3.807 3.808 9.98 0 13.788-3.807 3.808-9.98 3.808-13.788 0-3.808-3.807-3.808-9.98 0-13.788a.75.75 0 0 1 1.06 0Z"
                        clip-rule="evenodd"/>
                </svg>
                <span>Disable Interface</span>
              </DropDownMenuItem>

              <DropDownMenuItem v-else @click="enableInterface">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                  <path fill-rule="evenodd"
                        d="M12 2.25a.75.75 0 0 1 .75.75v9a.75.75 0 0 1-1.5 0V3a.75.75 0 0 1 .75-.75ZM6.166 5.106a.75.75 0 0 1 0 1.06 8.25 8.25 0 1 0 11.668 0 .75.75 0 1 1 1.06-1.06c3.808 3.807 3.808 9.98 0 13.788-3.807 3.808-9.98 3.808-13.788 0-3.808-3.807-3.808-9.98 0-13.788a.75.75 0 0 1 1.06 0Z"
                        clip-rule="evenodd"/>
                </svg>
                <span>Enable Interface</span>
              </DropDownMenuItem>

            </div>

            <!-- edit interface button -->
            <DropDownMenuItem @click="editInterface">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                <path
                    d="M21.731 2.269a2.625 2.625 0 0 0-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 0 0 0-3.712ZM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 0 0-1.32 2.214l-.8 2.685a.75.75 0 0 0 .933.933l2.685-.8a5.25 5.25 0 0 0 2.214-1.32L19.513 8.2Z"/>
              </svg>
              <span>Edit Interface</span>
            </DropDownMenuItem>

            <!-- export interface button -->
            <DropDownMenuItem @click="exportInterface">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5">
                <path fill-rule="evenodd"
                      d="M12 2.25a.75.75 0 0 1 .75.75v11.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-4.5 4.5a.75.75 0 0 1-1.06 0l-4.5-4.5a.75.75 0 1 1 1.06-1.06l3.22 3.22V3a.75.75 0 0 1 .75-.75Zm-9 13.5a.75.75 0 0 1 .75.75v2.25a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5V16.5a.75.75 0 0 1 1.5 0v2.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V16.5a.75.75 0 0 1 .75-.75Z"
                      clip-rule="evenodd"/>
              </svg>
              <span>Export Interface</span>
            </DropDownMenuItem>

            <!-- delete interface button -->
            <div class="border-t dark:border-zinc-700">
              <DropDownMenuItem @click="deleteInterface">
                <svg class="size-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                        d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z"
                        clip-rule="evenodd"/>
                </svg>
                <span class="text-red-500">Delete Interface</span>
              </DropDownMenuItem>
            </div>

          </template>
        </DropDownMenu>
      </div>

    </div>

    <!-- extra interface details -->
    <div v-if="['UDPInterface', 'RNodeInterface'].includes(iface.type)"
         class="p-1 text-sm border-t dark:text-zinc-100 dark:border-zinc-700">

      <!-- udp interface -->
      <div v-if="iface.type === 'UDPInterface'">
        <div>Listen: {{ iface.listen_ip }}:{{ iface.listen_port }}</div>
        <div>Forward: {{ iface.forward_ip }}:{{ iface.forward_port }}</div>
      </div>

      <!-- rnode interface details -->
      <div v-else-if="iface.type === 'RNodeInterface'">
        <div>Port: {{ iface.port }}</div>
        <div>Frequency: {{ formatFrequency(iface.frequency) }}</div>
        <div>Bandwidth: {{ formatFrequency(iface.bandwidth) }}</div>
        <div>Spreading Factor: {{ iface.spreadingfactor }}</div>
        <div>Coding Rate: {{ iface.codingrate }}</div>
        <div>Transmit Power: {{ iface.txpower }}dBm</div>
      </div>

    </div>

    <div
        class="flex bg-gray-50 p-1 text-sm text-gray-500 space-x-1 border-t rounded-b dark:bg-zinc-800 dark:text-white dark:border-zinc-700">

      <!-- status -->
      <div v-if="iface._stats?.status === true" class="text-sm text-green-500">Connected</div>
      <div v-else class="text-sm text-red-500">Disconnected</div>

      <!-- stats -->
      <div>• Bitrate: {{ formatBitsPerSecond(iface._stats?.bitrate ?? 0) }}</div>
      <div>• TX: {{ formatBytes(iface._stats?.txb ?? 0) }}</div>
      <div>• RX: {{ formatBytes(iface._stats?.rxb ?? 0) }}</div>
      <div v-if="iface.type === 'RNodeInterface'">• Noise Floor: {{
          iface._stats?.noise_floor
        }} dBm
      </div>
      <div v-if="iface._stats?.clients">• Clients: {{ iface._stats?.clients }}</div>

    </div>

  </div>
</template>

<script>
import DialogUtils from "../../js/DialogUtils";
import Utils from "../../js/Utils";
import DropDownMenuItem from "../DropDownMenuItem.vue";
import IconButton from "../IconButton.vue";
import DropDownMenu from "../DropDownMenu.vue";

export default {
  name: 'Interface',
  components: {
    DropDownMenu,
    IconButton,
    DropDownMenuItem,
  },
  props: {
    iface: Object,
  },
  data() {
    return {};
  },
  methods: {
    onIFACSignatureClick: function (ifacSignature) {
      DialogUtils.alert(ifacSignature);
    },
    isInterfaceEnabled: function (iface) {
      return Utils.isInterfaceEnabled(iface);
    },
    enableInterface() {
      this.$emit("enable");
    },
    disableInterface() {
      this.$emit("disable");
    },
    editInterface() {
      this.$emit("edit");
    },
    exportInterface() {
      this.$emit("export");
    },
    deleteInterface() {
      this.$emit("delete");
    },
    formatBitsPerSecond: function (bits) {
      return Utils.formatBitsPerSecond(bits);
    },
    formatBytes: function (bytes) {
      return Utils.formatBytes(bytes);
    },
    formatFrequency(hz) {
      return Utils.formatFrequency(hz);
    },
  },
}
</script>
