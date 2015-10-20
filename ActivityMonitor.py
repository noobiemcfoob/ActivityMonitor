0##
# This script is meant to monitor actual activity time on a computer. This means
# actual time typing and or moving the mouse. If an employee is trusted enough to be
# accurately only using the work computer for work, this is actual man hours expended.

import time
from datetime import datetime
import matplotlib.pyplot as plt
import threading
import pythoncom
from win32gui import GetCursorPos
from win32api import GetKeyboardState
import pyHook, pythoncom
from time import sleep

mouse_active    = False
keyboard_active = False
log_time        = 0

def LogActivity():
  global mouse_active
  global keyboard_active
  global log_time
  if time.clock() >= log_time:
    print("\nLogging activity: MA: {0:s} | KA: {1:s}\n".format( str(mouse_active), str(keyboard_active) ))
    logFile = open("activity.am","a")
    write_string = str(datetime.now())
    write_string += "," + "MouseActivity:{0:s}".format( str(mouse_active) )
    write_string += "," + "KeyboardActivity:{0:s}".format( str(keyboard_active) )
    write_string += "\n"
    logFile.write(write_string)
    mouse_active    = False
    keyboard_active = False
    log_time = time.clock()+10

def OnMouseEvent(event):
  global mouse_active
  mouse_active = True
  LogActivity()

  print("In mouse event. Time: ", time.clock())

  # return True to pass the event to other handlers
  return True

def OnKeyboardEvent(event):
  global keyboard_active
  keyboard_active = True
  LogActivity()

  print("In keyboard event. Time: ", time.clock())

  # return True to pass the event to other handlers
  return True

def TimeoutEvent():
  while(1):
    sleep(10)
    print("In timeout event. Time: ", time.clock())
    LogActivity()

activity = list()

if __name__ == "__main__":
  threads = list()
  hm = pyHook.HookManager() # create a hook manager
  hm.MouseAll = OnMouseEvent # hook all mouse events to OnMouseEvent function above
  hm.HookMouse() # enable the hook
  hm.KeyDown = OnKeyboardEvent
  hm.HookKeyboard()
  print("Starting message pumper")
  threading.Thread(target=TimeoutEvent).start()

  while(1):
    last_clock = time.clock()
    print("Pump Cycle: ",count, "| Time: ", last_clock)
    while time.clock() < last_clock+5:
      pythoncom.PumpWaitingMessages()
    count += 1
    last_clock = time.clock()

