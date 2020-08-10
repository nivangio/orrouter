

class HasAddress(object):
    def display_address(self):

        if "name" in self.address["properties"].keys():
            address_display = self.address["properties"]["name"]
        else:
            address_display = self.address["properties"]["street"] + " " + self.address["properties"]["housenumber"]

        return ", ".join([address_display, self.address["properties"].get("city",'')])
