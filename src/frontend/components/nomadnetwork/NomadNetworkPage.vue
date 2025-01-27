<template>

  <!-- nomadnetwork sidebar -->
  <NomadNetworkSidebar
      :nodes="nodes"
      :selected-destination-hash="selectedNode?.destination_hash"
      @node-click="onNodeClick"/>

  <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
    <!-- node -->
    <div v-if="selectedNode"
         class="flex flex-col h-full bg-white dark:bg-zinc-950 overflow-hidden sm:m-2 sm:border dark:border-zinc-800 sm:rounded-xl sm:shadow dark:shadow-zinc-900">
      <!-- header -->
      <div class="flex p-2 border-b border-gray-300 dark:border-zinc-800">
        <!-- node info -->
        <div class="my-auto dark:text-gray-100">
          <span class="font-semibold">{{ selectedNode.display_name }}</span>
          <span v-if="selectedNodePath" @click="onDestinationPathClick(selectedNodePath)"
                class="text-sm cursor-pointer"> - {{
              selectedNodePath.hops
            }} {{ selectedNodePath.hops === 1 ? 'hop' : 'hops' }} away</span>
        </div>

        <!-- close button -->
        <div class="my-auto ml-auto mr-2">
          <div @click="onCloseNodeViewer" class="cursor-pointer">
            <div
                class="flex text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-zinc-800 hover:bg-gray-200 dark:hover:bg-zinc-700 p-1 rounded-full">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                  <path
                      d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- browser navigation -->
      <div class="flex w-full border-gray-300 dark:border-zinc-800 border-b p-2">
        <button @click="loadNodePage(selectedNode.destination_hash, defaultNodePagePath)" type="button"
                class="my-auto text-gray-500 dark:text-gray-300 bg-gray-200 dark:bg-zinc-800 hover:bg-gray-300 dark:hover:bg-zinc-700 rounded p-1 cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd"
                  d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
        <button @click="reloadNodePage" type="button"
                class="ml-1 my-auto text-gray-500 dark:text-gray-300 bg-gray-200 dark:bg-zinc-800 hover:bg-gray-300 dark:hover:bg-zinc-700 rounded p-1 cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd"
                  d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.433a.75.75 0 0 0 0-1.5H3.989a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39Zm1.23-3.723a.75.75 0 0 0 .219-.53V2.929a.75.75 0 0 0-1.5 0V5.36l-.31-.31A7 7 0 0 0 3.239 8.188a.75.75 0 1 0 1.448.389A5.5 5.5 0 0 1 13.89 6.11l.311.31h-2.432a.75.75 0 0 0 0 1.5h4.243a.75.75 0 0 0 .53-.219Z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
        <button @click="loadPreviousNodePage" type="button" :disabled="nodePagePathHistory.length === 0"
                :class="[ nodePagePathHistory.length > 0 ? 'text-gray-500 dark:text-gray-300 bg-gray-200 dark:bg-zinc-800 hover:bg-gray-300 dark:hover:bg-zinc-700' : 'text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-zinc-900']"
                class="ml-1 my-auto rounded p-1 cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd"
                  d="M17 10a.75.75 0 0 1-.75.75H5.612l4.158 3.96a.75.75 0 1 1-1.04 1.08l-5.5-5.25a.75.75 0 0 1 0-1.08l5.5-5.25a.75.75 0 1 1 1.04 1.08L5.612 9.25H16.25A.75.75 0 0 1 17 10Z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
        <div class="my-auto mx-2 w-full">
          <input v-model="nodePagePathUrlInput" @keyup.enter="onNodePageUrlClick(nodePagePathUrlInput)" type="text"
                 placeholder="Enter Destination URL"
                 class="bg-gray-50 dark:bg-zinc-900 border border-gray-300 dark:border-zinc-700 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2.5 py-1.5 dark:placeholder-gray-400">
        </div>
        <button @click="onNodePageUrlClick(nodePagePathUrlInput)" type="button"
                class="my-auto text-gray-500 dark:text-gray-300 bg-gray-200 dark:bg-zinc-800 hover:bg-gray-300 dark:hover:bg-zinc-700 rounded p-1 cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd"
                  d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
      </div>

      <!-- page content -->
      <div class="h-full overflow-y-scroll p-3 bg-black text-white nodeContainer">
        <div class="flex" v-if="isLoadingNodePage">
          <div class="my-auto">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                 viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          <div class="my-auto">Loading {{ nodePageProgress }}%</div>
        </div>
        <pre v-else v-html="nodePageContent" class="h-full break-words whitespace-pre-wrap"></pre>
      </div>

      <!-- file download bottom bar -->
      <div v-if="isDownloadingNodeFile"
           class="flex w-full border-gray-300 dark:border-zinc-800 border-t p-2 dark:text-gray-100">
        <div class="my-auto mr-2">
          <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <div class="my-auto">Downloading: {{ nodeFilePath }} ({{ nodeFileProgress }}%)</div>
      </div>
    </div>

    <!-- no node selected -->
    <div v-else class="flex flex-col mx-auto my-auto text-center leading-5 dark:text-gray-100">
      <div class="mx-auto mb-1">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
             class="w-6 h-6 dark:text-gray-300">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418"/>
        </svg>
      </div>
      <div class="font-semibold">No Active Node</div>
      <div>Select a Node to start browsing!</div>
      <div class="mx-auto mt-2">
        <button @click.stop="openUrl" type="button"
                class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500
                dark:bg-zinc-800 dark:text-white dark:hover:bg-zinc-700 dark:focus-visible:outline-zinc-500">
          Open a Nomadnet URL
        </button>
      </div>
    </div>
  </div>

</template>

<style>

pre {
  font-family: Roboto Mono Nerd Font, monospace;
  line-height: normal;
}

pre.text-wrap > div {
  display: flex;
  white-space: pre;
}

pre.text-wrap > div > :last-child {
  width: 100%;
  white-space: pre-wrap;
}

pre a:hover {
  text-decoration: underline;
}

</style>

<script>

import MicronParser from "../../js/MicronParser";
import DialogUtils from "../../js/DialogUtils";
import WebSocketConnection from "../../js/WebSocketConnection";
import NomadNetworkSidebar from "./NomadNetworkSidebar.vue";
import GlobalEmitter from "../../js/GlobalEmitter";

export default {
  name: 'NomadNetworkPage',
  components: {
    NomadNetworkSidebar,
  },
  props: {
    destinationHash: String,
  },
  data() {
    return {

      nodes: {},
      selectedNode: null,
      selectedNodePath: null,

      isLoadingNodePage: false,
      defaultNodePagePath: "/page/index.mu",
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
  beforeUnmount() {
    // stop listening for websocket messages
    WebSocketConnection.off("message", this.onWebsocketMessage);
  },
  mounted() {

    // listen for websocket messages
    WebSocketConnection.on("message", this.onWebsocketMessage);

    // fixme: this is called by the micron-parser.js
    window.onNodePageUrlClick = (url, options = null) => {
      this.onNodePageUrlClick(url, options);
    };

    // load nomadnetwork node if a destination hash was provided on page load
    if (this.destinationHash) {
      (async () => {
        // fetch updated announce as we are probably loading node page before we loaded the announces list
        await this.getNomadnetworkNodeAnnounce(this.destinationHash);
        await this.onNodePageUrlClick(`${this.destinationHash}:${this.defaultNodePagePath}`);
      })();
    }

    this.getNomadnetworkNodeAnnounces();

  },
  methods: {
    async onWebsocketMessage(message) {
      const json = JSON.parse(message.data);
      switch (json.type) {
        case 'announce': {
          const aspect = json.announce.aspect;
          if (aspect === "nomadnetwork.node") {
            this.updateNodeFromAnnounce(json.announce);
          }
          break;
        }
        case 'nomadnet.page.download': {

          // get data from server
          const nomadnetPageDownload = json.nomadnet_page_download;

          // find download callbacks
          const getNomadnetPageDownloadCallbackKey = this.getNomadnetPageDownloadCallbackKey(nomadnetPageDownload.destination_hash, nomadnetPageDownload.page_path);
          const nomadnetPageDownloadCallback = this.nomadnetPageDownloadCallbacks[getNomadnetPageDownloadCallbackKey];
          if (!nomadnetPageDownloadCallback) {
            console.log("did not find nomadnet page download callback for key: " + getNomadnetPageDownloadCallbackKey);
            return;
          }

          // handle success
          if (nomadnetPageDownload.status === "success" && nomadnetPageDownloadCallback.onSuccessCallback) {
            nomadnetPageDownloadCallback.onSuccessCallback(nomadnetPageDownload.page_content);
            delete this.nomadnetPageDownloadCallbacks[getNomadnetPageDownloadCallbackKey];
            return;
          }

          // handle failure
          if (nomadnetPageDownload.status === "failure" && nomadnetPageDownloadCallback.onFailureCallback) {
            nomadnetPageDownloadCallback.onFailureCallback(nomadnetPageDownload.failure_reason);
            delete this.nomadnetPageDownloadCallbacks[getNomadnetPageDownloadCallbackKey];
            return;
          }

          // handle progress
          if (nomadnetPageDownload.status === "progress" && nomadnetPageDownloadCallback.onProgressCallback) {
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
          if (!nomadnetFileDownloadCallback) {
            console.log("did not find nomadnet file download callback for key: " + getNomadnetFileDownloadCallbackKey);
            return;
          }

          // handle success
          if (nomadnetFileDownload.status === "success" && nomadnetFileDownloadCallback.onSuccessCallback) {
            nomadnetFileDownloadCallback.onSuccessCallback(nomadnetFileDownload.file_name, nomadnetFileDownload.file_bytes);
            delete this.nomadnetFileDownloadCallbacks[getNomadnetFileDownloadCallbackKey];
            return;
          }

          // handle failure
          if (nomadnetFileDownload.status === "failure" && nomadnetFileDownloadCallback.onFailureCallback) {
            nomadnetFileDownloadCallback.onFailureCallback(nomadnetFileDownload.failure_reason);
            delete this.nomadnetFileDownloadCallbacks[getNomadnetFileDownloadCallbackKey];
            return;
          }

          // handle progress
          if (nomadnetFileDownload.status === "progress" && nomadnetFileDownloadCallback.onProgressCallback) {
            nomadnetFileDownloadCallback.onProgressCallback(nomadnetFileDownload.progress);
            return;
          }

          break;

        }
      }
    },
    onDestinationPathClick: function (path) {
      DialogUtils.alert(`${path.hops} ${path.hops === 1 ? 'hop' : 'hops'} away via ${path.next_hop_interface}`);
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
        for (const nodeAnnounce of nodeAnnounces) {
          this.updateNodeFromAnnounce(nodeAnnounce);
        }

      } catch (e) {
        // do nothing if failed to load announces
        console.log(e);
      }
    },
    async getNomadnetworkNodeAnnounce(destinationHash) {
      try {

        // fetch announces for "nomadnetwork.node" aspect
        const response = await window.axios.get(`/api/v1/announces`, {
          params: {
            destination_hash: destinationHash,
            limit: 1,
          },
        });

        // update ui
        const nodeAnnounces = response.data.announces;
        for (const nodeAnnounce of nodeAnnounces) {
          this.updateNodeFromAnnounce(nodeAnnounce);
        }

      } catch (e) {
        // do nothing if failed to load announce
        console.log(e);
      }
    },
    updateNodeFromAnnounce: function (announce) {
      this.nodes[announce.destination_hash] = announce;
    },
    async openUrl() {

      // ask for url
      const url = await DialogUtils.prompt("Enter a Nomadnet URL");
      if (!url) {
        return;
      }

      // navigate to the url
      await this.onNodePageUrlClick(url);

    },
    async loadNodePage(destinationHash, pagePath, fieldData = null, addToHistory = true, loadFromCache = true) {

      // update current route
      this.$router.replace({
        name: "nomadnetwork",
        params: {
          destinationHash: destinationHash,
        },
      });

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
      if (addToHistory && previousNodePagePath != null && previousNodePagePath !== this.nodePagePath) {
        this.nodePagePathHistory.push(previousNodePagePath);
      }

      // check if we can load this page from the cache
      if (loadFromCache) {

        // load from cache
        const nodePagePathCacheKey = `${destinationHash}:${pagePath}`;
        const cachedNodePageContent = this.nodePageCache[nodePagePathCacheKey];

        // if page is cache, we can just return it now
        if (cachedNodePageContent != null) {
          this.nodePageContent = cachedNodePageContent;
          this.isLoadingNodePage = false;
          return;
        }

      }

      this.downloadNomadNetPage(destinationHash, pagePath, fieldData, (pageContent) => {

        const muParser = new MicronParser();

        // do nothing if callback is for a previous request
        if (seq !== this.nodePageRequestSequence) {
          console.log("ignoring page content callback for previous page request")
          return;
        }

        // check if page url ends with .mu but remove page data first
        // address:/page/index.mu`Data=123
        const [pagePathWithoutData, pageData] = pagePath.split("`");

        // convert micron to html if page ends with .mu extension
        // otherwise, we will just serve the content as is
        if (pagePathWithoutData.endsWith(".mu")) {
          this.nodePageContent = muParser.convertMicronToHtml(pageContent);
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
        if (seq !== this.nodePageRequestSequence) {
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
        if (seq !== this.nodePageRequestSequence) {
          console.log("ignoring progress callback for previous page request")
          return;
        }

        // update page content
        this.nodePageProgress = Math.round(progress * 100);

      });
    },
    async reloadNodePage() {

      // reload current node page without adding to history and without using cache
      this.onNodePageUrlClick(this.nodePagePath, null, false, false);

    },
    async loadPreviousNodePage() {

      // get the previous path from history, or do nothing
      const previousNodePagePath = this.nodePagePathHistory.pop();
      if (!previousNodePagePath) {
        return;
      }

      // load the page
      this.onNodePageUrlClick(previousNodePagePath, null, null, true);

    },
    parseNomadnetworkUrl: function (url) {

      // parse relative urls
      if (url.startsWith(":")) {

        // remove leading ":"
        var path = url.substring(1);

        // if page path is empty we should load default page path
        if (path === "") {
          path = this.defaultNodePagePath;
        }

        return {
          destination_hash: null, // node hash was not in provided url
          path: path,
        };

      }

      // parse absolute urls such as 00000000000000000000000000000000:/page/index.mu
      if (url.includes(":")) {

        // parse destination hash and url
        const [destinationHash, ...relativeUrl] = url.split(":");

        // ensure destination is expected length
        if (destinationHash.length === 32) {
          return {
            destination_hash: destinationHash,
            path: relativeUrl.join(":"),
          };
        }

      }

      // parse node id only
      if (url.length === 32) {
        return {
          destination_hash: url,
          path: this.defaultNodePagePath,
        };
      }

      // unsupported url
      return null;

    },
    async onNodePageUrlClick(url, options = null, addToHistory = true, useCache = false) {

      let fieldData = [];

      if (options === "*") {
        useCache = false; // we want to send another request with the field data
        const inputs = document.querySelectorAll('.nodeContainer input');

        const inputValues = {};

        for (const input of inputs) {
          if (input.type === 'radio' || input.type === 'checkbox') {
            // Only add if the input is checked
            if (input.checked) {
              inputValues[input.name] = input.value;
            }
          } else {
            // For other input types, just get the value
            inputValues[input.name || input.id || input.type] = input.value;
          }
        }

        fieldData = inputValues;
      } else if (options !== null && options !== "") {
        useCache = false;
        // split options into an array of names
        const validNames = options.split('|');

        // Select inputs within the container
        const inputs = document.querySelectorAll('.nodeContainer input');

        const inputValues = {};

        // Filter inputs by name and handle their values
        for (const input of inputs) {
          if (validNames.includes(input.name)) {
            if (input.type === 'radio' || input.type === 'checkbox') {
              // Only add if the input is checked
              if (input.checked) {
                inputValues[input.name] = input.value;
              }
            } else {
              // For other input types, just get the value
              inputValues[input.name] = input.value;
            }
          }
        }

        fieldData = inputValues;
      }

      console.log(fieldData);


      // open http urls in new tab
      if (url.startsWith("http://") || url.startsWith("https://")) {
        window.open(url, "_blank");
        return;
      }

      // lxmf urls should open the conversation
      if (url.startsWith("lxmf@")) {
        const destinationHash = url.replace("lxmf@", "");
        if (destinationHash.length === 32) {
          await this.$router.push({
            name: "messages",
            params: {
              destinationHash: destinationHash,
            },
          });
          return;
        }
      }

      // attempt to parse url
      const parsedUrl = this.parseNomadnetworkUrl(url);
      if (parsedUrl != null) {

        // use parsed destination hash, or fallback to selected node destination hash
        const destinationHash = parsedUrl.destination_hash || this.selectedNode.destination_hash;

        // download file
        if (parsedUrl.path.startsWith("/file/")) {

          // prevent simultaneous downloads
          if (this.isDownloadingNodeFile) {
            DialogUtils.alert("An existing download is in progress. Please wait for it to finish before starting another download.");
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
          display_name: "Unknown Node",
          destination_hash: destinationHash,
        };

        // navigate to node page
        this.loadNodePage(destinationHash, parsedUrl.path, fieldData, addToHistory, useCache);
        return;

      }

      // unsupported url
      DialogUtils.alert("unsupported url: " + url);

    },
    downloadFileFromBase64: async function (fileName, fileBytesBase64) {

      // create blob from base64 encoded file bytes
      const byteCharacters = atob(fileBytesBase64);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
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
    onNodeClick: function (node) {

      // update selected node
      this.selectedNode = node;

      // load default node page
      this.loadNodePage(node.destination_hash, this.defaultNodePagePath);

    },
    onCloseNodeViewer: function () {

      // clear selected node
      this.selectedNode = null;

      // update current route
      this.$router.replace({
        name: "nomadnetwork",
      });

    },
    getNomadnetPageDownloadCallbackKey: function (destinationHash, pagePath) {
      return `${destinationHash}:${pagePath}`;
    },
    getNomadnetFileDownloadCallbackKey: function (destinationHash, filePath) {
      return `${destinationHash}:${filePath}`;
    },
    async getNodePath(destinationHash) {

      // clear previous known path
      this.selectedNodePath = null;

      try {

        // get path to destination
        const response = await window.axios.get(`/api/v1/destination/${destinationHash}/path`);

        // update ui
        this.selectedNodePath = response.data.path;

      } catch (e) {
        console.log(e);
      }

    },
    downloadNomadNetFile(destinationHash, filePath, onSuccessCallback, onFailureCallback, onProgressCallback) {
      try {

        // set callbacks for nomadnet filePath download
        this.nomadnetFileDownloadCallbacks[this.getNomadnetFileDownloadCallbackKey(destinationHash, filePath)] = {
          onSuccessCallback: onSuccessCallback,
          onFailureCallback: onFailureCallback,
          onProgressCallback: onProgressCallback,
        };

        // ask reticulum to download file from nomadnet
        WebSocketConnection.send(JSON.stringify({
          "type": "nomadnet.file.download",
          "nomadnet_file_download": {
            "destination_hash": destinationHash,
            "file_path": filePath,
          },
        }));

      } catch (e) {
        console.error(e);
      }
    },
    downloadNomadNetPage(destinationHash, pagePath, fieldData, onSuccessCallback, onFailureCallback, onProgressCallback) {
      try {

        // set callbacks for nomadnet page download
        this.nomadnetPageDownloadCallbacks[this.getNomadnetPageDownloadCallbackKey(destinationHash, pagePath)] = {
          onSuccessCallback: onSuccessCallback,
          onFailureCallback: onFailureCallback,
          onProgressCallback: onProgressCallback,
        };

        // ask reticulum to download page from nomadnet
        WebSocketConnection.send(JSON.stringify({
          "type": "nomadnet.page.download",
          "nomadnet_page_download": {
            "destination_hash": destinationHash,
            "page_path": pagePath,
            "field_data": fieldData,
          },
        }));

      } catch (e) {
        console.error(e);
      }
    },
  },
}
</script>
