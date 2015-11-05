import time
import datetime
import matplotlib.pyplot as plt
import csv
import math
from embeddedShell import ipshell
from sys import stdout

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

  def __repr__(self):
    return "|| Activity {0:s} | {1:s} ||".format( str(self.timestamp), str(self.activity) )

class IntervalDataPoint(ActivityDataPoint):
  def __init__( 
    self,
    timestamp
  ):
    self.timestamp            = timestamp
    self.activity             = 0
    self.total_activity       = 0
    self.total_observations   = 0

  def AddObservation(self, observation):
    if not type(observation) is ActivityDataPoint: raise Exception("Expecting AcitivtyDataPoint for observation")

    self.total_activity += observation.activity
    self.total_observations += 1

    self.activity = self.total_activity / self.total_observations

def TimeFloor(time, minutes):
  return time - datetime.timedelta(minutes=time.minute%minutes, seconds=time.second)

def DisplayBinarySearchProgress(out_string):
  if out_string != DisplayBinarySearchProgress.out_string:
    print(out_string)
  else:
    stdout.write("\rReproduced: "+out_string)
    stdout.flush()

DisplayBinarySearchProgress.out_string = ""

def BinarySearch(test_value, data, imin=0, imax=None, debug=False):
  if imax is None:
    imax = len(data)-1

  index = imin + int( (imax - imin)/2 )

  output_string = ""
  if debug: 
    output_string = "\n\n(TV: %s) Index: %d - %s ||\nIMIN: %d - %s || IMAX: %d - %s"%(
                      test_value.strftime("%c"),
                      index,
                      data[index].strftime("%c"),
                      imin,
                      data[imin].strftime("%c"),
                      imax,
                      data[imax].strftime("%c")
                    )

  if test_value < data[index]:
    if debug: output_string += "\nValue lower than index. Moving upper end"
    DisplayBinarySearchProgress(output_string)
    if index == imax:
      return index
    index = BinarySearch(test_value, data, imin=imin, imax=index, debug=debug)
  elif test_value > data[index]:
    if debug: output_string += "\nValue greater than index. Moving lower end"
    DisplayBinarySearchProgress(output_string)
    if index == imin:
      return imin 
    index = BinarySearch(test_value, data, imin=index, imax=imax, debug=debug)
  else:
    if debug: output_string += "\nMatched value at index %d"%(index)
    DisplayBinarySearchProgress(output_string)
    
  return index

##
# Read a log, fill unobserved times with blank data, and average data into predefined intervals
# start_time    = Starting time to begin filling in data set
# time_interval = number of minutes for time window 
def BuildAveragedDataSet(start_time=None, end_time=None, time_interval=10, activities=None, debug=False):
  dataset = list()
  interval_delta = datetime.timedelta(minutes=time_interval)
  if start_time is None:
    start_time = TimeFloor(activities[0].timestamp, time_interval)

  if end_time is None:
    end_time = TimeFloor(activities[-1].timestamp, time_interval)

  if start_time > end_time:
    raise Exception("BuildDataSet || Start time is after End Time")

  num_intervals = math.ceil( (end_time-start_time).total_seconds()/(60*time_interval) )
  # Build a num_intervals long list containing ActivityDataPoint at correct timestamp (empty)
  interval_time = start_time
  for interval in range(0,num_intervals):
    dataset.append( IntervalDataPoint(interval_time) )
    interval_time += interval_delta

  print("BuildDataSet || Number of bins defined: ", len(dataset), "from", dataset[0].timestamp, "to", dataset[-1].timestamp)

  # Build a list of just the timestamps
  interval_timestamps = [data.timestamp for data in dataset]

  def DisplayObservationNumber(number):
    stdout.write("\rOn Observation %d of %d"%(number, len(activities)-1))
    stdout.flush()

  # Cycle through all activities and sort into interval bins
  for index,activity in enumerate(activities):
    DisplayObservationNumber(index)
    # Floor the timestamp of the acivity to within the time_interval
    activity_timefloor = TimeFloor(activity.timestamp, time_interval)
    # Check that activity is in desired time window
    if activity_timefloor < start_time or activity_timefloor > end_time:
      continue

    # Determine which bin to put the observation
    # print("Searching for time bin for {0:s}".format( str(activity) ))
    activity_bin_index = BinarySearch(activity_timefloor, interval_timestamps, debug=True)

    try:
      print( "\nFound bin for {0:s} at index {1:d}".format( str(activity), activity_bin_index ) )
      print( "Time Bin: {0:s}".format( str(dataset[activity_bin_index]) ) )
      dataset[activity_bin_index].AddObservation( activity )
    except Exception as e:
      print("\n\nFailed to add {0:s} at index: {1:d}".format( str(activity), activity_bin_index ))
      raise e

  return dataset


if __name__ == '__main__':
  print("Running ReadLog")
  ReadLog()
  ipshell()

