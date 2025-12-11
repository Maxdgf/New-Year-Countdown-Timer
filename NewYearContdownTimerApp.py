'''
Mini 🎄new year countdown timer web-app on bottle py.
======================================================================
-Displays today's 📆date (🕐time, 📆date, ☀️month, day of the week).
-The countdown to the new year in hours-minutes-seconds, 
    how many 🌄days have passed in the current year 
    and how many are 🕯️left until the new year.
'''

import json, calendar
from datetime import datetime
from dataclasses import dataclass
from bottle import Bottle, template, response

PATH_TO_INDEX = "templates/index.html" # path to html index
PORT = 8000 # server port
HOST = "localhost" # hostname

@dataclass
class TimeUntilNewYear:
    hours: int
    minutes: int
    seconds: int

@dataclass
class StyleColorsheme:
    primary_color: str
    secondary_color: str

@dataclass
class DaysOfYearData:
    days_passed_count: int
    days_left_count: int

class DatetimeManager:
    def __init__(self): pass

    SECONDS_IN_HOUR = 3600 # seconds in 1 hour
    SECONDS_IN_MINUTE = 60 # seconds in 1 minute

    def __is_leap(self): calendar.isleap(datetime.now().year) # checking if a year is a leap year

    def get_time_now(self, pattern: str = '%H:%M:%S'): return f"🕐{datetime.now().time().strftime(pattern)}" # getting current formatted time
    def get_date_now(self): return f"📆{datetime.now().date()}" # getting current date
    def get_new_year(self): return datetime.now().year + 1 # getting new year num (current year num + 1)
    # getting week day (name)
    def get_day_of_week_now(self): 
        weekday_index = datetime.now().weekday() # getting week day index

        # returning week day name by index
        match weekday_index:
            case 0: return "Monday"
            case 1: return "Tuesday"
            case 2: return "Wednesday"
            case 3: return "Thursday"
            case 4: return "Friday"
            case 5: return "Saturday"
            case 6: return "Sunday"

    # getting colorsheme by current time of year
    def get_colorsheme_of_current_time_of_year(self):
        datetime_now = datetime.now()
        month_index = datetime_now.month # current month index

        # (primary color, secondary color)
        # -primary color = for page background mainly
        # -secondary color = for other elements(borders, buttons...)
        if month_index >= 1 and month_index <= 2: return StyleColorsheme(primary_color="#03cffc", secondary_color="#02a9cf") # winter colors
        elif month_index >= 3 and month_index <= 5: return StyleColorsheme(primary_color="#03fca9", secondary_color="#02cf8a") # spring colors
        elif month_index >= 6 and month_index <= 8: return StyleColorsheme(primary_color="#6cff03", secondary_color="#58d102") # summer colors
        elif month_index >= 9 and month_index < 11: return StyleColorsheme(primary_color="#ff8903", secondary_color="#db7704") # autumn colors
        elif month_index == 12: return StyleColorsheme(primary_color="#73d5ff", secondary_color="#67bce0") # december month colors

    # getting current month name
    def get_current_month_name(self): 
        datetime_now = datetime.now()
        month_index = datetime_now.month # current month index
        month_name = datetime_now.strftime('%B')
        
        # adding to output string emoji by current month index
        if month_index >= 1 and month_index <= 2: return "❄️" + month_name # winter
        elif month_index >= 3 and month_index <= 5: return "🌸" + month_name # spring
        elif month_index >= 6 and month_index <= 8: return "☀️" + month_name # summer
        elif month_index >= 9 and month_index < 11: return "🍂" + month_name # autumn
        elif month_index == 12: return "🎄" + month_name # (special) december month

    # calculating days count until the new year and days passed count in the currrent year
    def calculate_days_data_until_new_year(self): 
        current_datetime = datetime.now()
        destination_datetime = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0) # new year datetime

        days_left = (destination_datetime - current_datetime).days # days left to new year
        days_passed = self.get_days_count_in_year() - days_left # days passed in current year

        return DaysOfYearData(
            days_passed_count=days_passed, 
            days_left_count=days_left
        )
    
    # getting days count in current year
    def get_days_count_in_year(self): 
        # with leap check
        if self.__is_leap(): return 366
        else: return 365

    # getting time until the new year (hours, minutes, seconds)
    def get_time_data_until_new_year(self):
        current_datetime = datetime.now()
        destination_datetime = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0) # new year datetime
        time_left = destination_datetime - current_datetime

        seconds = int(time_left.total_seconds()) # seconds left
        hours = int(seconds / self.SECONDS_IN_HOUR) # hours left
        minutes = int(seconds / self.SECONDS_IN_MINUTE) # minutes left

        return TimeUntilNewYear(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
    
app = Bottle() # bottle py object
datetime_manager = DatetimeManager()

@app.route("/") # creating index template
def index(): return template(PATH_TO_INDEX)

@app.route("/api/current_datetime_now")
def get_current_time():
    response.content_type = "application/json"
    style_colorsheme = datetime_manager.get_colorsheme_of_current_time_of_year()
    # configuring current datetime data json
    return json.dumps(
        {
            "new_year": str(datetime_manager.get_new_year()),
            "datetime_now": f"{datetime_manager.get_time_now()}/{datetime_manager.get_date_now()}/{datetime_manager.get_current_month_name()}/{datetime_manager.get_day_of_week_now()}",
            "first_hex_color": style_colorsheme.primary_color,
            "second_hex_color": style_colorsheme.secondary_color
        }
    )

@app.route("/api/countdown_timer_until_new_year_data")
def get_countdown_timer_until_new_year_data():
    response.content_type = "application/json"
    time_until_new_year = datetime_manager.get_time_data_until_new_year()
    # configuring countdown timer data json
    return json.dumps(
        {
            "hours_left": time_until_new_year.hours,
            "minutes_left": time_until_new_year.minutes,
            "seconds_left": time_until_new_year.seconds
        }
    )

@app.route("/api/datetime_stats_until_new_year")
def get_days_left_until_new_year():
    response.content_type = "application/json"
    days_data = datetime_manager.calculate_days_data_until_new_year()
    # configuring datetime stats until new year data json
    return json.dumps(
        {
            "days_in_year_and_days_passed_difference": f"{days_data.days_passed_count}/{datetime_manager.get_days_count_in_year()}",
            "days_passed_in_current_year": days_data.days_passed_count,
            "days_left_until_new_year": str(days_data.days_left_count),
            "days_count_in_current_year": datetime_manager.get_days_count_in_year()
        }
    )

if __name__ == "__main__":
    # launching web app
    app.run(
        host=HOST,
        port=PORT,
        debug=True, # debug
        reloader=True # auto-reloading
    ) 