<template>
    <div v-if="iconName" class="p-2 rounded" :style="{ 'color': iconForegroundColour, 'background-color': iconBackgroundColour }">
        <MaterialDesignIcon :icon-name="iconName" class="size-6"/>
    </div>
    <div v-else class="bg-gray-200 dark:bg-zinc-700 text-gray-500 dark:text-gray-400 p-2 rounded">
        <MaterialDesignIcon icon-name="account-outline" class="size-6"/>
    </div>
</template>

<script>
import MaterialDesignIcon from "./MaterialDesignIcon.vue";
export default {
    name: "LxmfUserIcon",
    components: {
        MaterialDesignIcon,
    },
    props: {
        iconName: String,
        iconForegroundColour: String,
        iconBackgroundColour: String,
    },
}
</script>
