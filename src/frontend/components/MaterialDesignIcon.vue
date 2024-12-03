<template>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" :aria-label="iconName" fill="currentColor" style="display:inline-block;vertical-align:middle;">
        <path :d="iconPath"/>
    </svg>
</template>

<script>
import * as mdi from "@mdi/js";

export default {
    name: "MaterialDesignIcon",
    props: {
        iconName: {
            type: String,
            required: true,
        },
    },
    computed: {
        mdiIconName() {
            // convert icon name from lxmf icon appearance to format expected by the @mdi/js library
            // e.g: alien-outline -> mdiAlienOutline
            // https://pictogrammers.github.io/@mdi/font/5.4.55/
            return "mdi" + this.iconName.split("-").map((word) => {
                // capitalise first letter of each part
                return word.charAt(0).toUpperCase() + word.slice(1);
            }).join("");
        },
        iconPath() {
            // find icon, otherwise fallback to question mark, and if that doesn't exist, show nothing...
            return mdi[this.mdiIconName] || mdi["mdiProgressQuestion"] || "";
        },
    },
};
</script>
