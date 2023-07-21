# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
first_date = '2016-08-23'

@app.route("/api/v1.0/precipitation")
def prcp():
    prcpResults = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>first_date).all()
    return jsonify({"Prcp Results": prcpResults})

@app.route("/api/v1.0/stations")
def stations():
    stationsList = session.query(Station.station, Station.name).all()
    return jsonify(stationsList)

@app.route("/api/v1.0/tobs")
def tobs():
    activeStations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    if activeStations:
        best_station = activeStations[0][0]

        TempBestStation = session.query(Measurement.tobs).filter(Measurement.date>first_date).filter(Measurement.station == best_station).all()
        return jsonify(TempBestStation)
    else:
        return jsonify({"message": "No data found"}), 404

@app.route("/api/v1.0/<start>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(day_temp_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(multi_day_temp_results)


if __name__ == "__main__":
    app.run(debug=True)

