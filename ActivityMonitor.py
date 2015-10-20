##
# This script is meant to monitor actual activity time on a computer. This means
# actual time typing and or moving the mouse. If an employee is trusted enough to be
# accurately only using the work computer for work, this is actual man hours expended.

import time
from datetime import datetime
import matplotlib.pyplot as plt
import _thread
import pythoncom
from win32gui import GetCursorPos
from win32api import GetKeyboardState
import pyHook, pythoncom

def OnMouseEvent(event):
  # called when mouse events are received
  print('MessageName:',event.MessageName)
  print('Message:',event.Message)
  print('Time:',event.Time)
  print('Window:',event.Window)
  print('WindowName:',event.WindowName)
  print('Position:',event.Position)
  print('Wheel:',event.Wheel)
  print('Injected:',event.Injected)
  print('---')

  # return True to pass the event to other handlers
  return True

def OnKeyboardEvent(event):
  print('MessageName:',event.MessageName)
  print('Message:',event.Message)
  print('Time:',event.Time)
  print('Window:',event.Window)
  print('WindowName:',event.WindowName)
  print('Ascii:', event.Ascii, chr(event.Ascii))
  print('Key:', event.Key)
  print('KeyID:', event.KeyID)
  print('ScanCode:', event.ScanCode)
  print('Extended:', event.Extended)
  print('Injected:', event.Injected)
  print('Alt', event.Alt)
  print('Transition', event.Transition)
  print('---')

  # return True to pass the event to other handlers
  return True

class Observation(object):
  def __init__(self):
    self.mouse_activity = False

  def ReportMouseActivity(self, observation_delay):
    initialMousePos = GetCursorPos()
    time.sleep(observation_delay)
    values = GetKeyboardState()
    summed = 0
    for value in values:
      summed += not (value == 0 or value == 1)
    print(summed)
    if initialMousePos != GetCursorPos():
      print("Saw Initial:", initialMousePos, " And last:", GetCursorPos() )
      self.mouse_activity = True
    else:
      print("Same pos: ", initialMousePos)

  def Observe(self, observation_delay):
    self.ReportMouseActivity(observation_delay)
    #_thread.start_new_thread( ReportMouseActivity, tuple([observation_delay]) )

    return self.mouse_activity

##
# Pair observed activity with datetime to build observation
def BuildActivityObservation(observation_delay): 
  current_observation = Observation()
  
  return current_observation.Observe(observation_delay)

##
# Monitor use for a period of monitor_time (seconds) at intervals of monitor_delay (seconds)
def MonitorActivity( monitor_time, monitor_delay=5 ):
  observed = list()
  # Take first observation
  print( "Saw clock time of", time.clock() )
  first_time = time.clock()
  time_monitored = 0
  while( time.clock() <= first_time + monitor_time ):
    print( "Monitored {0:d} seconds".format(time_monitored) )
    observation = BuildActivityObservation(monitor_delay)
    print( "Observed: ", observation )
    observed.append( observation )
    print( "Sleeping for {0:d} seconds\n ".format(monitor_delay) )
    time_monitored += monitor_delay

  print("Monitored {0:d} seconds. Saw {1:d} obseverations".format( time_monitored, len( observed ) ) )
  return observed

##
# Plot sum of observed activity over time
def PlotObservedSum( observations ):
  plt.figure(0)

  summed_obvservations = list()
  summed_obvservations.append(0)
  for observation in observations:
    summed_obvservations.append(observation + summed_obvservations[-1])

  plt.plot(summed_obvservations, label="Summed Observations")
  plt.gca().set_title("Total Observed Activity over Time")
  plt.gca().set_ylabel("Total Observed Activity")
  plt.gca().set_xlabel("Time")

  plt.show()


if __name__ == "__main__":
  hm = pyHook.HookManager() # create a hook manager
  hm.MouseAll = OnMouseEvent # hook all mouse events to OnMouseEvent function above
  hm.HookMouse() # enable the hook
  hm.KeyDown = OnKeyboardEvent
  hm.HookKeyboard()
  print("Starting message pumper")
  _thread.start_new_thread( pythoncom.PumpMessages() ) # start a wait forever thread
  print("Messages pumping")

  minutes_to_monitor = 1 
  assert(minutes_to_monitor > 0)
  print("Monitoring for {0:d} minutes".format( minutes_to_monitor ) )

  observations = MonitorActivity( minutes_to_monitor*60 )
  PlotObservedSum( [activity for (x, activity) in observations] )

