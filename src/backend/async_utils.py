import asyncio
from typing import Coroutine


class AsyncUtils:

    # remember main loop
    main_loop: asyncio.AbstractEventLoop | None = None

    @staticmethod
    def set_main_loop(loop: asyncio.AbstractEventLoop):
        AsyncUtils.main_loop = loop

    # this method allows running the provided async coroutine from within a sync function
    # it will run the async function on the main event loop if possible, otherwise it logs a warning
    @staticmethod
    def run_async(coroutine: Coroutine):

        # run provided coroutine on main event loop, ensuring thread safety
        if AsyncUtils.main_loop and AsyncUtils.main_loop.is_running():
            asyncio.run_coroutine_threadsafe(coroutine, AsyncUtils.main_loop)
            return

        # main event loop not running...
        print("WARNING: Main event loop not available. Could not schedule task.")
