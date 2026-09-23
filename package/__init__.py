__version__ = '0.1'
__author__ = 'Thomas Tang'
__email__ = 'thomas.tang@evelyn.com'

print("Initializing package...")

# Import libraries
import os
import datetime
import calendar
from dateutil.relativedelta import relativedelta

print('===================================================================================================================')
print('Greetings Earthling. You are accessing the CCI data refresh module. Please check paths before continuing.')
print('===================================================================================================================')
print('Version: ' + __version__)
print('Author: ' + __author__)
print('Email: ' + __email__)
print('\n')

# Set out paths for folders
outputfolderpath = os.path.abspath(os.path.join(os.getcwd(), 'output'))

def get_last_day_of_month(date):
    # Get the number of days in the given month
    _, last_day = calendar.monthrange(date.year, date.month)
    # Replace the inputted date's day with the last day
    return date.replace(day=last_day)

refdate = get_last_day_of_month(datetime.datetime.today() - relativedelta(months=1))

# refdate = datetime.datetime.strptime("2026-02-28","%Y-%m-%d")

print('Output folder: ' + outputfolderpath)
print('Reference date: ' + refdate.strftime('%Y-%m-%d'))
print('===================================================================================================================\n')