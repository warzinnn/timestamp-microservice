import calendar
import json
import time
from datetime import datetime

import pytest

from src.domain.date import DateModel


class TestDateModel:
    def test_date_gmt_obj_successfully_converts_into_unix_timestamp(self):
        """
        GIVEN a date is inputed with the format (YYYY-mmmm-dd)
        WHEN converts the inputed date into unix format
        THEN return unix date format (GMT Time) in seconds
        """
        date_obj = DateModel("2023-01-17")
        assert date_obj.get_unix_timestamp == 1673913600

    def test_date_gmt_obj_successfully_converts_into_unix_timestamp_without_specifying_any_data(
        self,
    ):
        """
        GIVEN a not inputed data (uses default value from the system)
        WHEN converts the inputed date into unix format
        THEN return unix date format (GMT Time) in seconds
        """
        date_obj = DateModel("")

        assert_data = calendar.timegm(datetime.utcnow().timetuple())

        assert date_obj.get_unix_timestamp == assert_data

    def test_date_gmt_obj_successfully_converts_into_unix_timestamp_in_other_time_format(
        self,
    ):
        """
        GIVEN a not inputed data (uses default value from the system)
        WHEN converts the inputed date into unix format
        THEN return unix date format (GMT Time) in milliseconds/microseconds/nanoseconds
        """
        date_obj = DateModel("")

        assert_data = calendar.timegm(datetime.utcnow().timetuple())

        assert date_obj.get_unix_timestamp * 1000 == assert_data * 1000  # second
        assert (
            date_obj.get_unix_timestamp * 1000000 == assert_data * 1000000
        )  # microseconds
        assert (
            date_obj.get_unix_timestamp * 1000000000 == assert_data * 1000000000
        )  # nanoseconds

    def test_date_gmt_obj_successfully_formats_date(self):
        """
        GIVEN a date is inputed with the format (YYYY-Mm-dd)
        WHEN formats the inputed data
        THEN return the data in the format (WEEKDAY, DAY MONTH YEAR HR:MIN:SEC GMT)
        """
        date_obj = DateModel("2023-01-17")
        assert date_obj.get_formated_data == "Tue, 17 Jan 2023 00:00:00 GMT"

    def test_date_gmt_obj_returned_as_dict(self):
        """
        GIVEN a date is inputed with the format (YYYY-Mm-dd)
        WHEN converts the date obj into dictionary
        THEN returns the dict with unix and utc key
        """
        expected_dict = {"unix": 1673913600, "utc": "Tue, 17 Jan 2023 00:00:00 GMT"}
        date_obj = DateModel("2023-01-17")
        assert date_obj.date_as_dict() == expected_dict

    def test_date_empty_obj_returned_as_dict(self):
        """
        GIVEN an empty input
        WHEN converts the date obj into dictionary
        THEN returns the dict with unix and utc key from the hour in the moment
        """
        timestamp_now = calendar.timegm(datetime.utcnow().timetuple())
        date_time = time.gmtime(timestamp_now)
        formated_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", date_time)
        assert_data = {"unix": timestamp_now, "utc": f"{formated_date}"}

        date_obj = DateModel("")
        assert date_obj.date_as_dict() == assert_data

    def test_date_dict_serialized_as_JSON(self):
        """
        GIVEN a date is inputed with the format (YYYY-Mm-dd)
        WHEN converts the date obj into dictionary
        THEN returns the date obj as JSON
        """
        expected_json = (
            """{"unix": 1673913600, "utc": "Tue, 17 Jan 2023 00:00:00 GMT"}"""
        )

        date_obj = DateModel("2023-01-17")
        assert json.dumps(date_obj.date_as_dict()) == expected_json

    def test_timestamp_dict_serialized_as_JSON(self):
        """
        GIVEN a timestamp is inputed
        WHEN converts the date obj into dictionary
        THEN returns the date obj as JSON
        """
        expected_json = """{"unix": 1673913600, "timestamp_format": "seconds", "utc": "Tue, 17 Jan 2023 00:00:00 GMT"}"""

        date_obj = DateModel("1673913600")
        assert json.dumps(date_obj.date_as_dict()) == expected_json

    def test_timestamp_format_return_as_expected(self):
        """
        GIVEN a timestamp is inputed
        WHEN determine the timestamp format
        THEN returns the type of timestamp in the expected format
        """
        date_obj_seconds = DateModel("1673913600")
        date_obj_milliseconds = DateModel("1673913600000")
        date_obj_microseconds = DateModel("1673913600000000")
        date_obj_nanoseconds = DateModel("1673913600000000000")

        assert date_obj_seconds.input_type == "seconds"
        assert date_obj_milliseconds.input_type == "milliseconds"
        assert date_obj_microseconds.input_type == "microseconds"
        assert date_obj_nanoseconds.input_type == "nanoseconds"

    def test_receive_timestamp_in_seconds_and_then_converts_to_date(self):
        """
        GIVEN a timestamp is inputed in seconds format
        WHEN converts the inputed timestamp into date format
        THEN return the data in the format (WEEKDAY, DAY MONTH YEAR HR:MIN:SEC GMT)
        """
        date_obj = DateModel("1673913600")
        assert date_obj.get_date_from_timestamp == "Tue, 17 Jan 2023 00:00:00 GMT"

    def test_receive_timestamp_in_milliseconds_and_then_converts_to_date(self):
        """
        GIVEN a timestamp is inputed in milliseconds format
        WHEN converts the inputed timestamp into date format
        THEN return the data in the format (WEEKDAY, DAY MONTH YEAR HR:MIN:SEC GMT)
        """
        date_obj = DateModel("1673913600000")
        assert date_obj.get_date_from_timestamp == "Tue, 17 Jan 2023 00:00:00 GMT"

    def test_receive_timestamp_in_microseconds_and_then_converts_to_date(self):
        """
        GIVEN a timestamp is inputed in microseconds format
        WHEN converts the inputed timestamp into date format
        THEN return the data in the format (WEEKDAY, DAY MONTH YEAR HR:MIN:SEC GMT)
        """
        date_obj = DateModel("1673913600000000")
        assert date_obj.get_date_from_timestamp == "Tue, 17 Jan 2023 00:00:00 GMT"

    def test_receive_timestamp_in_nanoseconds_and_then_converts_to_date(self):
        """
        GIVEN a timestamp is inputed in nanoseconds format
        WHEN converts the inputed timestamp into date format
        THEN return the data in the format (WEEKDAY, DAY MONTH YEAR HR:MIN:SEC GMT)
        """
        date_obj = DateModel("1673913600000000000")
        assert date_obj.get_date_from_timestamp == "Tue, 17 Jan 2023 00:00:00 GMT"

    def test_receive_timestamp_then_call_fuction_formated_data_and_function_get_unix_timestamp_and_returns_None(
        self,
    ):
        """
        GIVEN a timestamp is inputed
        WHEN call functions used with date
        THEN returns None
        """
        date_obj = DateModel("1673913600000000000")
        assert date_obj.get_formated_data is None
        assert date_obj.get_unix_timestamp is None

    def test_receive_date_then_call_fuction_get_date_from_timestamp_and_function_and_returns_None(
        self,
    ):
        """
        GIVEN a date is inputed
        WHEN call functions used with timestamp
        THEN returns None
        """
        date_obj = DateModel("2023-01-17")
        assert date_obj.get_date_from_timestamp is None

    def test_receive_invalid_input_then_function_raises_exception(self):
        """
        GIVEN a invalid input is sent
        WHEN obj is created
        THEN raises an 'invalid date' exception
        """
        with pytest.raises(Exception):
            assert DateModel("2023")
        with pytest.raises(Exception):
            assert DateModel("2023-01-")
        with pytest.raises(Exception):
            assert DateModel("----")
        with pytest.raises(Exception):
            assert DateModel("01-01")
        with pytest.raises(Exception):
            assert DateModel(" ")
        with pytest.raises(Exception):
            assert DateModel("2023/01/01")
        with pytest.raises(Exception):
            assert DateModel("16739136000000000000000000000000000000000000000")
        with pytest.raises(Exception):
            assert DateModel("167391360000000000000")
        with pytest.raises(Exception):
            assert DateModel("-1")
        with pytest.raises(Exception):
            assert DateModel("abc")
        with pytest.raises(Exception):
            assert DateModel("?")
        with pytest.raises(Exception):
            assert DateModel("/")
        with pytest.raises(Exception):
            assert DateModel("'")
        with pytest.raises(Exception):
            assert DateModel("2023-01-01-")
