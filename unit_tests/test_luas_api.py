import unittest
from mock import patch, PropertyMock

from luas_api import Luas


class TestLuasApi(unittest.TestCase):
    mock_response_text = '<stopInfo created="2020-01-25T16:18:09" stop="Central Park" stopAbv="CPK"><message>Green Line services operating normally</message><direction name="Inbound"><tram dueMins="10" destination="Parnell" /></direction><direction name="Outbound"><tram dueMins="10" destination="Bride\'s Glen" /></direction></stopInfo>'

    class MockLuasApi(object):
        text = '<stopInfo created="2020-01-25T16:18:09" stop="Central Park" stopAbv="CPK"><message>Green Line services operating normally</message><direction name="Inbound"><tram dueMins="10" destination="Parnell" /></direction><direction name="Outbound"><tram dueMins="10" destination="Bride\'s Glen" /></direction></stopInfo>'

    @patch('luas_api.xmltodict.parse', return_value=mock_response_text)
    @patch('luas_api.requests.get')
    def test_request_stop_info_called_with_correct_params(self, mock_request, mock_xmltodict_parse):
        luas = Luas('central park')
        response = luas.request_stop_info
        actual_result_url = mock_request.call_args[0][0]
        actual_result_stop_params = mock_request.call_args[1]
        expected_result_url = 'https://luasforecasts.rpa.ie/xml/get.ashx'
        expected_result_stop_params = {'params': {'action': 'forecast', 'encrypt': 'false', 'stop': 'CPK'}}
        self.assertEqual(actual_result_url, expected_result_url)
        self.assertEqual(actual_result_stop_params, expected_result_stop_params)

    @patch('luas_api.Luas.request_stop_info', new_callable=PropertyMock, return_value=MockLuasApi())
    @patch('luas_api.requests.get')
    def test_time_of_request(self, mock_request, mock_response_text):
        luas = Luas('central park')
        actual_result = luas.time_of_request
        expected_result = '2020-01-25T16:18:09'
        self.assertEqual(actual_result, expected_result)

    @patch('luas_api.Luas.request_stop_info', new_callable=PropertyMock, return_value=MockLuasApi())
    @patch('luas_api.requests.get')
    def test_stop(self, mock_request, mock_response_text):
        luas = Luas('central park')
        actual_result = luas.stop
        expected_result = 'Central Park'
        self.assertEqual(actual_result, expected_result)

    @patch('luas_api.Luas.request_stop_info', new_callable=PropertyMock, return_value=MockLuasApi())
    @patch('luas_api.requests.get')
    def test_message(self, mock_request, mock_response_text):
        luas = Luas('central park')
        actual_result = luas.message
        expected_result = 'Green Line services operating normally'
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
