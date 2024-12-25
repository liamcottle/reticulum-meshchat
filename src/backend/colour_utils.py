class ColourUtils:

    @staticmethod
    def hex_colour_to_byte_array(hex_colour):

        # remove leading "#"
        hex_colour = hex_colour.lstrip('#')

        # convert the remaining hex string to bytes
        return bytes.fromhex(hex_colour)
