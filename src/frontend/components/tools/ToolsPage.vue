<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- appearance -->
            <div class="bg-white dark:bg-zinc-800 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-gray-200 p-2 font-semibold">Tools</div>
                <div class="dark:divide-zinc-700 text-gray-900 dark:text-gray-100 p-2">
                    A collection of useful tools bundled with MeshChat
                </div>
            </div>

            <!-- ping -->
            <RouterLink :to="{ name: 'ping' }" class="group flex bg-white dark:bg-zinc-800 p-2 rounded shadow hover:bg-gray-50 dark:hover:bg-zinc-700">
                <div class="mr-2">
                    <div class="flex bg-gray-300 text-gray-500 rounded shadow p-2">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-10">
                            <path fill-rule="evenodd" d="M14.615 1.595a.75.75 0 0 1 .359.852L12.982 9.75h7.268a.75.75 0 0 1 .548 1.262l-10.5 11.25a.75.75 0 0 1-1.272-.71l1.992-7.302H3.75a.75.75 0 0 1-.548-1.262l10.5-11.25a.75.75 0 0 1 .913-.143Z" clip-rule="evenodd" />
                        </svg>
                    </div>
                </div>
                <div class="my-auto mr-auto dark:text-gray-200">
                    <div class="font-bold">Ping</div>
                    <div class="text-sm">Allows you to ping a destination hash.</div>
                </div>
                <div class="my-auto text-gray-400 group-hover:text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5"></path>
                    </svg>
                </div>
            </RouterLink>

            <!-- rnode flasher -->
            <a target="_blank" href="/rnode-flasher/index.html" class="group flex bg-white dark:bg-zinc-800 p-2 rounded shadow hover:bg-gray-50 dark:hover:bg-zinc-700">
                <div class="mr-2">
                    <div class="flex bg-gray-300 text-white rounded shadow">
                        <img src="/rnode-flasher/reticulum_logo_512.png" class="size-14"/>
                    </div>
                </div>
                <div class="my-auto mr-auto dark:text-gray-200">
                    <div class="font-bold">RNode Flasher</div>
                    <div class="text-sm">Flash RNode firmware to supported devices.</div>
                </div>
                <div class="my-auto text-gray-400 group-hover:text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5"></path>
                    </svg>
                </div>
            </a>

        </div>
    </div>
</template>

<script>

export default {
    name: 'ToolsPage',
}
</script>
