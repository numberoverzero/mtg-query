class SynergyHashNotFoundException(Exception):
    def __init__(self, hash):
        self.hash = hash

    @property
    def msg(self):
        return "Could not find the hash \"{}\"".format(self.hash)
