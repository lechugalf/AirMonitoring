FROM python:3
WORKDIR /usr/src/app
COPY ./app ./
RUN pip install paho-mqtt
CMD [ "python", "-u", "./app.py" ]