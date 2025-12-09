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
from bottle import Bottle, template, response

PATH_TO_INDEX = "templates/index.html" # path to html index
PORT = 8000 # server port
HOST = "localhost" # hostname

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
        if month_index >= 1 and month_index <= 2: return ("#03cffc", "#02a9cf") # winter colors
        elif month_index >= 3 and month_index <= 5: return ("#03fca9", "#02cf8a") # spring colors
        elif month_index >= 6 and month_index <= 8: return ("#6cff03", "#58d102") # summer colors
        elif month_index >= 9 and month_index < 11: return ("#ff8903", "#db7704") # autumn colors
        elif month_index == 12: return ("#73d5ff", "#67bce0") # december month colors

    # getting current month name
    def get_current_month_name(self): 
        res_string = "" # output string

        datetime_now = datetime.now()
        month_index = datetime_now.month # current month index
        
        # adding to output string emoji by current month index
        if month_index >= 1 and month_index <= 2: res_string += "❄️" # winter
        elif month_index >= 3 and month_index <= 5: res_string += "🌸" # spring
        elif month_index >= 6 and month_index <= 8: res_string += "☀️" # summer
        elif month_index >= 9 and month_index < 11: res_string += "🍂" # autumn
        elif month_index == 12: res_string += "🎄" # (special) december month

        res_string += f"{datetime_now.strftime('%B')}" # adding formatted month name
        
        return res_string

    # calculating days count until the new year and days passed count in the currrent year
    def calculate_days_until_new_year(self): 
        current_datetime = datetime.now()
        destination_datetime = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0) # new year datetime

        days_left = (destination_datetime - current_datetime).days # days left to new year
        days_passed = self.get_days_count_in_year() - days_left # days passed in current year

        return (days_passed, days_left)
    
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

        return (hours, minutes, seconds)
    
app = Bottle() # bottle py object
datetime_manager = DatetimeManager()

@app.route("/") # creating index template
def index(): return template(PATH_TO_INDEX)

@app.route("/api/current_datetime_now")
def get_current_time():
    response.content_type = "application/json"
    # configuring current datetime data json
    return json.dumps(
        {
            "new_year": str(datetime_manager.get_new_year()),
            "datetime_now": f"{datetime_manager.get_time_now()}/{datetime_manager.get_date_now()}/{datetime_manager.get_current_month_name()}/{datetime_manager.get_day_of_week_now()}",
            "first_hex_color": datetime_manager.get_colorsheme_of_current_time_of_year()[0],
            "second_hex_color": datetime_manager.get_colorsheme_of_current_time_of_year()[1]
        }
    )

@app.route("/api/countdown_timer_until_new_year_data")
def get_countdown_timer_until_new_year_data():
    response.content_type = "application/json"
    # configuring countdown timer data json
    return json.dumps(
        {
            "hours_left": datetime_manager.get_time_data_until_new_year()[0],
            "minutes_left": datetime_manager.get_time_data_until_new_year()[1],
            "seconds_left": datetime_manager.get_time_data_until_new_year()[2]
        }
    )

@app.route("/api/datetime_stats_until_new_year")
def get_days_left_until_new_year():
    response.content_type = "application/json"
    # configuring datetime stats until new year data json
    return json.dumps(
        {
            "days_in_year_and_days_passed_difference": f"{datetime_manager.calculate_days_until_new_year()[0]}/{datetime_manager.get_days_count_in_year()}",
            "days_passed_in_current_year": datetime_manager.calculate_days_until_new_year()[0],
            "days_left_until_new_year": str(datetime_manager.calculate_days_until_new_year()[1]),
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