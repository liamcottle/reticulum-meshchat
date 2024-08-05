<template>
    <RouterLink :to="to" v-slot="{ href, route, navigate, isActive, isExactActive }" custom>
        <a :href="href" @click="handleNavigate($event, navigate)" type="button" :class="[ isExactActive ? 'bg-blue-100 text-blue-800 group:text-blue-800' : 'hover:bg-gray-100']" class="w-full text-gray-800 group flex gap-x-3 rounded-r-full p-2 mr-2 text-sm leading-6 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
            <span class="my-auto">
                <slot name="icon"></slot>
            </span>
            <span class="my-auto flex w-full">
                <slot name="text"></slot>
            </span>
        </a>
    </RouterLink>
</template>

<script>
export default {
    name: 'SidebarLink',
    props: {
        to: Object,
    },
    methods: {
        handleNavigate(event, navigate) {

            // emit click event for SidebarLink element
            this.$emit('click');

            // handle navigation
            navigate(event);

        },
    },
};
</script>
