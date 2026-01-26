from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

class DatetimeManager:
    '''Datetime manager helps calculate and get actual datetime, time data.'''

    def __init__(self) -> None: 
        self.new_year_num = datetime.now().year + 1
        self.is_time_format_pm = True
        self.time_zone = 0

    SEC_IN_HOUR = 3600 # seconds in 1 hour
    SEC_IN_MINUTE = 60 # seconds in 1 minute

    # time until new year dataclass(only read)
    @dataclass(frozen=True)
    class _TimeUntilNewYear:
        days: int # days left
        hours: int # hours left
        minutes: int # minutes left
        seconds: int # seconds left

    # ui style colorsheme dataclass(only read)
    @dataclass(frozen=True)
    class _StyleColorsheme:
        primary_color: str # primary
        secondary_color: str # secondary

    # datetime now dataclass(only read)
    @dataclass(frozen=True)
    class _DatetimeNow:
        time: str # time now
        date: str # date now
        month_name: str # month name now
        day_of_week: str # day of the week now

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
        '''
        returns a weekday name.

        Parameters
        ------------------
        weekday_index: week day index

        Returns
        ------------------
        day of week name str.
        '''

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
        '''
        returns a datetime now with specific time zone(utc).

        Returns
        -----------------
        datetime now.
        '''
        utc = timezone(timedelta(hours=self.time_zone))
        return datetime.now(utc)

    # set time format AM/PM
    def set_time_format(self, time_format: str) -> None:
        '''
        sets a time format AM/PM.

        Parameters
        ----------------
        time_format: time format str pattern
        '''
        if time_format == "pm": self.is_time_format_pm = True
        else: self.is_time_format_pm = False

    # set time zone
    def set_time_zone(self, num: int) -> None:
        '''
        sets time zone value.

        Parameters
        ----------------
        num: time zone num to set
        '''
        self.time_zone = num

    # get datetime data now
    def get_datetime_data_now(self) -> _DatetimeNow:
        '''
        returns a datetime now.

        Returns
        ----------------
        _DatetimeNow data.
        '''
        datetime_now = self.__get_datetime_now()
        time_format_pattern = "%H:%M:%S PM" if self.is_time_format_pm else "%I:%M:%S AM"
        time, date, weekday_index = "🕐" + datetime_now.time().strftime(time_format_pattern), "📆" + str(datetime_now.date()), datetime_now.weekday()
        weekday, month_name = self.__get_day_of_week_now(weekday_index), self.__get_current_month_name()
        return self._DatetimeNow(time=time, date=date, month_name=month_name, day_of_week=weekday)

    # get colorsheme by current time of year
    def get_colorsheme_of_current_time_of_year(self) -> _StyleColorsheme:
        '''
        returns a StyleColorsheme object.

        Returns
        ---------------
        _StyleColorsheme data.
        '''
        month_index = self.__get_datetime_now().month # current month index

        # (primary color, secondary color)
        # -primary color = for page background mainly
        # -secondary color = for other elements(borders, buttons...)
        if 1 <= month_index <= 2: return self._StyleColorsheme(primary_color="#03cffc", secondary_color="#02a9cf") # winter colors
        elif 3 <= month_index <= 5: return self._StyleColorsheme(primary_color="#03fca9", secondary_color="#02cf8a") # spring colors
        elif 6 <= month_index <= 8: return self._StyleColorsheme(primary_color="#6cff03", secondary_color="#58d102") # summer colors
        elif 9 <= month_index <= 11: return self._StyleColorsheme(primary_color="#ff8903", secondary_color="#db7704") # autumn colors
        else: return self._StyleColorsheme(primary_color="#73d5ff", secondary_color="#67bce0") # december month colors

    # get time until the new year (days, hours, minutes, seconds)
    def get_time_data_until_new_year(self) -> _TimeUntilNewYear:
        '''
        returns a TimeUntilNewYear object.

        Retuns
        ---------------
        _TimeUntilNewYear data.
        '''
        current_datetime = self.__get_datetime_now()
        destination_datetime = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc) # 01.01.new_year 00:00:00
        time_left = destination_datetime - current_datetime
        seconds = int(time_left.seconds) # get seconds
        days, hours, minutes = time_left.days, int(seconds / self.SEC_IN_HOUR), int(seconds / self.SEC_IN_MINUTE)
        return self._TimeUntilNewYear(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    # check is new year arrived
    def check_is_new_year_arrived(self) -> bool:
        '''checks whether New Year has arrived and returns bool state.'''
        current_year = self.__get_datetime_now().year # current year num now
        if current_year == self.new_year_num:
            self.new_year_num = current_year + 1 # updating, set new, new year num
            return True
        else: return False