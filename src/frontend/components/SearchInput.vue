<template>
    <div class="relative w-full">
        <input :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" type="text" v-bind="$attrs" class="pr-8">
        <button v-if="modelValue" @click="$emit('update:modelValue', '')" type="button" class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
</template>

<script>
export default {
    name: 'SearchInput',
    inheritAttrs: false,
    props: {
        modelValue: {
            type: String,
            default: "",
        },
    },
    emits: ["update:modelValue"],
}
</script>
