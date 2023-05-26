# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_precip = session.query(measurement.date,measurement.prcp).filter(measurement.date >= one_year_date).all()
    precip = {date: prcp for date, prcp in last_year_precip}
    session.close()
    return jsonify(precip)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    no_stations = session.query(station.station).all()
    stations = list(np.ravel(no_stations))
    session.close()
    return jsonify(stations=stations)

#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs()
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_tobs = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= one_year_date).all()
    temps = list(np.ravel(last_year_tobs))
    session.close()
    return jsonify(temps)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start=None, end=None):
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    print ("=============")
    print (start)
    print (end)
    print ("=============")
    if not end:
        results = session.query(*sel).filter(measurement.date >= start).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)
    results = session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end).all()
    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps)
       
if __name__ == '__main__':
    app.run(debug=True)