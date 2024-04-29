#used for making databases in the flask app

import csv
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Redacted
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",
    hostname="",
    databasename="",
)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Accident(Base):
    __tablename__ = 'accidents'

    id = Column(Integer, primary_key=True)
    accident_number = Column(String(50))
    number_of_motor_vehicles = Column(Integer)
    number_of_injuries = Column(Integer)
    number_of_fatalities = Column(Integer)
    property_damage = Column(String(50))
    hit_and_run = Column(String(50))
    reporting_officer = Column(String(50))
    collision_type = Column(String(50))
    collision_type_description = Column(String(255))
    weather = Column(String(50))
    weather_description = Column(String(255))
    illuaccidemination = Column(String(50))
    illumination_description = Column(String(255))
    harmfulcodes = Column(String(50))
    harmfuldescriptions = Column(String(255))
    street_address = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    rpa = Column(String(50))
    precinct = Column(String(50))
    lat = Column(Float)
    long = Column(Float)
    mapped_location = Column(String(255))
    elevation = Column(Float)
    closest_hospital = Column(String(255))
    miles_to_closest_hospital = Column(Float)
    date = Column(Date)
    time = Column(Time)
    emergency_needed = Column(Boolean)

def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%y')
    return date_obj.date()

def add_rows_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'date' in row:
                row['date'] = convert_date(row['date'])
            if 'emergency_needed' in row:
                row['emergency_needed'] = row['emergency_needed'].lower() == 'true'
            row['closest_hospital'] = None
            row['miles_to_closest_hospital'] = None
            accident = Accident(**row)
            session.add(accident)
        session.commit()

if __name__ == '__main__':
    csv_file_path = '/home/gyousab2/mysite/nashville_data_new.csv'
    add_rows_from_csv(csv_file_path)
    print("Rows added successfully!")
