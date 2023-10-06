# Home Task Application

### Note
Please note that to build this Python app with a database I'm using a remote database, taking advantage of the service AWS RDS Aurora compatible with PostgreSQL. 
That will allow us to keep our date with backups and recurrent snapshots, scaling instances to read and write without having the issues of maintaining the database.

### Local usage of the app
First please be aware, that if you try to run Python code locally, before starting run the following command:

```
pip install -r requirements.txt
```
If for some reason psycopg2 failed to install, open requirements.txt and comment psycopg2 and uncomment psycopg2-binary. Then run the command again and should work fine.

To test the app please run the following command:

```
python3 apppsql.py
```

Then use the Thunder Client collection to execute the tests.


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

Used to insert or update users to the database.
There are some requirements like the user can only contain letters, the name of the user must be provided through the URL and date must be in YYY-MM-DD format, and data must be passed through the header with JSON content.

Expected Request: ```PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” }```

Expected Return: ```204 No Content```


#### delete_user
Endpoint: ```/hello/username/delete```

Used to delete users from the database.
There are some requirements like user can only contain letters, name of the user must be provided through the URL.

Expected Request: ```DELETE /hello/<username>/delete```

Expected Return: ```204 No Content```


#### get_birthday_message
Endpoint: ```/hello/username```

Used to get users from the database and calculate how many days are left for the next birthday.
There are some requirements like user can only contain letters, name of the user must be provided through the URL.

If the user already had his birthday this year we should add +1 year to the next birthday.

If succeed we should get the following messages:

If username’s birthday is in N days:

```{ “message”: “Hello, <username>! Your birthday is in N day(s)”```

If username’s birthday is today:

```{ “message”: “Hello, <username>! Happy birthday!” }```

Expected Request: ```GET /hello/<username>/delete```

Expected Return: ```200 OK```


## Results
First, check if we want to run the tests external to the cluster we need to enable port forward to the home-task service.
![Port Forward](../docs/images/portforward.jpg?raw=true "Port Forward")
In this case, I'll use Thunder Client on VSCode.

You can test inside the cluster by using the curl tool.

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
Regarding the tests, it will execute the unit tests for the app requirements.
I was able to use mocks for testing postgresql integration.

To run the test use the following command:
``` 
pip install -r requirements.txt

python3 -m unittest -v test_app.py

```

Also, when the statefulset is created, it will also create an init container that will execute the unit tests.
You can check the result of the init container on logs of the init container or check the example in the following image.
If the tests fail then the main container won't be installed.

 ![Init Container Tests](../docs/images/init-container-tests.jpg?raw=true "Init Container Tests")