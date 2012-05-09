#-*- coding: utf-8 -*-

class SystemInfo:
    """
    Klasa jest kontenerem przechowującym informacje o obciążeniu systemu.
    """
    
    def __init__(self):
        """
        Konstruktor klasy SystemInfo.
        """
        self.cpu      = {}
        self.disk     = {}
        self.ram      = {}

    def get_cpu(self):
        """
        Metoda pobiera informacje o CPU.
        """
        return self.cpu

    def get_disk(self):
        """
        Metoda pobiera informacje o HDD.
        """
        return self.disk

    def get_ram(self):
        """
        Metoda pobiera informacje o RAM.
        """
        return self.ram

    def set_cpu(self, x):
        """
        Metoda zapisuje informacje o CPU.\n
        
        x - informecje o CPU.\n
        """
        self.cpu = x

    def set_disk(self, x):
        """
        Metoda zapisuje informacje o HDD.\n
        
        x - informecje o HDD.\n
        """
        self.disk = x

    def set_ram(self, x):
        """
        Metoda zapisuje informacje o RAM.\n
        
        x - informecje o RAM.\n
        """
        self.ram = x

if __name__ == "__main__":
    pass
