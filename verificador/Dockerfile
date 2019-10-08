FROM ubuntu
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN pip install pymongo
RUN pip install paho-mqtt
RUN apt-get install -y nano
COPY \app\ /home/code
WORKDIR /home/code/
CMD python -u verificador.py rangos.json