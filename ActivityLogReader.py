import time
import datetime
import matplotlib.pyplot as plt
import csv
import math
from embeddedShell import ipshell

activity_readings = list()

minute = datetime.timedelta(minutes=1)

def ReadLog(filename="mouse_activity.am"):
  with open(filename, 'r') as activity_log:
    reader = csv.reader(activity_log) #iterator for each row of activity_log
    for activity in reader:
      timestamp       = datetime.datetime.strptime(activity[0], "%c") # Process date string of format 10/27/15 16:51:09. See datetime docs for help
      mouse_activity  = activity[1].split(':')[-1] == 'True'
      active_app      = activity[2].split(':')[-1]

      activity_readings.append( ActivityDataPoint( timestamp, mouse_activity, active_app ) )

class ActivityDataPoint(object):
  def __init__( 
    self,
    timestamp,
    activity,
    active_app
  ):
    self.timestamp    = timestamp
    self.activity     = activity
    self.active_app   = active_app

def TimeFloor(time, minutes):
  return time - datetime.timedelta(minutes=time.minutes%minutes, seconds=now.second)

##
# Read a log and fill unobserved times with blank data
# start_time    = Starting time to begin filling in data set
# time_interval = number of minutes for time window 
def BuildDataSet(start_time=None, end_time=None, time_interval=10, activities=None):
  dataset = list()
  interval_delta = datetime.delta(minutes=time_interval)
  if start_time is None:
    start_time = TimeFloor(activities[0].timestamp, time_interval)

  if end_time is None:
    end_time = TimeFloor(activities[-1].timestamp, time_interval)

  if start_time > end_time:
    raise Exception("BuildDataSet || Start time is after End Time")

  num_intervals = math.ceil( (end_time-start_time).total_seconds()/60 )
  interval_time = start_time
  current_activities = list()
  for activity in activities:
    activity_timefloor = TimeFloor(activity.timestamp, time_interval) 
    # Pad dataset with empty interval windows
    while activity_timefloor > interval_time:
      dataset.append( ActivityDataPoint( interval_time, False, None ), () )
      interval_time += interval_delta

    if activity_timefloor != interval_time:
      raise Exception("Something went really wrong...")

    #Check data set time. If Time is not in window (ahead), fill with zeros


if __name__ == '__main__':
  print("Running ReadLog")
  ReadLog()
  ipshell()


