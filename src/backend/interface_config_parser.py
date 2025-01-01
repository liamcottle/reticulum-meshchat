class InterfaceConfigParser:

    @staticmethod
    def parse(text):

        # process config
        interfaces = []
        current_interface = None
        for line in text.splitlines():

            # strip whitespace from either side of string
            line = line.strip()

            # skip empty lines and commented out lines
            if not line or line.startswith("#"):
                continue

            # check if we found a line containing an interface name
            if line.startswith("[[") and line.endswith("]]"):

                # we found a new interface, so add the previously parsed one to the interfaces list
                if current_interface:
                    interfaces.append(current_interface)

                # get interface name by removing the "[[" and "]]"
                interface_name = line[2:-2]
                current_interface = {
                    "name": interface_name,
                }

            # we found a key=value line, so we will set these values on the interface
            elif current_interface is not None and "=" in line:

                # parse key and value
                line_parts = line.split("=", 1)
                key = line_parts[0].strip()
                value = line_parts[1].strip().strip('"').strip("'")

                # skip empty values or values equal to "None"
                if value is None or value == "None":
                    continue

                # set key/value on interface
                current_interface[key] = value

        # add the final interface to the list
        if current_interface:
            interfaces.append(current_interface)

        return interfaces
