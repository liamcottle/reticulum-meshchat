import RNS.vendor.configobj


class InterfaceConfigParser:

    @staticmethod
    def parse(text):

        # get lines from provided text
        lines = text.splitlines()

        # ensure [interfaces] section exists
        if "[interfaces]" not in lines:
            lines.insert(0, "[interfaces]")

        # parse lines as rns config object
        config = RNS.vendor.configobj.ConfigObj(lines)

        # get interfaces from config
        config_interfaces = config.get("interfaces")

        # process interfaces
        interfaces = []
        for interface_name in config_interfaces:

            # ensure interface has a name
            interface_config = config_interfaces[interface_name]
            interface_config["name"] = interface_name
            interfaces.append(interface_config)

        return interfaces
