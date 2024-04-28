import unittest
from unittest.mock import patch, MagicMock
from .bank_holiday_updater import BankHolidayUpdater, sqlite3, requests


class TestBankHolidayUpdater(unittest.TestCase):
    @patch('sqlite3.connect')
    def test_create_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        updater = BankHolidayUpdater()
        updater.create_database()

        mock_cursor.execute.assert_called()

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'division1': {'events': [
            {'title': 'Event1', 'date': '2024-05-01', 'notes': 'Note1', 'bunting': True}]}}
        mock_get.return_value = mock_response

        updater = BankHolidayUpdater()
        data = updater.fetch_data()

        self.assertIsNotNone(data)
        self.assertEqual(data['division1']['events'][0]['title'], 'Event1')

    @patch('requests.get')
    def test_fetch_data_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        updater = BankHolidayUpdater()
        data = updater.fetch_data()

        self.assertIsNone(data)

    @patch('sqlite3.connect')
    def test_insert_data(self, mock_connect):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        updater = BankHolidayUpdater()
        updater.insert_data('division1', 'Event1', '2024-05-01', 'Note1', True)

        mock_cursor.execute.assert_called()

    @patch('sqlite3.connect')
    @patch.object(BankHolidayUpdater, 'fetch_data')
    def test_fetch_and_cache_data(self, mock_fetch_data, _):
        self.test_create_database()
        mock_fetch_data.return_value = {'division1': {'events': [
            {'title': 'Event1', 'date': '2024-05-01', 'notes': 'Note1', 'bunting': True}]}}

        updater = BankHolidayUpdater()
        updater.fetch_and_cache_data()

        self.assertEqual(len(updater.fetch_data()), 1)


if __name__ == '__main__':
    unittest.main()
