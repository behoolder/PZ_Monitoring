#-*- coding: utf-8 -*-

from sensor.commons.system_info import SystemInfo
from commands import getoutput

class Linux:
    """
    Klasa ta zawiera szereg metod informujących o obciażeniu systemu.
    """

    def __init__(self):
        """
        Konstruktor klasy Linux.
        """

        self.data = SystemInfo()

    def ram_usage(self):
        """
        Zwraca informacje na temat całkowitej, użytej oraz wolnej ilości pamięci RAM.
        """

        output = getoutput("free").split()

        ram = {}

        ram["total"] = str(output[7])
        ram["used"] = str(output[8])
        ram["free"] = str(output[9])

        return {"RAM" : ram}

    def cpu_usage(self, n = 2, delay = 0.2):
        """
        Zwraca informacje na temat obciażenia CPU.\n

        n - liczba iteracji pomijanych zanim obciażenie CPU zostanie obliczone\n
        delay - opoźnienie pomiędzy iteracjami\n
        """

        if not isinstance(n, int) or not isinstance(delay, float):
            raise TypeError

        if n < 2:
            n = 2

        if delay < 0.0 :
            delay = 0.2

        output = getoutput("top -b -d " + str(delay) + " -n " + str(n))

        idx = -1
        for i in range(output.count("Cpu")) :
            idx = output.find("Cpu", idx + 1)

        output = output[idx:].split()

        cpu = {}
        cpu["user"] = output[1].split("%")[0]
        cpu["system"] = output[2].split("%")[0]

        return {"CPU" : cpu}

    def disk_space(self):
        """
        Zwraca informacje na temat dysku twardego.\n
        """

        output = getoutput("df -l").split("\n")

        disk = []
        for s in output[1:] :
            d = {}
            val = s.split()
            d["name"] = val[0]
            d["total"] = str(val[1])
            d["used"] = str(val[2])
            d["free"] = str(val[3])
            disk.append(d)

        return {"Hard drives" : disk}

    def metrics(self):
        """
        Zwraca metryki.\n
        """
        return {"hostname" : getoutput("hostname"), "cpu" : "1", "ram" : "1", "hdd" : "1"}

    def get_data(self):
        """
        Zwraca wszystkie informacje.\n
        """

        self.data.set_ram(self.ram_usage())
        self.data.set_cpu(self.cpu_usage())
        self.data.set_disk(self.disk_space())

        return self.data
