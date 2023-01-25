import calendar, time
from datetime import datetime

from tests.conftest import client

class TestBlueprintApi:
    def test_blueprint_api_status_code_with_valid_input_equals_200(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/2023-01-01' is requested (GET)
        THEN checks if http status code is equal to 200
        """
        response = client.get('/api/2023-01-01')
        assert response.status_code == 200

    def test_blueprint_api_content_type_match_json_when_input_is_valid(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/2023-01-01' is requested (GET)
        THEN checks if http header content-type code is equal to application/json
        """
        response = client.get('/api/2023-01-01')
        assert response.headers['Content-Type'] == 'application/json'

    def test_blueprint_api_content_type_match_json_when_input_is_invalid(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param invalid '/api/XXXX' is requested (GET)
        THEN checks if http header content-type code is equal to application/json
        """
        response = client.get('/api/2023--')
        assert response.headers['Content-Type'] == 'application/json'

    def test_blueprint_api_with_date_input_equals_expected_output(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/2023-01-17' (DATE_INPUT) is requested (GET)
        THEN checks if the output from the resource is equal to expected_output
        """
        response = client.get('/api/2023-01-17')
        print(response.data)
        expected_output = {"unix":1673913600,"utc":"Tue, 17 Jan 2023 00:00:00 GMT"}
        assert response.json == expected_output

    def test_blueprint_api_with_empty_input_equals_expected_output(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/' (EMPTY_INPUT) is requested (GET)
        THEN checks if the output from the resource is equal to expected_output
        """
        timestamp_now = calendar.timegm(datetime.utcnow().timetuple())
        date_time = time.gmtime(timestamp_now)
        formated_date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', date_time)
        expected_output = {"unix": "", "utc": ""}
        expected_output['unix'] = timestamp_now
        expected_output['utc'] = formated_date
        
        response = client.get('/api/')
        assert response.json == expected_output

    def test_blueprint_api_with_timestamp_input_equals_expected_output(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/' (TIMESTAMP_INPUT) is requested (GET)
        THEN checks if the output from the resource is equal to expected_output
        """
        expected_output = {"unix":1673913600,"utc":"Tue, 17 Jan 2023 00:00:00 GMT"}
        
        response = client.get('/api/1673913600')
        assert response.json == expected_output

    def test_blueprint_api_with_timestamp_input_equals_expected_output(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/' (TIMESTAMP_INPUT) is requested (GET)
        THEN checks if the output from the resource is equal to expected_output
        """
        expected_output = {"unix":1673913600,"utc":"Tue, 17 Jan 2023 00:00:00 GMT"}
        
        response = client.get('/api/1673913600')
        assert response.json == expected_output

    def test_blueprint_api_with_invalid_input_equals_expected_error_output(self, client):
        """
        GIVEN a flask app is configured for testing
        WHEN endpoint with date param '/api/XXXX' (invalid_input) is requested (GET)
        THEN checks if the output from the resource is equal to expected_output
        """
        expected_output = {"error":"Invalid Date"}
        
        response = client.get('/api/2013--')
        assert response.json == expected_output



    