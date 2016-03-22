import sys, csv, time, re
import datetime
from collections import defaultdict

class Employee:
  def __init__(self, name, times):
    self.name = name
    self.times = times

  def is_available_at(self, when):
    for time in self.times:
      if time[0] <= when <= time[1]:
        return True
    return False

def main(lines):
  MINIMUM = 1
  if len(lines)==0:
    raise ValueError('Input was empty')

  employees = {}
  for person in lines:
    times = list(map(lambda t: strings_to_time(t), [split_time_string(s) for s in lines[person]]))
    employees[person] = Employee(person, times)

  display_modes()
  s = input('Please select a mode: ').strip()
  print()

  if s == 's':
    s = input('Set your minimum: ').strip()
    try:
      MINIMUM = int(s)
    except Exception as e:
      print('That was not an integer. Defaulting to 1.')

  s = input('Please select a mode: ').strip()
  print()

  """ Search for available at a specific time """
  if s == '1':
    while True:
      try:
        s = input('What time would you like to search for? ').strip()
        timing = string_to_time(s)
        break
      except Exception as e:
        print('Invalid format, required: MM/DD hh:mm (in military time)\n')

    for e in employees:
      if employees[e].is_available_at(timing):
        print('{} is'.format(e))
      else:
        print('{} is not'.format(e))


  """ Search for availability over a specific day (all day) """
  if s == '2':
    while True:
      try:
        day = input("What is the day you want to check? (format: MM/DD) ").strip()
        string_to_time('{} 11:11'.format(day))
        break
      except Exception as e:
        print('Invalid format, required: MM/DD hh:mm (in military time)\n')

    time_dic = defaultdict(list)
    for i in range(0, 24*60, 15):

      time_to_check = '{}:{}'.format(int(i/60), str(i%60).zfill(2))
      date_form = string_to_time('{} {}'.format(day, time_to_check))

      for e in employees:
        if employees[e].is_available_at(date_form):
          time_dic[time_to_check].append(e)
    
    for name,value in sorted(time_dic.items(), key=lambda x: time.strptime(x[0], '%H:%M')):
      if len(value) >= MINIMUM:
        print('{} : {}'.format(name, ', '.join(value))) 


  """ Search for availability over a specific day (specified time frame) """
  if s == '3':
    while True:
      try:
        date_input = input("Please specify the time frame (format: MM/DD hh:mm-hh:mm) ").strip()
        day = date_input.split()[0]
        times = split_time_string(date_input)
        date_form = list(map(lambda t: string_to_time(t), times))
        break
      except Exception as e:
        print('Invalid format, required: MM/DD hh:mm (in military time)\n')

    time_dic = defaultdict(list)
    for i in range(date_form[0].tm_hour * 60 + date_form[0].tm_min, date_form[1].tm_hour * 60 + date_form[1].tm_min, 15):

      time_to_check = '{}:{}'.format(int(i/60), str(i%60).zfill(2))
      date_form = string_to_time('{} {}'.format(day, time_to_check))

      for e in employees:
        if employees[e].is_available_at(date_form):
          time_dic[time_to_check].append(e)

    for name,value in sorted(time_dic.items(), key=lambda x: time.strptime(x[0], '%H:%M')):
      if len(value) >= MINIMUM:
        print('{} : {}'.format(name, ', '.join(value))) 

  """ Search for availability over a certain threshold """
  if s == '4':
    while True:
      try:
        date1 = input("Please specify the start date (format: MM/DD hh:mm) ").strip()
        start_date = datetime.datetime(*string_to_time(date1)[:6])

        date2 = input("Please specify the end date (format: MM/DD hh:mm) ").strip()
        end_date = datetime.datetime(*string_to_time(date2)[:6])
        break
      except Exception as e:
        print('Invalid format, required: MM/DD hh:mm (in military time)\n')
        raise e

    time_dic = defaultdict(list)
    count = 0
    modified_date = start_date
    while modified_date < end_date:
      time_to_check = '{}/{} {}:{}'.format(modified_date.month, modified_date.day, modified_date.hour, str(modified_date.minute).zfill(2))
      date_form = string_to_time(time_to_check)

      for e in employees:
        if employees[e].is_available_at(date_form):
          time_dic[time_to_check].append(e)

      modified_date += datetime.timedelta(0, 15 * 60)
    for name,value in sorted(time_dic.items(), key=lambda x: time.strptime(x[0], '%m/%d %H:%M')):
      if len(value) >= MINIMUM:
        print('{} : {}'.format(name, ', '.join(value))) 

  
def split_time_string(ts):
  split_str = ts.split()
  times = split_str[1].split('-')
  return list(map(lambda s: "{} {}".format(split_str[0], s), times))

def strings_to_time(times):
  return list(map(lambda t: time.strptime(t, "%m/%d %H:%M"), times))

def string_to_time(t):
  return time.strptime(t, "%m/%d %H:%M")

def display_modes():
  msg = """\
        -- Possible Modes --
        1 - Search for availability at specific time
        2 - Search for availability over a specific day (all day)
        3 - Search for availability over a specific day (specified time frame)
        4 - Search for availability over a certain threshold 
        s - Set a minimum (so it doesn't show results under X people, default 0)
        """
  print(msg)


if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please supply a CSV file path in quotations (like this: \"data/file.csv\")')

  elif sys.argv[1][-4:] != '.csv':
    print('Please supply a CSV file! (given: \'{}\')'.format(sys.argv[1][-4:]))

  else:
    try:
      with open(sys.argv[1], 'r') as fp:
        dic = {}
        for row in csv.reader(fp):
          dic[row[0]] = row[1:]
        main(dic)
    except IOError as e:
      print('Invalid filepath provided (given: \'{}\')'.format(sys.argv[1]))
    except Exception as e:
      print('Something went wrong during the loading of your file')
      print('{}: {}'.format(type(e).__name__, e))