# an announce handler that forwards announces to a provided callback for the provided aspect filter
# this handler exists so we can have access to the original aspect, as this is not provided in the announce itself
class AnnounceHandler:

    def __init__(self, aspect_filter: str, received_announce_callback):
        self.aspect_filter = aspect_filter
        self.received_announce_callback = received_announce_callback

    # we will just pass the received announce back to the provided callback
    def received_announce(self, destination_hash, announced_identity, app_data):
        try:
            # handle received announce
            self.received_announce_callback(self.aspect_filter, destination_hash, announced_identity, app_data)
        except:
            # ignore failure to handle received announce
            pass
