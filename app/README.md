# Home Task Application

### Note
Please note that to build this python app with a database I'm using a remote database, tanking advantage of service AWS RDS Aurora compatible with Mysql. 
That will allow to keep our date with backups and recurrent snapshots, scaling instances to read and write and without having the issues of maintaining the database.

## Functions
 - healthcheck
 - insert_update_user
 - delete_user
 - get_birthday_message

#### healthcheck
Endpoint: ```/healthcheck```

Used to execute healthcheck to the app.
It's also used on Kubernetes to check Readiness and Liveness probes.

#### insert_update_user
Endpoint: ```/hello/username```

Used to insert or update user to the database.
There are some requirementes like user can only contain letters, name of the user must be provided through the URL and date must be in YYY-MM-DD format, and also data must be passed through header with json content.

Expected Request: ```PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” }```

Expected Return: ```204 No Content```


#### delete_user
Endpoint: ```/hello/username/delete```

Used to delete user to the database.
There are some requirementes like user can only contain letters, name of the user must be provided through the URL.

Expected Request: ```DELETE /hello/<username>/delete```

Expected Return: ```204 No Content```


#### get_birthday_message
Endpoint: ```/hello/username```

Used to get user from the database and calculate how many days left to the next birthday.
There are some requirementes like user can only contain letters, name of the user must be provided through the URL.

If the user already had his birthday this year we should add +1 year to the next birthday.

If succeeded we should get the following messages: 

If username’s birthday is in N days:

```{ “message”: “Hello, <username>! Your birthday is in N day(s)”```

If username’s birthday is today:

```{ “message”: “Hello, <username>! Happy birthday!” }```

Expected Request: ```GET /hello/<username>/delete```

Expected Return: ```200 OK```


## Results
First check if we want to run the tests external to the cluster we need to enable port forward to the home-task service.
![Port Forward](../docs/images/portforward.jpg?raw=true "Port Forward")
In this case I'll use Thunde Client on VSCode.

You can test inside cluster by using curl tool.

```kubectl run curl --image=curlimages/curl -i --tty -- sh```

#### healthcheck
![Healthcheck](../docs/images/healthcheck.jpg?raw=true "Healthcheck")

#### insert_update_user
 ![Insert user - Normal birthday](../docs/images/insert_test_normal_birthday.jpg?raw=true "Insert user - Normal birthday")
 ![Insert user - Birthday Today](../docs/images/insert_test_its_birthday.jpg?raw=true "Insert user - Birthday Today")

#### delete_user
 ![Delete User](../docs/images/delete_test.jpg?raw=true "Delete User")

#### get_birthday_message
 ![Get user - Normal birthday](../docs/images/get_test_days_to_birthday.jpg?raw=true "Get user - Normal birthday")
 ![Get user - Birthday Today](../docs/images/get_test_its_birthday.jpg?raw=true "Get user - Birthday Today")

 Using grafana with Loki we can check all the logs from the operations we just did.
  ![Logs](../docs/images/grafana_logs.jpg?raw=true "Logs")


## Results with curl
#### healthcheck
![Healthcheck](../docs/images/curl-healthcheck.jpg?raw=true "Healthcheck")

#### insert_update_user
 ![Insert user - Normal birthday](../docs/images/curl-insert.jpg?raw=true "Insert user - Normal birthday")
#### delete_user
 ![Delete User](../docs/images/curl-delete.jpg?raw=true "Delete User")

#### get_birthday_message
 ![Get user - Normal birthday](../docs/images/curl-get.jpg?raw=true "Get user - Normal birthday")

## Testing the APP
Unfortunately I was not able to complete the test task.
I was not able to use mocks for testing mysql integration and then I had to move to sqllite3 database.
However, the test is designed but unfortunately it's not working properly.

To run the test use the following command:
``` 
python3 -m unittest test_app.py

```
It will use the local database named "birthdays.db".