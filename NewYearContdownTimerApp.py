'''
Mini 🎄new year countdown timer web-app on bottle py.
======================================================================
-Displays today's 📆date (🕐time, 📆date, ☀️month, day of the week).
-The countdown to the new year in days-hours-minutes-seconds format.
'''

import json, os
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from bottle import Bottle, template, response, request, static_file, redirect

PATH_TO_INDEX = "templates/index.html" # path to html index
PORT, HOST = 8000, "localhost" # server port and hostname(for debug on local machine)
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) # project root path

# time until new year dataclass
@dataclass(frozen=True)
class TimeUntilNewYear:
    days: int # days left
    hours: int # hours left
    minutes: int # minutes left
    seconds: int # seconds left

# ui style colorsheme dataclass
@dataclass(frozen=True)
class StyleColorsheme:
    primary_color: str # primary
    secondary_color: str # secondary

# datetime now dataclass
@dataclass(frozen=True)
class DatetimeNow:
    time: str # time now
    date: str # date now
    month_name: str # month name now
    day_of_week: str # day of the week now

class DatetimeManager:
    def __init__(self) -> None: 
        self.new_year_num = datetime.now().year + 1
        self.is_time_format_pm = True
        self.time_zone = 0

    SEC_IN_HOUR = 3600 # seconds in 1 hour
    SEC_IN_MINUTE = 60 # seconds in 1 minute

    # get current month name
    def __get_current_month_name(self) -> str: 
        '''returns a current month name.'''

        datetime_now = self.__get_datetime_now()
        month_index, month_name = datetime_now.month, datetime_now.strftime('%B') # month data
        
        # add to output string emoji by current month index
        if 1 <= month_index <= 2: return "❄️" + month_name # winter
        elif 3 <= month_index <= 5: return "🌸" + month_name # spring
        elif 6 <= month_index <= 8: return "☀️" + month_name # summer
        elif 9 <= month_index <= 11: return "🍂" + month_name # autumn
        else: return "🎄" + month_name # (special) december month
    # get week day (name)
    def __get_day_of_week_now(self, weekday_index: int) -> str: 
        '''returns a weekday name.'''

        # return week day name by index
        match weekday_index:
            case 0: return "Monday"
            case 1: return "Tuesday"
            case 2: return "Wednesday"
            case 3: return "Thursday"
            case 4: return "Friday"
            case 5: return "Saturday"
            case 6: return "Sunday"
    
    # get datetime now with specific time zone(utc)
    def __get_datetime_now(self) -> datetime:
        '''returns a datetime now with specific time zone(utc).'''
        utc = timezone(timedelta(hours=self.time_zone))
        return datetime.now(utc)

    # set time format AM/PM
    def set_time_format(self, time_format: str) -> None:
        '''sets a time format AM/PM.'''
        if time_format == "pm": self.is_time_format_pm = True
        else: self.is_time_format_pm = False

    # set time zone
    def set_gmt(self, num: int) -> None:
        '''sets time zone value.'''
        self.time_zone = num

    # get datetime data now
    def get_datetime_data_now(self) -> DatetimeNow:
        '''returns a datetime now.'''
        datetime_now = self.__get_datetime_now()
        time_format_pattern = "%H:%M:%S PM" if self.is_time_format_pm else "%I:%M:%S AM"
        time, date, weekday_index = "🕐" + datetime_now.time().strftime(time_format_pattern), "📆" + str(datetime_now.date()), datetime_now.weekday()
        weekday, month_name = self.__get_day_of_week_now(weekday_index), self.__get_current_month_name()
        return DatetimeNow(time=time, date=date, month_name=month_name, day_of_week=weekday)

    # get colorsheme by current time of year
    def get_colorsheme_of_current_time_of_year(self) -> StyleColorsheme:
        '''returns a StyleColorsheme dataclass object.'''
        month_index = self.__get_datetime_now().month # current month index

        # (primary color, secondary color)
        # -primary color = for page background mainly
        # -secondary color = for other elements(borders, buttons...)
        if 1 <= month_index <= 2: return StyleColorsheme(primary_color="#03cffc", secondary_color="#02a9cf") # winter colors
        elif 3 <= month_index <= 5: return StyleColorsheme(primary_color="#03fca9", secondary_color="#02cf8a") # spring colors
        elif 6 <= month_index <= 8: return StyleColorsheme(primary_color="#6cff03", secondary_color="#58d102") # summer colors
        elif 9 <= month_index <= 11: return StyleColorsheme(primary_color="#ff8903", secondary_color="#db7704") # autumn colors
        else: return StyleColorsheme(primary_color="#73d5ff", secondary_color="#67bce0") # december month colors

    # get time until the new year (days, hours, minutes, seconds)
    def get_time_data_until_new_year(self) -> TimeUntilNewYear:
        '''returns a TimeUntilNewYear dataclass object.'''
        current_datetime = self.__get_datetime_now()
        destination_datetime = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc) # 01.01.new_year 00:00:00
        time_left = destination_datetime - current_datetime
        seconds = int(time_left.total_seconds())
        days, hours, minutes = time_left.days, int(seconds / self.SEC_IN_HOUR), int(seconds / self.SEC_IN_MINUTE)
        return TimeUntilNewYear(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    # check is new year arrived
    def check_is_new_year_arrived(self) -> bool:
        '''checks whether New Year has arrived and returns bool state.'''
        current_year = self.__get_datetime_now().year # current year num now
        if current_year == self.new_year_num:
            self.new_year_num = current_year + 1 # updating, set new, new year num
            return True
        else: return False
    
app, datetime_manager = Bottle(), DatetimeManager() # bottle py object, datetime manager object

# create index template
@app.route("/")
def index(): return template(PATH_TO_INDEX)

# serve all static files
@app.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=os.path.join(PROJECT_ROOT, "static"))

@app.route("/set_time_format", method="POST")
def set_time_format(): 
    time_format = request.forms.time_format
    if time_format:
        datetime_manager.set_time_format(time_format=time_format)
    return redirect("/") # redirect to main page
    
@app.route("/set_time_zone", method="POST")
def set_gmt_factor():
    time_zone = request.forms.gmt_factor
    if time_zone: 
        datetime_manager.set_gmt(num=int(time_zone))
    return redirect("/") # redirect to main page

@app.route("/api/current_datetime_now")
def get_current_time():
    response.content_type = "application/json"
    datetime_now = datetime_manager.get_datetime_data_now()
    # configure current datetime data json
    return json.dumps(
        {
            "time_now": datetime_now.time,
            "date_now": datetime_now.date,
            "month_name_now": datetime_now.month_name,
            "day_of_week_now": datetime_now.day_of_week
        }
    )

@app.route("/api/time_of_year_style")
def get_time_of_year_style():
    response.content_type = "application/json"
    style_colorsheme = datetime_manager.get_colorsheme_of_current_time_of_year()
    # configure web app ui style data json
    return json.dumps(
        {
            "primary_color": style_colorsheme.primary_color,
            "secondary_color": style_colorsheme.secondary_color
        }
    )

@app.route("/api/countdown_timer_until_new_year_data")
def get_countdown_timer_until_new_year_data():
    response.content_type = "application/json"
    time_until_new_year = datetime_manager.get_time_data_until_new_year()
    # configure countdown timer data json
    return json.dumps(
        {
            "days_left": time_until_new_year.days,
            "hours_left": time_until_new_year.hours,
            "minutes_left": time_until_new_year.minutes,
            "seconds_left": time_until_new_year.seconds,
            "new_year": str(datetime_manager.new_year_num)
        }
    )

@app.route("/api/is_new_year_arrived_state")
def get_is_new_year_arrived_state():
    response.content_type = "application/json"
    # configure is new year arrived state json
    return json.dumps(
        { "is_new_year_arrived": str(datetime_manager.check_is_new_year_arrived()).lower() }
    )

if __name__ == "__main__": 
    app.run(host=HOST, port=PORT, debug=True, reloader=True) # launch app