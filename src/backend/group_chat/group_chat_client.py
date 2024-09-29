import asyncio
import json
import time

import RNS


# a group chat client for interacting with group chat servers
class GroupChatClient:

    def __init__(self, group_destination_hash: bytes, user_identity: RNS.Identity):
        self.group_destination_hash = group_destination_hash
        self.user_identity = user_identity
        self.link: RNS.Link | None = None

    # connect to group chat server
    async def _connect(self, timeout_after_seconds: int = 15):

        # determine when to timeout connecting
        timeout_after_seconds = time.time() + timeout_after_seconds

        # check if we have a path to the destination
        if not RNS.Transport.has_path(self.group_destination_hash):

            # we don't have a path, so we need to request it
            RNS.Transport.request_path(self.group_destination_hash)

            # wait until we have a path, or give up after the configured timeout
            while not RNS.Transport.has_path(self.group_destination_hash) and time.time() < timeout_after_seconds:
                await asyncio.sleep(0.1)

        # find destination identity from hash
        destination_identity = RNS.Identity.recall(self.group_destination_hash)
        if destination_identity is None:

            # we have to bail out since we don't have the identity/path yet
            raise Exception("Could not find path to destination. Try again later.")

        # the group destination we will connect to
        group_destination = RNS.Destination(
            destination_identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            "meshchat",
            "group",
        )

        # create link to group destination
        self.link = RNS.Link(group_destination)

        # wait until we have established a link, or give up after the configured timeout
        while self.link.status is not RNS.Link.ACTIVE and time.time() < timeout_after_seconds:
            await asyncio.sleep(0.1)

        # if we still haven't established a link, bail out
        if self.link.status is not RNS.Link.ACTIVE:
            raise Exception("Could not establish link to destination.")

        # send our identity to be able to perform queries
        self.link.identify(self.user_identity)

    # makes a request over the link and returns an async response, or throws an exception on error
    async def request(self, path: str, data: bytes | None = None):

        # create future
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        # handle response
        def response_callback(request_receipt):
            loop.call_soon_threadsafe(future.set_result, request_receipt.response)

        # handle failure
        def failed_callback(error):
            loop.call_soon_threadsafe(future.set_exception, error)

        # if link is not active, connect now
        if self.link is None or self.link.status != RNS.Link.ACTIVE:
            await self._connect()

        # send request over link
        self.link.request(path, data=data, response_callback=response_callback, failed_callback=failed_callback)
        return await future

    # get info about group
    async def get_info(self):
        return await self.request("/api/v1/info")

    # join group
    async def join(self, display_name: str):
        return await self.request("/api/v1/join", data=json.dumps({
            "display_name": display_name,
        }).encode("utf-8"))

    # leave group
    async def leave(self):
        return await self.request("/api/v1/leave")

    # get group members
    async def get_members(self, page: int, limit: int):
        return await self.request("/api/v1/members", data=json.dumps({
            "page": page,
            "limit": limit,
        }).encode("utf-8"))
