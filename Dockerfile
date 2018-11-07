FROM python:3.5.6-slim-jessie
RUN apt-get update
RUN apt-get -y install libgtk2.0-dev
RUN apt-get -y install libspatialindex-dev

ADD . /
WORKDIR /
RUN pip install -r requirements.txt
WORKDIR /services

EXPOSE 80

CMD [ "python", "./WaitressServer.py" ]
