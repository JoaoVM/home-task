FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /tmp
EXPOSE 5000
ENV FLASK_APP=apppsql.py
ENTRYPOINT [ "python", "apppsql.py" ]
CMD ["flask", "run", "--host", "0.0.0.0"]
