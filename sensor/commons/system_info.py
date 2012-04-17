class SystemInfo:
    """
    Klasa ta jest kontenerem przechowujacym informacje o obciazeniu systemu.
    """
    
    def __init__(self):
        self.cpu      = {}
        self.disk     = {}
        self.hostname = {}
        self.ram      = {}

    def get_cpu(self):
        return self.cpu

    def get_disk(self):
        return self.disk

    def get_hostname(self):
        return self.hostname

    def get_ram(self):
        return self.ram

    def set_cpu(self, x):
        self.cpu = x

    def set_disk(self, x):
        self.disk = x

    def set_hostname(self, x):
        self.hostname = s;

    def set_ram(self, x):
        self.ram = x

    #def get_str_info(self):
        #return str({"INFO" : [self.get_cpu(), self.get_ram(), self.get_disk()]}).replace('\'', '"')

if __name__ == "__main__":
    pass
