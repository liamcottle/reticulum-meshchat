<template>
    <div class="cursor-pointer flex p-3 space-x-2 text-sm bg-white text-gray-500 hover:bg-gray-100 dark:bg-zinc-800 dark:text-white dark:hover:bg-zinc-700">
        <slot/>
    </div>
</template>

<script>
export default {
    name: 'DropDownMenuItem',
}
</script>
