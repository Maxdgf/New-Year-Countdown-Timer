const body = document.body; // body

// countdown timer elements
const newYearView = document.getElementById("new_year_view");
const timeUntilNewYearView = document.getElementById("time_left_until_new_year_view");

// other elements
const currentTimeView = document.getElementById("current_time_view");
const nowDataFrame = document.getElementById("now_data_frame");
const settingsFrame = document.getElementById("settings_frame");
const otherDataFrame = document.getElementById("other_data_frame");

var currentDateTimeId = null;
var countdownTimerDataId = null;
var currentUiStyleId = null;
var isNewYearArrivedStateId = null;

function loadCurrentDatetime() {
    fetch("/api/current_datetime_now")
        .then(response => response.json()) // get response as json
        .then(
            // process data
            data => { 
                currentTimeView.innerText = data.time_now + " / " +
                    data.date_now + " / " +
                    data.month_name_now + " / " +
                    data.day_of_week_now;
            }
        )
        .catch( exception => { console.error("Exception-[get current datetime now]: ", exception); } ); // exception
}

function loadCurrentUiStyle() {
    fetch("/api/time_of_year_style")
        .then(response => response.json()) // get response as json
        .then(
            // process data
            data => {
                body.style.backgroundColor = data.primary_color; // primary color

                // secondary color
                settingsFrame.style.borderColor = data.secondary_color;
                otherDataFrame.style.borderColor = data.secondary_color;
                nowDataFrame.style.borderColor = data.secondary_color;
            }
        )
        .catch(exception => { console.error("Exception-[get ui style data]: ", exception); }); // exception
}

function loadCountdownTimerData() {
    fetch("/api/countdown_timer_until_new_year_data")
        .then(response => response.json()) // get response as json
        .then(
            // process data
            data => {
                newYearView.innerText = data.new_year;
                timeUntilNewYearView.innerText = data.days_left + " d: " +
                    data.hours_left + " h: " +
                    data.minutes_left + " m: " +
                    data.seconds_left + " s";
            }
        )
        .catch(exception => { console.error("Exception-[get countdown timer data]: ", exception); }); // exception
}

function loadIsNewYearArrivedState() {
    fetch("/api/is_new_year_arrived_state")
        .then(response => response.json())
        .then(
            data => {
                var state = (data.is_new_year_arrived === "true"); // convert to bool

                if (state) {
                    alert("New year is arrived! 🎉");
                }
            }
        )
        .catch(exception => { console.error("Exception-[get is new year arrived state]: ", exception); });
}

// fisrt launch
loadCurrentDatetime();
loadCountdownTimerData();
loadCurrentUiStyle();
loadIsNewYearArrivedState();

// periodic data fetch (1 second)
currentDateTimeId = setInterval(loadCurrentDatetime, 1000);
countdownTimerDataId = setInterval(loadCountdownTimerData, 1000);
currentUiStyleId = setInterval(loadCurrentUiStyle, 1000);
isNewYearArrivedStateId = setInterval(loadIsNewYearArrivedState, 1000);