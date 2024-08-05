import { reactive } from "vue";

// global state
const globalState = reactive({
    unreadConversationsCount: 0,
});

export default globalState;
