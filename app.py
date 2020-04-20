import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Connection
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
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
        f"Welcome to the Hawaii Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/station"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation"""
    # Query all date and precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    weather_data = []
    for date, prcp in results:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        weather_data.append(date_dict)

    return jsonify(weather_data)



@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    station = [result[0] for result in results[:]]
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation"""
    # Query all date and precipitation data

    most_active_stn_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').order_by(Measurement.tobs.asc()).all()

    session.close()
 
    
    return jsonify(most_active_stn_temps)


# @app.route("/api/v1.0/date/<start>")
# def start_date(start):
#     # Create our session (link) from Python to the DB
#     session= Session(engine)
#     stn_stats = session.query((Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()  
#     session.close()
#     return jsonify(stn_stats)

@app.route("/api/v1.0/date/<start>")
def start_date(start):
    session = Session(engine)
    stn_temp = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()
    return jsonify(stn_temp)


@app.route("/api/v1.0/date/<start>/<end>")
def calc_temps(start, end):
    session = Session(engine)
    stn_temp_range = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    return jsonify(stn_temp_range)


if __name__ == "__main__":
    app.run(debug=True)
