import os

class Sensor:
    
    def __init__(self):
        if os.name == 'posix':
            from linux.linux import Linux
            self.sensor = Linux()
        elif os.name == 'nt':
            from windows.windows import Windows
            self.sensor = Windows()
        else :
            self.sensor = None
    
    def get_sensor(self):
        return self.sensor