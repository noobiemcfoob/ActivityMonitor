##
# This script is meant to monitor actual activity time on a computer. This means
# actual time typing and or moving the mouse. If an employee is trusted enough to be
# accurately only using the work computer for work, this is actual man hours expended.

import time
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import win32gui
import win32process
import win32api
from time import sleep
import wmi

c = wmi.WMI()

def get_app_name(hwnd):
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            break
    except:
        return None
    else:
        return exe

## Get list of all windows
windows = list()
def foreach_window(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        windows.append( hwnd )
    return True
#win32gui.EnumWindows(foreach_window, 0)

def LogMouseActivity(mouse_active, app_name):
  print("\nLogging Mouse Activity: MA: {0:s} in App: {1:s}\n".format( str(mouse_active), str(app_name) ) )
  logFile = open("mouse_activity.am","a")
  write_string = str(datetime.now())
  write_string += "," + "MouseActivity:{0:s}".format( str(mouse_active) )
  write_string += "," + "MouseApp:{0:s}".format( str(app_name) )
  write_string += "\n"
  logFile.write(write_string)

def MonitorActivity():
  while(1):
    mouse_pos = win32api.GetCursorPos()
    sleep(10)
    LogMouseActivity( 
      mouse_active = mouse_pos != win32api.GetCursorPos(), 
      app_name     = get_app_name( win32gui.GetForegroundWindow() )
    )

activity = list()

def main_function():
  MonitorActivity()

if __name__ == '__main__':
  main_function()
