from dataclasses import dataclass
from datetime import datetime, timezone, timedelta


class DatetimeManager:
    """Datetime manager helps calculate and get actual datetime, time data."""

    def __init__(self) -> None:
        self.new_year_num = datetime.now().year + 1 # new year num
        self.time_format = "pm"                     # current time format mode
        self.time_zone = 0                          # current time zone num

    SEC_IN_HOUR = 3600  # seconds in 1 hour
    SEC_IN_MINUTE = 60  # seconds in 1 minute

    # time until new year dataclass(read-only)
    @dataclass(frozen=True)
    class _TimeUntilNewYear:
        days: int     # days left
        hours: int    # hours left
        minutes: int  # minutes left
        seconds: int  # seconds left

    # ui style color scheme dataclass(read-only)
    @dataclass(frozen=True)
    class _StyleColorScheme:
        primary_color: str    # primary
        secondary_color: str  # secondary

    # datetime now dataclass(read-only)
    @dataclass(frozen=True)
    class _DatetimeNow:
        time: str          # time now
        date: str          # date now
        month_name: str    # month name now
        day_of_week: str   # day of the week now

    # get current month name
    def __get_current_month_name(self) -> str | None:
        """
        Returns a current month name.

        Returns
        --------------
        Month name str.
        """

        datetime_now = self.__get_datetime_now()
        month_index, month_name = datetime_now.month, datetime_now.strftime('%B')  # month data

        # add to output string emoji by current month index
        if 1 <= month_index <= 2:
            return "❄️" + month_name  # winter
        elif 3 <= month_index <= 5:
            return "🌸" + month_name  # spring
        elif 6 <= month_index <= 8:
            return "☀️" + month_name  # summer
        elif 9 <= month_index <= 11:
            return "🍂" + month_name  # autumn
        elif month_index == 12:
            return "🎄" + month_name  # december month
        else:
            return None

    @staticmethod
    def __get_day_of_week_now(weekday_index: int) -> str | None:
        """
        Returns a weekday name.

        Parameters
        ------------------
        weekday_index: week day index

        Returns
        ------------------
        Day of week name str.
        """

        # return week day name by index
        match weekday_index:
            case 0:
                return "Monday"
            case 1:
                return "Tuesday"
            case 2:
                return "Wednesday"
            case 3:
                return "Thursday"
            case 4:
                return "Friday"
            case 5:
                return "Saturday"
            case 6:
                return "Sunday"
            case _:
                return None

    def __get_datetime_now(self) -> datetime:
        """
        Returns a datetime now with specific time zone(utc).

        Returns
        -----------------
        datetime now.
        """

        utc = timezone(timedelta(hours=self.time_zone))
        return datetime.now(utc)

    def set_time_format(self, time_format: str) -> None:
        """
        Sets a time format AM/PM.

        Parameters
        ----------------
        time_format: time format str pattern
        """

        tf = time_format.lower()  # convert time format to lowercase
        self.time_format = tf

    def set_time_zone(self, num: int) -> None:
        """
        Sets time zone value.

        Parameters
        ----------------
        num: time zone num to set
        """

        self.time_zone = num

    def get_datetime_data_now(self) -> _DatetimeNow:
        """
        Returns a datetime now.

        Returns
        ----------------
        _DatetimeNow data.
        """

        datetime_now = self.__get_datetime_now()
        time_format_pattern = "%H:%M:%S PM" if self.time_format == "pm" else "%I:%M:%S AM"
        time, date = f"🕐{datetime_now.time().strftime(time_format_pattern)}", f"📆{datetime_now.date()}"
        weekday, month_name = self.__get_day_of_week_now(datetime_now.weekday()), self.__get_current_month_name()

        return self._DatetimeNow(time=time, date=date, month_name=month_name, day_of_week=weekday)

    def get_color_scheme_of_current_time_of_year(self) -> _StyleColorScheme | None:
        """
        Returns a StyleColorScheme object.

        Returns
        ---------------
        _StyleColorScheme data.
        """

        month_index = self.__get_datetime_now().month  # current month index

        # Data model - (primary color, secondary color)
        # - primary color = for page background mainly
        # - secondary color = for other elements(UI)
        if 1 <= month_index <= 2:
            return self._StyleColorScheme(primary_color="#03cffc", secondary_color="#02a9cf")  # winter colors
        elif 3 <= month_index <= 5:
            return self._StyleColorScheme(primary_color="#03fca9", secondary_color="#02cf8a")  # spring colors
        elif 6 <= month_index <= 8:
            return self._StyleColorScheme(primary_color="#6cff03", secondary_color="#58d102")  # summer colors
        elif 9 <= month_index <= 11:
            return self._StyleColorScheme(primary_color="#ff8903", secondary_color="#db7704")  # autumn colors
        elif month_index == 12:
            return self._StyleColorScheme(primary_color="#73d5ff", secondary_color="#67bce0")  # december month colors
        else:
            return None

    def get_time_data_until_new_year(self) -> _TimeUntilNewYear:
        """
        Returns a TimeUntilNewYear object.

        Returns
        ---------------
        _TimeUntilNewYear data.
        """

        current_datetime = self.__get_datetime_now()

        # 01.01.new_year 00:00:00
        destination_datetime = datetime(
            year=current_datetime.year + 1,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=timezone.utc
        )

        time_left = destination_datetime - current_datetime
        seconds = int(time_left.seconds)  # get seconds
        days, hours, minutes = time_left.days, int(seconds / self.SEC_IN_HOUR), int(seconds / self.SEC_IN_MINUTE)

        return self._TimeUntilNewYear(days=days, hours=hours, minutes=minutes, seconds=seconds)

    def check_is_new_year_arrived(self) -> bool:
        """
        Checks whether New Year has arrived and returns bool state.

        Returns
        ---------------
        Bool flag.
        """

        current_year = self.__get_datetime_now().year  # current year num now
        if current_year == self.new_year_num:
            self.new_year_num = current_year + 1       # set new year num
            return True
        else:
            return False
