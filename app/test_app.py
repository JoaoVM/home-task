import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import json
from psycopg2 import errorcodes
import logging
import apppsql

class TestApp(unittest.TestCase):
    def setUp(self):
        apppsql.app.testing = True
        self.app = apppsql.app.test_client()
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass

    def test_healthcheck(self):
        response = self.app.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'UP'})

    @patch('apppsql.conn')
    def test_insert_update_user_success(self, mock_conn):
        date_of_birth = {'dateOfBirth': '1990-01-01'}
        mock_request = MagicMock()
        mock_request.json = date_of_birth 

        # Create a MagicMock object for the cursor
        mock_cursor = MagicMock()
        # Assign the MagicMock object to the cursor attribute of the mock_conn object
        mock_conn.cursor.return_value = mock_cursor

        response = self.app.put('/hello/testuser', json=mock_request.json)
        self.assertEqual(response.status_code, 204)
        mock_cursor.execute.assert_called_with(
            "INSERT INTO \"birthdays\".\"user\" (\"username\",\"date_of_birth\") VALUES (%s, %s)",
            ('testuser', datetime.strptime(date_of_birth['dateOfBirth'], '%Y-%m-%d').date())
        )
        mock_conn.commit.assert_called_once()

    @patch('apppsql.conn')
    def test_delete_user_success(self, mock_conn):
        username = 'testuser'
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        response = self.app.delete(f"/hello/{username}/delete")

        self.assertEqual(response.status_code, 204)
        mock_cursor.execute.assert_called_with(
            "DELETE FROM \"birthdays\".\"user\" WHERE \"username\"=%s", (username,))
        mock_conn.commit.assert_called_once()


    @patch('apppsql.conn')
    def test_get_birthday_message(self, mock_conn):
        username = 'testuser'
        expected_message = 'Hello, testuser! Your birthday is in 10 day(s)!'
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (datetime.now().date() + timedelta(days=10),)
        mock_conn.cursor.return_value = mock_cursor

        response = self.app.get(f"/hello/{username}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], expected_message)
        mock_cursor.execute.assert_called_with(
            "SELECT \"date_of_birth\" FROM \"birthdays\".\"user\" WHERE \"username\"=%s",
            (username,))
        mock_conn.commit.assert_called_once()


    def test_insert_update_user_invalid_username(self):
        username = 'testuser123'
        date_of_birth = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

        response = self.app.put(f'/hello/{username}', json={'dateOfBirth': date_of_birth})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Invalid username. Username must contain only letters.')

    def test_insert_update_user_invalid_date_of_birth_format(self):
        username = 'testuser'
        date_of_birth = '2021/01/01'

        response = self.app.put(f'/hello/{username}', json={'dateOfBirth': date_of_birth})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Invalid date of birth format. Date of birth should be in YYYY-MM-DD format.')

    def test_insert_update_user_invalid_date_of_birth(self):
        username = 'testuser'
        date_of_birth = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

        response = self.app.put(f'/hello/{username}', json={'dateOfBirth': date_of_birth})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Invalid date of birth. Date of birth must be before today.')

    def test_delete_user_invalid_username(self):
        username = 'testuser123'

        response = self.app.delete(f'/hello/{username}/delete')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Invalid username. Username must contain only letters.')



if __name__ == '__main__':
    unittest.main()
