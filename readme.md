# Timebuddy

A simple python script to calculate time-related data based on a CSV input of a name followed by said persons availabilities. Developed for UMass Transit purposes, but can surve a larger majority for the same reason.

### Requirements

 * Python 3.5+
 * A CSV file with your data in it

### How to use

Download the python script and set up your CSV file (take a look at the `test.csv` file provided for an idea at your format. It should be a name followed by a series of comma-separated values with the format `MM/DD hh:mm-hh:mm` where it represents the date, start time on that date, then the end time on that date. Not intended for overnight usage.

Once you got all that set up, type `python time_counter_thing.py PATH_TO_CSV_HERE`. Make sure this is a `.csv` file or the program will not accept it.

You'll be then prompted with this UI if the file is parsed properly:

```py
    Possible Modes 
    1 - Search for availability at specific time
    2 - Search for availability over a specific day (all day)
    3 - Search for availability over a specific day (specified time frame)
    4 - Search for availability over a certain threshold
    s - Set a minimum (so it doesn't show results under X people, default 0)
```

* **1** - You will input a date and time and the program will output a list of people who are available at that time.
* **2** - Input a date and it will calculate all the availability on that day (in 15-min increments)
* **3** - Input a date and a start/end time (identical format to the one used in the CSV file). It will do the same as **2**, but on a specific time frame.
* **4** - Input a start date/time and an end date/time. Similar to **3**, but you can specify the date for both as well (so it can span multiple days)
* **s** - Specify the minimum number of people required at a time for the program to output it to the screen. This is especially useful in larger CSV files, where you may have a small number of people available at EVERY time. You'll want to set this higher if this is the case.

### Plans to add

A feature that you can specify the "first time when X people are available". Was one of my major initial intentions, but seemed a bit more complex than the ones I added first, so I put it off.
