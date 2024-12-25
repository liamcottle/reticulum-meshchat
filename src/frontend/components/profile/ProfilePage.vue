<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- info -->
            <div class="bg-white dark:bg-zinc-800 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-gray-200 p-2 font-semibold">Customise your Profile Icon</div>
                <div class="text-gray-900 dark:text-gray-100">
                    <div class="text-sm p-2">
                        <ul class="list-disc list-inside">
                            <li>Personalise your profile with a custom coloured icon.</li>
                            <li>This icon will be sent in all of your outgoing messages.</li>
                            <li>When you send someone a message, they will see your new icon.</li>
                            <li>You can <span @click="removeProfileIcon" class="cursor-pointer underline text-blue-500">remove your icon</span>, however it will still show for anyone that already received it.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- colours -->
            <div class="bg-white dark:bg-zinc-800 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-gray-200 p-2 font-semibold">Select your Colours</div>
                <div class="divide-y divide-gray-300 dark:divide-zinc-700 text-gray-900 dark:text-gray-100">

                    <!-- icon colour -->
                    <div class="p-2">
                        <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Icon Colour</div>
                        <div class="flex">
                            <select v-model="iconForegroundColour" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-600 dark:focus:border-blue-600 block w-full p-2.5">
                                <option value="#000000">Black</option>
                                <option value="#FFFFFF">White</option>
                                <option disabled></option>
                                <option value="#64748b">Slate</option>
                                <option value="#6b7280">Gray</option>
                                <option value="#71717a">Zinc</option>
                                <option value="#737373">Neutral</option>
                                <option value="#78716c">Stone</option>
                                <option disabled></option>
                                <option value="#ef4444">Red</option>
                                <option value="#f97316">Orange</option>
                                <option value="#f59e0b">Amber</option>
                                <option value="#eab308">Yellow</option>
                                <option value="#84cc16">Lime</option>
                                <option value="#22c55e">Green</option>
                                <option value="#10b981">Emerald</option>
                                <option value="#14b8a6">Teal</option>
                                <option value="#06b6d4">Cyan</option>
                                <option value="#0ea5e9">Sky</option>
                                <option value="#3b82f6">Blue</option>
                                <option value="#6366f1">Indigo</option>
                                <option value="#8b5cf6">Violet</option>
                                <option value="#a855f7">Purple</option>
                                <option value="#d946ef">Fuschia</option>
                                <option value="#ec4899">Pink</option>
                                <option value="#f43f5e">Rose</option>
                            </select>
                        </div>
                    </div>

                    <!-- background colour -->
                    <div class="p-2">
                        <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Background Colour</div>
                        <div class="flex">
                            <select v-model="iconBackgroundColour" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-600 dark:focus:border-blue-600 block w-full p-2.5">
                                <option value="#000000">Black</option>
                                <option value="#FFFFFF">White</option>
                                <option disabled></option>
                                <option value="#64748b">Slate</option>
                                <option value="#6b7280">Gray</option>
                                <option value="#71717a">Zinc</option>
                                <option value="#737373">Neutral</option>
                                <option value="#78716c">Stone</option>
                                <option disabled></option>
                                <option value="#ef4444">Red</option>
                                <option value="#f97316">Orange</option>
                                <option value="#f59e0b">Amber</option>
                                <option value="#eab308">Yellow</option>
                                <option value="#84cc16">Lime</option>
                                <option value="#22c55e">Green</option>
                                <option value="#10b981">Emerald</option>
                                <option value="#14b8a6">Teal</option>
                                <option value="#06b6d4">Cyan</option>
                                <option value="#0ea5e9">Sky</option>
                                <option value="#3b82f6">Blue</option>
                                <option value="#6366f1">Indigo</option>
                                <option value="#8b5cf6">Violet</option>
                                <option value="#a855f7">Purple</option>
                                <option value="#d946ef">Fuschia</option>
                                <option value="#ec4899">Pink</option>
                                <option value="#f43f5e">Rose</option>
                            </select>
                        </div>
                    </div>

                </div>
            </div>

            <!-- search icons -->
            <div class="bg-white dark:bg-zinc-800 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-gray-200 p-2 font-semibold">Select your Icon</div>
                <div class="divide-y divide-gray-300 dark:divide-zinc-700 text-gray-900 dark:text-gray-100">
                    <div class="flex p-1">
                        <input v-model="search" type="text" :placeholder="`Search ${iconNames.length} icons...`" class="bg-gray-50 dark:bg-zinc-700 border border-gray-300 dark:border-zinc-600 text-gray-900 dark:text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-600 dark:focus:border-blue-600 block w-full p-2.5">
                    </div>
                    <div class="divide-y">
                        <div @click="onIconClick(mdiIconName)" v-for="mdiIconName of searchedIconNames" class="flex space-x-1 p-2 cursor-pointer hover:bg-gray-100">
                            <div class="my-auto">
                                <LxmfUserIcon :icon-name="mdiIconName" :icon-foreground-colour="iconForegroundColour" :icon-background-colour="iconBackgroundColour"/>
                            </div>
                            <div class="my-auto">{{ mdiIconName }}</div>
                        </div>
                        <div v-if="searchedIconNames.length === 0" class="p-1 text-sm text-gray-500">No icons match your search.</div>
                        <div v-if="searchedIconNames.length === maxSearchResults" class="p-1 text-sm text-gray-500">A maximum of {{ maxSearchResults }} icons are shown.</div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import * as mdi from "@mdi/js";
import MaterialDesignIcon from "../../../../build/exe/lib/src/frontend/components/MaterialDesignIcon.vue";
import LxmfUserIcon from "../LxmfUserIcon.vue";
import DialogUtils from "../../js/DialogUtils";
export default {
    name: 'ProfilePage',
    components: {
        LxmfUserIcon,
        MaterialDesignIcon,
    },
    data() {
        return {

            config: null,
            iconForegroundColour: null,
            iconBackgroundColour: null,

            search: "",
            maxSearchResults: 100,
            iconNames: [],

        };
    },
    mounted() {

        this.getConfig();

        // load icon names
        this.iconNames = Object.keys(mdi).map((mdiIcon) => {
            return mdiIcon
                .replace(/^mdi/, '') // Remove the "mdi" prefix
                .replace(/([a-z])([A-Z])/g, '$1-$2') // Add a hyphen between lowercase and uppercase letters
                .toLowerCase(); // Convert the entire string to lowercase
        });

    },
    methods: {
        async getConfig() {
            try {
                const response = await window.axios.get("/api/v1/config");
                this.config = response.data.config;
            } catch(e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        async updateConfig(config) {
            try {
                const response = await window.axios.patch("/api/v1/config", config);
                this.config = response.data.config;
            } catch(e) {
                alert("Failed to save config!");
                console.log(e);
            }
        },
        async onIconClick(iconName) {

            // ensure foreground colour set
            if(this.iconForegroundColour == null){
                DialogUtils.alert("Please select an icon colour first");
                return;
            }

            // ensure background colour set
            if(this.iconBackgroundColour == null){
                DialogUtils.alert("Please select a background colour first");
                return;
            }

            // confirm user wants to update their icon
            if(!confirm("Are you sure you want to set this as your profile icon?")){
                return;
            }

            // save icon appearance
            await this.updateConfig({
                "lxmf_user_icon_name": iconName,
                "lxmf_user_icon_foreground_colour": this.iconForegroundColour,
                "lxmf_user_icon_background_colour": this.iconBackgroundColour,
            });

        },
        async removeProfileIcon() {

            // confirm user wants to remove their icon
            if(!confirm("Are you sure you want to remove your profile icon? Anyone that has already received it will continue to see it until you send them a new icon.")){
                return;
            }

            // remove profile icon
            await this.updateConfig({
                "lxmf_user_icon_name": null,
                "lxmf_user_icon_foreground_colour": null,
                "lxmf_user_icon_background_colour": null,
            });

        }
    },
    computed: {
        searchedIconNames() {
            return this.iconNames.filter((iconName) => {
                return iconName.includes(this.search);
            }).slice(0, this.maxSearchResults);
        },
    },
    watch: {
        config() {
            // update ui when config is updated
            this.iconName = this.config.lxmf_user_icon_name;
            this.iconForegroundColour = this.config.lxmf_user_icon_foreground_colour || "#000000";
            this.iconBackgroundColour = this.config.lxmf_user_icon_background_colour || "#FFFFFF";
        },
    },
}
</script>
