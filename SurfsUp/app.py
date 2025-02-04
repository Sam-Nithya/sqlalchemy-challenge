# Import the dependencies
from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################


from sqlalchemy import create_engine
# Create engine using the `hawaii.sqlite` database file
database_path = r"C:\Users\s.lokuhewage\sqlalchemy-challenge\Resources\hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")


# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)


# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    routes = {
        "Precipitation Data": "/api/v1.0/precipitation",
        "Stations": "/api/v1.0/stations",
        "Temperature Observations": "/api/v1.0/tobs",
        "Temperature from Start Date": "/api/v1.0/2017-01-01",
        "Temperature from Start to End Date": "/api/v1.0/2016-01-01/2017-01-01"
    }
    print("You have opened the link")
    return jsonify(routes)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - timedelta(days=365)

    # Query to retrieve precipitation data for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary with date as the key and precipitation as the value
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query to retrieve all station data
    results = session.query(Station.station, Station.name).all()
    stations = [{"station": station, "name": name} for station, name in results]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    # Query to retrieve temperature observations for the most active station
    most_active_station_id = 'USC00519281'  # Use the specified active station ID

    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - timedelta(days=365)

    # Query the last 12 months of temperature observation data for this station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary with date as the key and temperature as the value
    temperature_data = {date: tobs for date, tobs in results}
    
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def temperature_from_start(start):
    # Query the min, max, and average temperatures from the start date to the end of the dataset
    results = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
    ).filter(Measurement.date >= start).all()

    # Create a dictionary to hold the results
    temperature_stats = {
        "Start Date": start,
        "Min Temperature": results[0].min_temp,
        "Max Temperature": results[0].max_temp,
        "Avg Temperature": results[0].avg_temp
    }

    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temperature_from_start_to_end(start, end):
    # Query the min, max, and average temperatures from the start date to the end date
    results = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary to hold the results
    temperature_stats = {
        "Start Date": start,
        "End Date": end,
        "Min Temperature": results[0].min_temp,
        "Max Temperature": results[0].max_temp,
        "Avg Temperature": results[0].avg_temp
    }

    return jsonify(temperature_stats)

# To run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)



