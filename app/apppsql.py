import os
#os.system("python3 -m pip install flask &")
#os.system("python3 -m pip install mysql.connector &")
#os.system("python3 -m pip install psycopg2 &")
import psycopg2

from flask import Flask, request, jsonify
from psycopg2 import errorcodes
from datetime import datetime

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(user='postgres', password='Rev0lutAdm1n', host='psqlbirthdays.cluster-cucrythpesxp.eu-west-1.rds.amazonaws.com', database='birthdays', sslmode='require')

cursor = conn.cursor()
# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "birthdays"."user" (
  "username" VARCHAR(16) NOT NULL,
  "date_of_birth" DATE NOT NULL,
  PRIMARY KEY ("username"));
""")

conn.commit()

@app.route('/healthcheck')
def healthcheck():
    return jsonify(status="UP"), 200

@app.route('/hello/<username>', methods=['PUT'])
def insert_update_user(username):
    # Validate username (letters only)
    if not username.isalpha():
        return 'Invalid username. Username must contain only letters.', 400
    
    # Validate date of birth format and make sure it is before today's date
    try:
        date_of_birth = datetime.strptime(request.json.get('dateOfBirth'), '%Y-%m-%d').date()
        if date_of_birth >= datetime.today().date():
            return 'Invalid date of birth. Date of birth must be before today.', 400
    except ValueError:
        return 'Invalid date of birth format. Date of birth should be in YYYY-MM-DD format.', 400

    # Save/update user's name and date of birth in the database
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO \"birthdays\".\"user\" (\"username\",\"date_of_birth\") VALUES (%s, %s)", (username, date_of_birth))
        conn.commit()
        return '', 204
    except psycopg2.Error as err:
        if err.pgcode == errorcodes.INVALID_PASSWORD:
            print("Something is wrong with your password")
        elif err.pgcode == errorcodes.DUPLICATE_TABLE:
            print("Table already exists")
        else:
            print("Other Error: %s" % err) 
        if cursor.conn:
            cursor.conn.rollback()    


@app.route('/hello/<username>/delete', methods=['DELETE'])
def delete_user(username):
    # Validate username (letters only)
    if not username.isalpha():
        return 'Invalid username. Username must contain only letters.', 400

    # Delete user's name and date of birth in the database
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM \"birthdays\".\"user\" WHERE \"username\"=%s", (username,))
        conn.commit()
        return '', 204
    except psycopg2.Error as err:
        if err.pgcode == errorcodes.INVALID_PASSWORD:
            print("Something is wrong with your password")
        elif err.pgcode == errorcodes.INVALID_TABLE_NAME:
            print("Table does not exist")
        else:
            print("Other Error: %s" % err) 
        if cursor.conn:
            cursor.conn.rollback()    


@app.route('/hello/<username>', methods=['GET'])
def get_birthday_message(username):
    # Validate username (letters only)
    if not username.isalpha():
        return 'Invalid username. Username must contain only letters.', 400

    # Check if user exists in the database
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT \"date_of_birth\" FROM \"birthdays\".\"user\" WHERE \"username\"=%s", (username,))
        result = cursor.fetchone()
        conn.commit()
    except psycopg2.Error as err:
        if err.pgcode == errorcodes.INVALID_PASSWORD:
            print("Something is wrong with your password")
        elif err.pgcode == errorcodes.INVALID_TABLE_NAME:
            print("Table does not exist")
        else:
            print("Other Error: %s" % err) 
        if cursor.conn:
            cursor.conn.rollback()    

    if result is None:
        return 'User not found.', 404

    # Get the user's date of birth from the database
    date_of_birth = result[0]
    converted_date_of_birth = datetime.strptime(str(date_of_birth), '%Y-%m-%d').date()

    # Calculate the number of days until the user's next birthday
    today = datetime.today().date()
    next_birthday = datetime.strptime(f'{today.year}-{converted_date_of_birth.month}-{converted_date_of_birth.day}', '%Y-%m-%d').date()

    # If the user already had is birthday this year add one more year to the next birthday
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    days_until_birthday = (next_birthday - today).days

    # Prepare the birthday message based on the number of days until the next birthday
    if days_until_birthday == 0:
        message = f'Hello, {username}! Happy birthday!'
    else:
        message = f'Hello, {username}! Your birthday is in {days_until_birthday} day(s)!'

    return jsonify(message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Close the database connection when the application shuts down
@app.teardown_appcontext
def close_connection(exception):
    conn.close()
