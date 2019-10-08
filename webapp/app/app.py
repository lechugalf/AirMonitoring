from flask import Flask, jsonify, render_template, request, abort
from flask_pymongo import PyMongo
from bson import json_util
import json
import sys
import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/project'
mongo = PyMongo(app)

#
# CONTROLLERS
#

def getStations():
    result = mongo.db.stations.find()
    documents = []
    for document in result:
        documents.append({
            'idStation': document['idStation'],
            'nameStation': document['nameStation'],
            'longitud': document['longitud'],
            'latitud': document['latitud'],
            'elevacion': document['elevacion'],
            'operacion': document['operacion'],
        })
    return documents


def getParameters():
    result = mongo.db.parameters.find()
    documents = []
    for document in result:
        documents.append({
            'idParameter': document['idParameter'],
            'nameParameter': document['nameParameter'],
            'unit': document['unit'],
        })
    return documents


def getAllMeasurements():
    result = mongo.db.measurements.find()
    documents = []
    for document in result:
        documents.append({
            'idStation': document['idStation'],
            'mediciones': document['mediciones'],
            'dateTime': document['dateTime'],
        })
    return documents


def getMeasurementsByDate(start, end):
    """Params start and end are Datetime objects"""
    result = mongo.db.measurements.find({
        'dateTime': {
            '$gte': start,
            '$lte': end
        }
    })
    documents = []
    for document in result:
        documents.append({
            'idStation': document['idStation'],
            'mediciones': document['mediciones'],
            'dateTime': document['dateTime'].isoformat(),
        })
    return documents


def getData():

    #Get stations
    stations = getStations()

    #Get parameters
    parameters = getParameters()

    #Get 5 days of measurements from now()
    current = datetime.datetime(2016, 1, 8, 10, 0)

    #final = datetime.datetime(2016, 1, 2, 10, 0)
    datetimeRange = [current - datetime.timedelta(hours=x) for x in range(3*24)]
    final = datetime.datetime.strptime(datetimeRange[-1].isoformat(), "%Y-%m-%dT%H:%M:%S")
    measurements = getMeasurementsByDate(final, current)

    #data
    data = {
        'datetime': current,
        'stations': stations,
        'parameters': parameters,
        'measurements': measurements
    }

    return data

#
# HELPERS
#

def abort_if_file_doesnt_exist(filename):
    abort(404, message="File {} doesn't exist".format(filename))


#
# VIEWS
#

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data():
    if request.method == 'GET':
        data = getData()
        return jsonify(data)
    else:
        abort(404, message="Unknown endpoint!")



@app.route('/stations', methods=['GET'])
def stations():
    if request.method == 'GET':
        stations = getStations()
        return jsonify(stations)
    else:
        abort(404, message="Unknown endpoint!")


@app.route('/parameters', methods=['GET'])
def parameters():
    if request.method == 'GET':
        parameters = getParameters()
        return jsonify(parameters)
    else:
        abort(404, message="Unknown endpoint!")


@app.route('/measurements', methods=['GET'])
def getMeasurements():
    if request.method == 'GET':
        if 'start' in request.args and 'end' in request.args:
            start = request.args.get('start', '')
            end = request.args.get('end', '')
            sttDatetime = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            endDatetime = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            measurements = getMeasurementsByDate(sttDatetime, endDatetime)
            return jsonify(measurements)
        else:
            measurements = getAllMeasurements()
            return jsonify(measurements)
    else:
        abort(404, message="Unknown endpoint!")

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    