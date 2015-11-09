##
# This script is meant to monitor actual activity time on a computer. This means
# actual time typing and or moving the mouse. If an employee is trusted enough to be
# accurately only using the work computer for work, this is actual man hours expended.

import time
import sys
from datetime import datetime
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
  write_string = datetime.now().strftime("%c") #Build timestamp string in format 10/27/15 16:51:09. See datetime docs for help
  write_string += "," + "MouseActivity:{0:s}".format( str(mouse_active) )
  write_string += "," + "ActiveApp:{0:s}".format( str(app_name) )
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

def MonitorExceptionCatcher():
  try:
    MonitorActivity()
  except Exception as e:
    print("\n\nSaw exception: \n",e
    return True

def ExceptionMonitor(exception_count_threshold=None):
  exception_count = 0
  last_exception_time = None
  ##
  # MonitorExceptionCatcher returns True if it fails.
  # otherwise, it will run forever.
  # This loop wil continuously try to call main_function
  while(MonitorExceptionCatcher()):
    exception_count += 1
    last_exception_time = datetime.now()

    if exception_count_threshold and exception_count >= exception_count_threshold:
      print("Exceeded Exception Count Threshold")
      exception_count = 0

if __name__ == '__main__':

  exception_count = 0
  last_exception_time = None
  ##
  # main_function returns True if it fails.
  # otherwise, it will run forever.
  # This loop wil continuously try to call main_function
  while(main_function()):
    exception_count += 1
    last_exception_time = datetime.now()

