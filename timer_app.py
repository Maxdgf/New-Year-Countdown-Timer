'''
Mini 🎄new year countdown timer web-app on bottle py.
======================================================================
-Displays today's 📆date (🕐time, 📆date, ☀️month, day of the week).
-The countdown to the new year in days-hours-minutes-seconds format.
'''

import json, os
from bottle import Bottle, template, response, request, static_file, redirect

from app_utils.datetime_manager import DatetimeManager

PATH_TO_INDEX = "templates/index.html" # path to html index
PORT, HOST = 8000, "localhost" # server port and hostname(for debug on local machine)
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) # project root path
    
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
    time_zone = request.forms.time_zone
    if time_zone: 
        datetime_manager.set_time_zone(num=int(time_zone))
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