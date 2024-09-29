import json
import RNS


# the interface a data provider should implement for the group server to function
# for example, you could store and retrieve this information from an sqlite database
# however, an interface is provided to allow you to do this however you want
class GroupDataProviderInterface:

    # gets member count of a group
    def get_member_count(self, group_destination_hash: bytes) -> int:
        raise Exception("Not Implemented")

    # check if a user is a member of a group
    def is_member(self, group_destination_hash: bytes, identity_hash: bytes) -> bool:
        raise Exception("Not Implemented")

    # adds a member to a group
    def add_member(self, group_destination_hash: bytes, identity_hash: bytes, display_name: str):
        raise Exception("Not Implemented")

    # removes a member from a group
    def remove_member(self, group_destination_hash: bytes, identity_hash: bytes):
        raise Exception("Not Implemented")


# a group chat server than can handle membership management
class GroupChatServer:

    GROUP_TYPE_PUBLIC = "public"

    def __init__(self, identity: RNS.Identity, data_provider: GroupDataProviderInterface, public_display_name: str, group_type: str):

        self.identity = identity
        self.data_provider = data_provider
        self.public_display_name = public_display_name
        self.group_type = group_type

        # create group destination
        self.group_destination = RNS.Destination(
            self.identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            "meshchat",
            "group",
        )

        # register request handlers
        self.group_destination.register_request_handler(path="/api/v1/info", response_generator=self.on_received_api_v1_info_request, allow=RNS.Destination.ALLOW_ALL)
        self.group_destination.register_request_handler(path="/api/v1/join", response_generator=self.on_received_api_v1_join_request, allow=RNS.Destination.ALLOW_ALL)
        self.group_destination.register_request_handler(path="/api/v1/leave", response_generator=self.on_received_api_v1_leave_request, allow=RNS.Destination.ALLOW_ALL)

    # announce group destination
    def announce(self):
        self.group_destination.announce(app_data=json.dumps({
            "group_type": self.group_type,
            "public_display_name": self.public_display_name,
            "members_count": self.data_provider.get_member_count(self.group_destination.hash),
        }).encode("utf-8"))
        print("[GroupChatServer] announced destination: " + RNS.prettyhexrep(self.group_destination.hash))

    # error response format
    def success_response(self, message):
        return json.dumps({
            "success": message,
        }).encode("utf-8")

    # error response format
    def error_response(self, message):
        return json.dumps({
            "error": message,
        }).encode("utf-8")

    # error response for requests that require an identity
    def identity_not_provided_error_response(self):
        return self.error_response("You must identity to to access this endpoint.")

    # /api/v1/info
    def on_received_api_v1_info_request(self, path, data, request_id, remote_identity, requested_at):
        return json.dumps({
            "group_type": self.group_type,
            "public_display_name": self.public_display_name,
            "members_count": self.data_provider.get_member_count(self.group_destination.hash),
        }).encode("utf-8")

    # /api/v1/join
    def on_received_api_v1_join_request(self, path, data: bytes | None, request_id, remote_identity: RNS.Identity | None, requested_at):

        # ensure user has identified
        if remote_identity is None:
            return self.identity_not_provided_error_response()

        # attempt to parse data as json
        display_name = None
        if data is not None:
            try:
                json_data = json.loads(data.decode("utf-8"))
                display_name = json_data["display_name"] or "Anonymous Peer"
            except:
                print("failed to parse request data as json")
                pass

        # ensure user is not already a member
        if self.data_provider.is_member(self.group_destination.hash, remote_identity.hash):
            return self.error_response("You are already a member of this group")

        if self.group_type == self.GROUP_TYPE_PUBLIC:
            self.data_provider.add_member(self.group_destination.hash, remote_identity.hash, display_name)
            return self.success_response("You are now a member of this group")
        else:
            return self.error_response("Unsupported group type")

    # /api/v1/leave
    def on_received_api_v1_leave_request(self, path, data, request_id, remote_identity: RNS.Identity | None, requested_at):

        # ensure user has identified
        if remote_identity is None:
            return self.identity_not_provided_error_response()

        # remove member from group
        self.data_provider.remove_member(self.group_destination.hash, remote_identity.hash)
        return self.success_response("You are no longer a member of this group")
