<template>
    <div class="bg-white rounded shadow divide-y divide-gray-300 dark:divide-zinc-700 dark:bg-zinc-900 overflow-hidden">
        <div @click="isExpanded = !isExpanded" class="flex p-2 justify-between cursor-pointer hover:bg-gray-50 dark:hover:bg-zinc-800">
            <div class="my-auto mr-auto">
                <div class="font-bold dark:text-white">
                    <slot name="title"/>
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-300">
                    <slot name="subtitle"/>
                </div>
            </div>
            <div class="my-auto ml-2">
                <div class="w-5 h-5 text-gray-600 dark:text-gray-300 transform transition-transform duration-200" :class="{ 'rotate-90': isExpanded }">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" class="size-5">
                        <rect width="256" height="256" fill="none"/>
                        <path d="M181.66,122.34l-80-80A8,8,0,0,0,88,48V208a8,8,0,0,0,13.66,5.66l80-80A8,8,0,0,0,181.66,122.34Z" fill="currentColor"/>
                    </svg>
                </div>
            </div>
        </div>
        <div v-if="isExpanded" class="divide-y divide-gray-200 dark:text-white">
            <slot name="content"/>
        </div>
    </div>
</template>
<script>
export default {
    name: 'ExpandingSection',
    data() {
        return {
            isExpanded: false,
        };
    },
}
</script>