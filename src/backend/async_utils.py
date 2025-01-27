import asyncio


class AsyncUtils:

    # this method allows running the provided async coroutine from within a sync function
    # it will run the async function on the existing event loop if available, otherwise it will start a new event loop
    @staticmethod
    def run_async(coroutine):

        # attempt to get existing event loop
        existing_event_loop = None
        try:
            existing_event_loop = asyncio.get_running_loop()
        except RuntimeError:
            # 'RuntimeError: no running event loop'
            pass

        # if there is an existing event loop running, submit the coroutine to that loop
        if existing_event_loop and existing_event_loop.is_running():
            existing_event_loop.create_task(coroutine)
            return

        # otherwise start a new event loop to run the coroutine
        asyncio.run(coroutine)
