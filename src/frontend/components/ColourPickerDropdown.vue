<template>
    <div v-click-outside="{ handler: onClickOutsideMenu, capture: true }" class="cursor-default relative inline-block text-left">

        <!-- menu button -->
        <div ref="dropdown-button" @click.stop="toggleMenu">
            <slot>
                <div class="size-8 border border-gray-50 dark:border-zinc-700 rounded shadow cursor-pointer" :style="{ 'background-color': colour }"></div>
            </slot>
        </div>

        <!-- drop down menu -->
        <Transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95">
            <div v-if="isShowingMenu" class="absolute left-0 z-10 ml-4">
                <v-color-picker v-model="colourPickerValue" :modes="['hex']" hide-inputs hide-sliders show-swatches></v-color-picker>
            </div>
        </Transition>

    </div>
</template>

<script>
import DropDownMenu from "./DropDownMenu.vue";
import IconButton from "./IconButton.vue";

export default {
    name: 'ColourPickerDropdown',
    components: {
        IconButton,
        DropDownMenu,
    },
    emits: [
        'update:colour',
    ],
    props: {
        colour: String,
    },
    data() {
        return {
            isShowingMenu: false,
            colourPickerValue: null,
        };
    },
    methods: {
        toggleMenu() {
            if(this.isShowingMenu){
                this.hideMenu();
            } else {
                this.showMenu();
            }
        },
        showMenu() {
            this.isShowingMenu = true;
        },
        hideMenu() {
            this.isShowingMenu = false;
        },
        onClickOutsideMenu(event) {
            if(this.isShowingMenu){
                event.preventDefault();
                this.hideMenu();
            }
        },
    },
    watch:{
        colour() {
            // update internal colour picker value when parent changes value of v-model:colour
            this.colourPickerValue = this.colour;
        },
        colourPickerValue() {

            // get current colour picker value
            var value = this.colourPickerValue;

            // remove alpha channel from hex colour if present
            if(value.length === 9){
                value = value.substring(0, 7);
            }

            // fire v-model:colour update event
            this.$emit("update:colour", value);

        },
    }
}
</script>
