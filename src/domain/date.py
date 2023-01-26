import calendar
import re
import time
from datetime import datetime


class DateModel:
    def __init__(self, date_str: str):
        self.date_str = date_str
        self.input_type = self.determine_input()

    def __str__(self):
        if self.input_type == "date":
            return f'DateModel({self.date_str.split("-")[0]}-{self.date_str.split("-")[1]}-{self.date_str.split("-")[2]})'
        elif self.input_type == "empty":
            return f"DateModel({self.get_formated_data})"
        else:
            return f"DateModel({self.date_str})"

    def _validate_date(self) -> datetime | int:
        """
        Validates the input data
        can accept: YYYY-MM-DD
                    EMPTY
                        OR
                    TIMESTAMP
        """
        if self.input_type == "date" or self.input_type == "empty":
            if self.date_str == "":
                """IF DATE IS ''"""
                return datetime.utcnow()
            else:
                date_str_splitted = self.date_str.split("-")

                year = date_str_splitted[0]
                month = date_str_splitted[1]
                day = date_str_splitted[2]

                return datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
        else:
            if self.input_type == "seconds":
                return int(self.date_str)
            elif self.input_type == "milliseconds":
                return int(self.date_str) / 1000
            elif self.input_type == "microseconds":
                return int(self.date_str) / 1000000
            elif self.input_type == "nanoseconds":
                return int(self.date_str) / 1000000000

    def _convert_to_unix_timestamp(self) -> int:
        """
        Convert time into unix timestamp
            return timestamp in seconds
            to transform into milliseconds -> multiply by 1000
            microseconds -> (* 1000000)
            nanoseconds -> (* 1000000000)

        calendar.timegm converts from UTC timestamp
        It returns the corresponding Unix timestamp value assuming an epoch of 1970-01-01.
        """
        validated_date = self._validate_date()

        unix_date = calendar.timegm(validated_date.timetuple())
        return unix_date

    def _format_date(self) -> str:
        """
        From input DateModel('2023-01-17')
        Returns the date in the format:
            (WEEKDAY, DAY MONTH YEAR HR:MIN:SEC GMT)
            For example: Tue, 17 Jan 2023 00:00:00 GMT
        """
        if self.input_type == "date" or self.input_type == "empty":
            validated_date = self._validate_date()
            unix_date = calendar.timegm(
                validated_date.timetuple()
            )  # generates unix timestamp

            # Timestamp -> struct_time obj
            # converts unix timestamp (in seconds) into struct_time obj
            date_time = time.gmtime(unix_date)

            # strftime converts datetime obj into diferent string formats
            formated_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", date_time)
            return formated_date

    @property
    def get_unix_timestamp(self):
        """
        Returns unix timestamp in SECONDS
        Input:  DateModel('2023-01-17')
        Output: 1673913600
        """
        if self.input_type == "date" or self.input_type == "empty":
            return self._convert_to_unix_timestamp()

    @property
    def get_date_from_timestamp(self):
        """
        Returns date if input is TIMESTAMP
        Input:  DateModel('1673913600')
        Output: "Tue, 17 Jan 2023 00:00:00 GMT"
        """
        if self.input_type != "date" and self.input_type != "empty":
            return self._convert_timestamp_formated_date()

    @property
    def get_formated_data(self):
        """
        Returns formated date if input is DATE
        Input:  DateModel('2023-01-17')
        Output: Tue, 17 Jan 2023 00:00:00 GMT
        """
        if self.input_type == "date" or self.input_type == "empty":
            return self._format_date()

    def date_as_dict(self):
        """
        Converts Obj to dict {"unix": UNIX_TIMESTAMP, "utc": FORMATED_DATA}
        """
        if self.input_type != "date" and self.input_type != "empty":
            return {
                "unix": int(self.date_str),
                "timestamp_format": self.input_type,
                "utc": self.get_date_from_timestamp,
            }
        elif self.input_type == "empty":
            return {"unix": self.get_unix_timestamp, "utc": self.get_formated_data}
        elif self.input_type == "date":
            return {"unix": self.get_unix_timestamp, "utc": self.get_formated_data}

    def _convert_timestamp_formated_date(self):
        """
        Converts TIMESTAMP into formated date.
        For example:
        1673913600 -> Tue, 17 Jan 2023 00:00:00 GMT
        """
        if self.input_type != "date":
            timestamp = self._validate_date()
            date_time = time.gmtime(timestamp)
            formated_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", date_time)
            return formated_date

    def determine_input(self):
        """
        Determines if input data is DATE or TIMESTAMP (in seconds, milliseconds, microseconds, nanoseconds)
        """
        value = self.date_str
        regex_str = r"(\d{5,})*$|([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})*$|^(?![\s\S])*$"
        input = re.match(regex_str, value)

        if input is not None:
            if input.group() == "":
                return "empty"
            elif re.match(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}", input.group()):
                return "date"
            elif len(input.group()) >= 9 and len(input.group()) <= 11:
                return "seconds"
            elif len(input.group()) >= 12 and len(input.group()) <= 14:
                return "milliseconds"
            elif len(input.group()) >= 15 and len(input.group()) <= 16:
                return "microseconds"
            elif len(input.group()) >= 17 and len(input.group()) <= 20:
                return "nanoseconds"
            else:
                raise Exception("invalid_date")
        else:
            raise Exception("invalid_date")
