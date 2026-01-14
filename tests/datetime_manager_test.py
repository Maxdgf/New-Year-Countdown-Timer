r'''
Tests for datetime manager module
---------------------------------------------------
for run test: pytest tests\datetime_manager_test.py
'''

from app_utils.datetime_manager import DatetimeManager

datetime_manager = DatetimeManager()

def test_set_time_format():
    datetime_manager.set_time_format("pm")

def test_set_time_zone():
    datetime_manager.set_time_zone(2)

def test_get_datetime_data_now():
    assert datetime_manager.get_datetime_data_now() is not None

def test_get_colorsheme_of_current_time_of_year():
    assert datetime_manager.get_colorsheme_of_current_time_of_year() is not None

def test_get_time_data_until_new_year():
    assert datetime_manager.get_time_data_until_new_year() is not None