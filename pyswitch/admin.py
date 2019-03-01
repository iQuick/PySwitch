# -*- coding: utf-8 -*-


from __future__ import print_function
import os
import sys
import ctypes
if sys.version_info[0] == 3:
    import winreg as winreg
else:
    import _winreg as winreg

    

def is_admin():
    '''
    Checks if the script is running with administrative privileges.
    Returns True if is running as admin, False otherwise.
    '''    
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
