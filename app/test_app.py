import unittest
import sqlite3
from datetime import datetime
from unittest.mock import patch

# Import the Flask app for testing
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock SQLite3 connection
        self.conn = sqlite3.connect('birthdays.db')
        self.cursor = self.conn.cursor()

        # Create the user table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                date_of_birth DATE NOT NULL
            )
        """)
        self.conn.commit()

    def tearDown(self):
        # Close the mock SQLite3 connection
        self.cursor.close()
        self.conn.close()

        # Delete the mock database file
        os.remove('birthdays.db')

    def test_insert_update_user(self):
        with app.test_client() as client:
            # Mock the input data
            data = {
                'dateOfBirth': '1990-01-01'
            }
            
            # Patch the real database connection with the mock connection
            with patch('app.conn', self.conn):
                response = client.put('/hello/testuser', json=data)

            # Test the response status code
            self.assertEqual(response.status_code, 204)
            
            # Test that the user was successfully inserted/updated in the mock database
            self.cursor.execute("SELECT * FROM `user` WHERE `username`='testuser'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date())

    def test_delete_user(self):
        with app.test_client() as client:
            # Insert a test user into the mock database
            self.cursor.execute("INSERT INTO `user` (`username`, `date_of_birth`) VALUES ('testuser', '1990-01-01')")
            self.conn.commit()
            
            # Patch the real database connection with the mock connection
            with patch('app.conn', self.conn):
                response = client.delete('/hello/testuser/delete')

            # Test the response status code
            self.assertEqual(response.status_code, 204)
            
            # Test that the user was successfully deleted from the mock database
            self.cursor.execute("SELECT * FROM `user` WHERE `username`='testuser'")
            result = self.cursor.fetchone()
            self.assertIsNone(result)

    def test_get_birthday_message(self):
        with app.test_client() as client:
            # Insert a test user into the mock database
            self.cursor.execute("INSERT INTO `user` (`username`, `date_of_birth`) VALUES ('testuser', '1990-01-01')")
            self.conn.commit()
            
            # Patch the real database connection with the mock connection
            with patch('app.conn', self.conn):
                response = client.get('/hello/testuser')

            # Test the response status code
            self.assertEqual(response.status_code, 200)
            
            # Test that the birthday message is correct
            expected_message = "Hello, testuser! Your birthday is in X day(s)!"
            self.assertEqual(response.json['message'], expected_message)


if __name__ == '__main__':
    unittest.main()
