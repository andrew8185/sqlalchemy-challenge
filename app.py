import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from dateutil.relativedelta import *
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f'Available Routes: <br/>'
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/startdate <br/>'
        f'/api/v1.0/startdate/enddate <br/>'      
    )
    
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    """Return last 12 months of precipitation data"""        
    query_date = dt.date(2017,8,23) - relativedelta(months=12)
    results = session.query(measurement_table.date, measurement_table.prcp).\
                filter(measurement_table.date >= query_date).all()
    session.close()
    
    year_prcp_data = list(np.ravel(results))
    return jsonify(year_prcp_data)

@app.route('/api/v1.0/stations')
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)
    """Return list of stations"""
    results = session.query(station_table.station).all()
    session.close()
    
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)
    """Temperature observations of the most active station for the past year"""
    query_date = dt.date(2017,8,23) - relativedelta(months=12)
    results = session.query(measurement_table.date, measurement_table.tobs).\
    filter(measurement_table.date >= query_date).\
    filter(measurement_table.station == 'USC00519281').all()
    
    year_active_temp_data = list(np.ravel(results))
    return jsonify(year_active_temp_data)

print(measurement_table)

@app.route('/api/v1.0/<start>')
def summary_stats_after_start(start):
    session = Session(engine)
    """Return summary statistics of temperature after start date"""
    
    results = session.query(func.min(measurement_table.tobs),
                                     func.max(measurement_table.tobs),
                                     func.avg(measurement_table.tobs)).\
                                        filter((measurement_table.date) >= start).all()
    
    summary_after_date = list(np.ravel(results))
    return jsonify(summary_after_date)

@app.route('/api/v1.0/<start>/<end>')
def summary_stats_between_dates(start,end):
    session = Session(engine)
    """Return summary statistics of temperature between the start and end date"""
    
    results = session.query(func.min(measurement_table.tobs),
                                     func.max(measurement_table.tobs),
                                     func.avg(measurement_table.tobs)).\
                                        filter((measurement_table.date) >= start).\
                                        filter((measurement_table.date) <= end).all()
    
    summary_between_dates = list(np.ravel(results))
    return jsonify(summary_between_dates)

if __name__ == '__main__':
    app.run(debug=True)
