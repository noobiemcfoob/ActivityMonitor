##
# This script is meant to monitor actual activity time on a computer. This means
# actual time typing and or moving the mouse. If an employee is trusted enough to be
# accurately only using the work computer for work, this is actual man hours expended.

import time
import datetime

def DetermineIfActive():
  return True

##
# Pair observed activity with datetime to build observation
def ObserveActivity():
  observation = ( datetime.now(), DetermineIfActive() )
  return observation

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
    observation = ObserveActivity()
    print( "Observed: ", observation )
    observed.append( observation )
    print( "Sleeping for {0:d} seconds".format(monitor_delay) )
    time_monitored += monitor_delay
    time.delay( monitor_delay )

  print("Monitored {0:d} seconds. Saw {1:d} obseverations", time_monitored, observed.size() )
  return observed

if __name__ == "__main__":
  minutes_to_monitor = 1
  print("Monitoring for {0:d} minutes", minutes_to_monitor)

  MonitorActivity( minutes_to_monitor*60 )

