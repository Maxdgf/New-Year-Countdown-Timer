const body = document.body; // body

// countdown timer elements
const newYearView = document.getElementById("new_year_view");
const timeUntilNewYearView = document.getElementById("time_left_until_new_year_view");

// other elements
const currentTimeView = document.getElementById("current_time_view");
const nowDataFrame = document.getElementById("now_data_frame");
const settingsFrame = document.getElementById("settings_frame");
const otherDataFrame = document.getElementById("other_data_frame");

function loadCurrentDatetime() {
    fetch("/api/current_datetime_now")
        .then(response => response.json()) // get response as json
        .then(
            // process data
            data => {
                var month_name = data.month_name_now != null ? data.month_name_now : '?'; // month name
                var weekday = data.day_of_week != null ? data.day_of_week : '?'; // day of week

                currentTimeView.innerText = data.time_now + " / " +
                    data.date_now + " / " +
                    month_name + " / " +
                    weekday;
            }
        )
        .catch( exception => { console.error("Exception-[get current datetime now]: ", exception); } ); // print exception
}

function loadCurrentUiStyle() {
    fetch("/api/time_of_year_style")
        .then(response => response.json()) // get response as json
        .then(
            // process data
            data => {
                body.style.backgroundColor = data.primary_color != null ? data.primary_color : "blue"; // primary color

                var secondary = data.secondary_color != null ? data.secondary_color : "cyan"; // secondary color
                settingsFrame.style.borderColor = secondary;
                otherDataFrame.style.borderColor = secondary;
                nowDataFrame.style.borderColor = secondary;
            }
        )
        .catch(exception => { console.error("Exception-[get ui style data]: ", exception); }); // print exception
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
        .catch(exception => { console.error("Exception-[get countdown timer data]: ", exception); }); // print exception
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
        .catch(exception => { console.error("Exception-[get is new year arrived state]: ", exception); }); // print exception
}

// first launch
loadCurrentDatetime();
loadCountdownTimerData();
loadCurrentUiStyle();
loadIsNewYearArrivedState();

// periodic data fetch (1 second)
setInterval(loadCurrentDatetime, 1000);
setInterval(loadCountdownTimerData, 1000);
setInterval(loadCurrentUiStyle, 1000);
setInterval(loadIsNewYearArrivedState, 1000);
