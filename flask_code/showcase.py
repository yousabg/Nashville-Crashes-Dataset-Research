#the main flask code

from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
from geopy.distance import geodesic
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

#Redacted
app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",
    hostname="",
    databasename="",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Accidents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accident_number = db.Column(db.String(50))
    number_of_motor_vehicles = db.Column(db.Integer)
    number_of_injuries = db.Column(db.Integer)
    number_of_fatalities = db.Column(db.Integer)
    property_damage = db.Column(db.String(50))
    hit_and_run = db.Column(db.String(50))
    reporting_officer = db.Column(db.String(50))
    collision_type = db.Column(db.String(50))
    collision_type_description = db.Column(db.String(255))
    weather = db.Column(db.String(50))
    weather_description = db.Column(db.String(255))
    illuaccidemination = db.Column(db.String(50))
    illumination_description = db.Column(db.String(255))
    harmfulcodes = db.Column(db.String(50))
    harmfuldescriptions = db.Column(db.String(255))
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    rpa = db.Column(db.String(50))
    precinct = db.Column(db.String(50))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    mapped_location = db.Column(db.String(255))
    elevation = db.Column(db.Float)
    closest_hospital = db.Column(db.String(255))
    miles_to_closest_hospital = db.Column(db.Float)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    emergency_needed = db.Column(db.Boolean)
    elevation = db.Column(db.Float)

class Hospital(db.Model):
    long = db.Column(db.Float)
    lat = db.Column(db.Float)
    OBJECTID = db.Column(db.Integer)
    ID = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(255))
    TELEPHONE = db.Column(db.String(50))
    ADDRESS = db.Column(db.String(255))
    ADDRESS2 = db.Column(db.String(255))
    CITY = db.Column(db.String(100))
    STATE = db.Column(db.String(50))
    ZIP = db.Column(db.String(20))
    ZIPP4 = db.Column(db.String(20))
    COUNTY = db.Column(db.String(100))
    FIPS = db.Column(db.String(50))
    DIRECTIONS = db.Column(db.String(255))
    NAICSDESCR = db.Column(db.String(255))

#Redacted
px.set_mapbox_access_token('')
token = ''

def find_closest_hospital(day_input):
	day = pd.to_datetime(day_input).date()
	accidents = Accidents.query.filter(func.date(Accidents.date) == day).all()
	if any(accident.closest_hospital is None for accident in accidents):
		hospitals = Hospital.query.all()
		hospital_locations = [(hospital.lat, hospital.long) for hospital in hospitals]
		hospital_names = [hospital.name for hospital in hospitals]

		for accident in accidents:
		    incident_location = (accident.lat, accident.long)
		    distances = [geodesic(incident_location, hospital_location).miles for hospital_location in hospital_locations]
		    min_distance_index = distances.index(min(distances))
		    closest_hospital = hospital_names[min_distance_index]
		    miles_to_closest_hospital = distances[min_distance_index]
		    accident.closest_hospital = closest_hospital
		    accident.miles_to_closest_hospital = miles_to_closest_hospital

		db.session.commit()

		return accidents
	else:
		return accidents



def map_accidents_for_day(day_input):
	day_data = find_closest_hospital(day_input)
	if day_data:
	    accident_hover_info = []
	    for accident in day_data:
                hover_text = f"<b>Accident Number:</b> {accident.accident_number}<br>"
                hover_text += f"<b>Time:</b> {accident.time.strftime('%I:%M %p')}<br>"
                hover_text += f"<b>Emergency Needed:</b> {accident.emergency_needed}<br>"
                hover_text += f"<b>Collision Type:</b> {accident.collision_type_description}<br>"
                hover_text += f"<b>Weather:</b> {accident.weather_description}<br>"
                hover_text += f"<b>Closest Hospital:</b> {accident.closest_hospital}<br>"
                hover_text += f"<b>Miles to Closest Hospital:</b> {accident.miles_to_closest_hospital}<br>"
                hover_text += f"<b>Elevation:</b> {accident.elevation}<br>"
                accident_hover_info.append(hover_text)
	    closest_hospitals = {accident.closest_hospital for accident in day_data if accident.closest_hospital}
	    hospitals = (
        Hospital.query
        .filter(Hospital.name.in_(closest_hospitals))
        .distinct(Hospital.name)
        .all()
        )
	    fig = go.Figure()
	    fig.add_trace(
			go.Scattermapbox(
                lat=[accident.lat for accident in day_data],
                lon=[accident.long for accident in day_data],
				mode='markers',
				marker=dict(
					size=15,
					symbol='car',  # Use a road accident icon
					color='red',
					allowoverlap=True
				),
				hoverinfo='text',
				hovertext=accident_hover_info,
				text=[accident.accident_number for accident in day_data],
				textposition="bottom right"
			)
		)
	    fig.add_trace(
			go.Scattermapbox(
				lat=[hospital.lat for hospital in hospitals],
                lon=[hospital.long for hospital in hospitals],
				mode='markers',
				marker=dict(
					size=25,
					symbol='hospital',  # Use a hospital icon
					color='blue',
					allowoverlap=True
				),
				hoverinfo='text',
				hovertext=[hospital.name for hospital in hospitals],
                text=[hospital.name for hospital in hospitals],
				textposition="bottom right",
			)
		)
	    fig.update_layout(
			hovermode='closest',
			hoverlabel=dict(
				bgcolor="white",
				font_size=12,
				font_family="Rockwell",
				namelength = 0
			),
			mapbox=dict(
				accesstoken=token,
				style="outdoors",
				center=dict(lat=36.1627, lon=-86.7816),
				zoom=10
			),
			height=750,
			width=1050,
			autosize = True,
			margin = dict(l=0, r=0, t=0, b=0),
			showlegend=False
		)
	    return fig.to_html()
	else:
		return f"No accidents recorded with hospital information on {day_input}."


def convert_date_to_full_day_name(user_input_day):
    date_object = datetime.strptime(user_input_day, "%Y-%m-%d")
    full_day_name = date_object.strftime("%B %d, %Y")
    return full_day_name

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/mapping', methods=['GET', 'POST'])
def mapping():
	if request.method == 'POST':
		user_input_day = request.form['user_input_day']
		plot_html = map_accidents_for_day(user_input_day) 
		return render_template('mapping.html', plot=plot_html, day = convert_date_to_full_day_name(user_input_day))
	else:
		return render_template('mapping.html', plot=None, day = None)

if __name__ == "__main__":
	app.run()
