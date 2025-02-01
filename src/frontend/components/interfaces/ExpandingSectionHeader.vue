<template>
    <div class="flex items-center justify-between cursor-pointer p-2 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-zinc-800 dark:hover:bg-zinc-700">
        <span class="font-semibold text-gray-900 dark:text-gray-100">
            <slot/>
        </span>
        <span class="w-5 h-5 text-gray-600 dark:text-gray-300 transform transition-transform duration-200" :class="{ 'rotate-90': isExpanded }">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" class="size-5">
                <rect width="256" height="256" fill="none"/>
                <path d="M181.66,122.34l-80-80A8,8,0,0,0,88,48V208a8,8,0,0,0,13.66,5.66l80-80A8,8,0,0,0,181.66,122.34Z"/>
            </svg>
        </span>
    </div>
</template>
<script>
export default {
    name: 'ExpandingSectionHeader',
    props: {
        isExpanded: Boolean,
    },
}
</script>