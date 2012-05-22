#-*- coding: utf-8 -*-

from sensor.commons.system_info import SystemInfo
from wmi import WMI
from os import getenv

class Windows:
    """
    Klasa ta zawiera szereg metod informujących o obciążeniu systemu.
    """

    def __init__(self):
        """
        Konstruktor klasy Windows.
        """
        self.data = SystemInfo()

    def cpu_usage(self):
        """
        Zwraca informacje na temat obciążenia CPU.
        """
        cpu = {}

        cpu["system"] = str(WMI().Win32_Processor()[0].LoadPercentage)

        return {"CPU" : cpu}

    def disk_space(self):
        """
        Zwraca informacje na temat dysku twardego.
        """
        myWMI = WMI()

        diskList = []

        for disk in myWMI.Win32_LogicalDisk(DriveType=3):
            d = {}

            d["name"]  = str(disk.Caption)
            d["total"] = str(disk.Size)
            d["free"]  = str(disk.FreeSpace)
            d["used"]  = str(int(disk.Size) - int(disk.FreeSpace))

            diskList.append(d)

        return {"Hard drives" : diskList}

    def get_data(self):
        """
        Zwraca wszystkie informacje.
        """
        self.data.set_ram(self.ram_usage())
        self.data.set_cpu(self.cpu_usage())
        self.data.set_disk(self.disk_space())

        return self.data

    def metrics(self):
        """
        Zwraca metryki.
        """
        return {"hostname" : getenv("COMPUTERNAME"), "cpu" : "1", "ram" : "1", "hdd" : "1"}

    def ram_usage(self):
        """
        Zwraca informacje na temat całkowitej, użytej oraz wolnej ilości pamięci RAM.
        """
        myWMI = WMI()

        ram = {}

        ram["total"] = str(myWMI.Win32_ComputerSystem()[0].TotalPhysicalMemory)
        ram["free"]  = str(myWMI.Win32_OperatingSystem()[0].FreePhysicalMemory * 1024)
        ram["used"]  = str(int(myWMI.Win32_ComputerSystem()[0].TotalPhysicalMemory) - int(myWMI.Win32_OperatingSystem()[0].FreePhysicalMemory) * 1024)

        return {"RAM" : ram}