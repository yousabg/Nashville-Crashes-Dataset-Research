#This code was used to receive new data

import os
import pandas as pd
import ssl
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import Flask
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import sys
sys.path.insert(0, '/home/gyousab2/mysite/pyhigh')
from pyhigh import get_elevation


app = Flask(__name__)
app.config["DEBUG"] = True

# Redcated data
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
    accident_number = db.Column(db.String(50), unique=True)
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
    location_tuple = db.Column(db.String(255))
    elevation = db.Column(db.Float)
    closest_hospital = db.Column(db.String(255))
    miles_to_closest_hospital = db.Column(db.Float)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    emergency_needed = db.Column(db.Boolean)


def parse_mapped_location(location_str):
    lon, lat = location_str.replace('POINT (', '').replace(')', '').split()
    return (float(lat), float(lon))



def download_data(start_date):
    base_url = "https://data.nashville.gov/resource/6v6w-hpcw.csv"
    rows_per_request = 1000
    offset = 0
    dataframes = []

    while True:
        url = f"{base_url}?$limit={rows_per_request}&$offset={offset}"
        df = pd.read_csv(url)

        if df.empty:
            break

        df['date'] = pd.to_datetime(df['date_and_time']).dt.date
        df['time'] = pd.to_datetime(df['date_and_time']).dt.time
        df['emergency_needed'] = (df['number_of_injuries'] > 0) | (df['number_of_fatalities'] > 0)
        df['location_tuple'] = df['mapped_location'].apply(parse_mapped_location)
        df["elevation"] = df["location_tuple"].apply(lambda loc: get_elevation(loc[0], loc[1]))

        df = df[df['date'] > start_date]

        dataframes.append(df)
        offset += rows_per_request

    full_data = pd.concat(dataframes, ignore_index=True)
    full_data.to_csv('nashville_data.csv', index=False)
    return full_data


def get_latest_date_in_database():
    latest_date = db.session.query(func.max(Accidents.date)).scalar()
    print(latest_date.strftime('%Y-%m-%d'))
    return latest_date


def main():
    if not os.path.exists('nashville_data.csv'):
        print("Downloading data...")
        latest_date = get_latest_date_in_database()
        data = download_data(start_date=latest_date)
    else:
        print("Loading data from file...")
        data = pd.read_csv('nashville_data.csv')

    for index, row in data.iterrows():
        new_accident = Accidents(
            accident_number=row['accident_number'],
            number_of_motor_vehicles=row['number_of_motor_vehicles'],
            number_of_injuries=row['number_of_injuries'],
            number_of_fatalities=row['number_of_fatalities'],
            property_damage=row['property_damage'],
            hit_and_run=row['hit_and_run'],
            reporting_officer=row['reporting_officer'],
            collision_type=row['collision_type'],
            collision_type_description=row['collision_type_description'],
            weather=row['weather'],
            weather_description=row['weather_description'],
            illuaccidemination=row['illuaccidemination'],
            illumination_description=row['illumination_description'],
            harmfulcodes=row['harmfulcodes'],
            harmfuldescriptions=row['harmfuldescriptions'],
            street_address=row['street_address'],
            city=row['city'],
            state=row['state'],
            zip_code=row['zip_code'],
            rpa=row['rpa'],
            precinct=row['precinct'],
            lat=row['lat'],
            long=row['long'],
            mapped_location=str(row['mapped_location']),
            date=row['date'],
            time=row['time'],
            emergency_needed=row['emergency_needed'],
            closest_hospital=None,
            miles_to_closest_hospital=None,
            elevation=None  # Add elevation if retrieved
        )

        try:
            db.session.add(new_accident)
            db.session.commit()
        except IntegrityError:
            # Handle duplicate entry (e.g., accident_number is unique)
            db.session.rollback()

    print("Data insertion complete!")


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    main()
