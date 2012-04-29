class SystemInfo:
    """
    Klasa ta jest kontenerem przechowujacym informacje o obciazeniu systemu.
    """
    
    def __init__(self):
        self.cpu      = {}
        self.disk     = {}
        self.ram      = {}

    def get_cpu(self):
        return self.cpu

    def get_disk(self):
        return self.disk

    def get_ram(self):
        return self.ram

    def set_cpu(self, x):
        self.cpu = x

    def set_disk(self, x):
        self.disk = x

    def set_ram(self, x):
        self.ram = x

if __name__ == "__main__":
    pass
