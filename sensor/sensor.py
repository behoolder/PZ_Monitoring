#!/usr/bin/env python

import os

def get_sensor():
    """
    Importuje sensor w zaleznosci od systemu operacyjnego
    """
    if os.name == 'posix':
        from linux.linux import Linux
        sensor = Linux()
    elif os.name == 'nt':
        from windows.windows import Windows
        sensor = Windows()
    return sensor