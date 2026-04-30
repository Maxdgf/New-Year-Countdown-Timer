# Tests for datetime manager module
# - run test: pytest tests\datetime_manager_test.py

from utils.datetime_manager import DatetimeManager

datetime_manager = DatetimeManager() # init datetime manager object

def test_set_time_format():
    datetime_manager.set_time_format("am")
    assert datetime_manager.time_format == "am"

def test_set_time_zone():
    datetime_manager.set_time_zone(2)
    assert datetime_manager.time_zone == 2

def test_get_datetime_data_now():
    data = datetime_manager.get_datetime_data_now()

    assert data.month_name is not None
    assert data.day_of_week is not None

def test_get_color_scheme_of_current_time_of_year():
    color_scheme = datetime_manager.get_color_scheme_of_current_time_of_year()
    assert color_scheme is not None