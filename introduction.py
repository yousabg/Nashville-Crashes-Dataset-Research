import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    data = pd.read_csv("nashville_data.csv")
    data['date_and_time'] = pd.to_datetime(data['date_and_time'])
    data['date'] = data['date_and_time'].dt.date
    data['time'] = data['date_and_time'].dt.time
    data.drop('date_and_time', axis=1, inplace=True)
    data['date'] = data['date'].astype(str)
    data['date'] = pd.to_datetime(data['date'])
    data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.time
    mask = data['time'] != pd.to_datetime("00:00:00").time()
    data = data[mask]
    data['hour'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour
    hourly_accidents = data.groupby('hour').size().reset_index(name='accidents_per_hour')
    total_accidents = data.shape[0]
    hourly_accidents['percentage_of_yearly_accidents'] = (hourly_accidents['accidents_per_hour'] / total_accidents) * 100
    hourly_accidents_sorted = hourly_accidents.sort_values(by='hour')
    hourly_accidents_sorted['accidents_per_hour'] = hourly_accidents_sorted['accidents_per_hour'].astype(str)
    for i in range(len(hourly_accidents_sorted["hour"])):
        hour = hourly_accidents_sorted["hour"][i]
        hour_int = int(hour)
        if hour_int == 0:
            hour_12 = "12 AM"
        elif hour_int < 12:
            hour_12 = str(hour_int) + " AM"
        elif hour_int == 12:
            hour_12 = "12 PM"
        else:
            val = hour_int - 12
            hour_12 = str(val) + " PM"

        hourly_accidents_sorted["hour"][i] = hour_12
    hourly_accidents_sorted['accidents_per_hour'] = pd.to_numeric(hourly_accidents_sorted['accidents_per_hour'])
    print(sum(hourly_accidents_sorted["accidents_per_hour"]))
    unique_days = data['date'].nunique()
    print(unique_days)
    hourly_accidents_sorted["average per hour"] = hourly_accidents_sorted["accidents_per_hour"]/unique_days
    print(hourly_accidents_sorted)
    total_accidents = len(data)
    average_accidents_per_day = total_accidents / unique_days
    print(average_accidents_per_day)

    plt.figure(figsize=(20, 15))
    sns.set_style("whitegrid")
    sns.lineplot(x='hour', y='average per hour', data=hourly_accidents_sorted, linewidth=3, color='skyblue')
    plt.title('Accidents per Hour of the Day', fontsize=24, fontweight='bold')
    plt.xlabel('Hour', fontsize=20, fontweight='bold')
    plt.ylabel('Average Accidents', fontsize=20, fontweight='bold')
    plt.xticks(rotation=45, fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=25)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

    plt.savefig('accidents_per_hour.png', dpi=300)

#insert pic here


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyhigh import get_elevation
from scipy.stats import norm as norm



def parse_mapped_location(location_str):
    lon, lat = location_str.replace('POINT (', '').replace(')', '').split()
    return (float(lat), float(lon))
if __name__ == "__main__":
    data = pd.read_csv("nashville_data.csv")
    data = data.dropna(subset=['mapped_location'])
    data["location_tuple"] = data["mapped_location"].apply(parse_mapped_location)
    data["elevation"] = data["location_tuple"].apply(lambda loc: get_elevation(loc[0], loc[1]))
    filename = 'nashville_data_2.csv'
    data.to_csv(filename, index=False)

    df = pd.read_csv("nashville_data_2.csv")
    avg_elevation_nashville = 604/3.281 #According to https://en-us.topographic-map.com/map-z5l4s/Nashville-Davidson/?center=36.14675%2C-86.79457&zoom=12
    min_elevation_nashville = 358/3.281
    max_elevation_nashville = 1129/3.281
    standard_deviation_nashville = (max_elevation_nashville-min_elevation_nashville)/4 #https://www.thoughtco.com/range-rule-for-standard-deviation-3126231

    average_elevation_accidents = np.mean(df["elevation"])
    stan_dev_accidents = np.std(df['elevation'])
    a = 0.05
    random_variables = norm.rvs(loc=average_elevation_accidents, scale=stan_dev_accidents, size=10000)

    plt.figure(figsize=(15, 15))

    plt.hist(random_variables, edgecolor='black', color='skyblue')

    plt.title('Distribution of Accident Elevations', fontsize=25, fontweight='bold')
    plt.xlabel('Elevation (feet)', fontsize=20, fontweight='bold')
    plt.ylabel('Frequency', fontsize=20, fontweight='bold')

    plt.axvline(avg_elevation_nashville, color='blue', linewidth=2, linestyle='--',
                label='Average Elevation of Nashville')

    plt.legend(fontsize=12)

    p_value = np.sum(random_variables >= avg_elevation_nashville) / len(random_variables)
    print("P-value:", p_value)

    plt.tight_layout()
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    plt.savefig('elevation_distribution.png', dpi=300)

#inset pic here

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_dataframe(filename, **kwargs):
    pickle_filename = f"{filename}.pkl"
    if os.path.exists(pickle_filename):
        print(f"Loading from cache: {pickle_filename}")
        return pd.read_pickle(pickle_filename)
    else:
        df = pd.read_csv(filename, **kwargs)
        df.to_pickle(pickle_filename)
        return df

if __name__ == '__main__':
    accidents_df = pd.read_csv("accident.csv", encoding='windows-1252')
    persons_df = pd.read_csv("person.csv")
    vehicle_df = pd.read_csv("vehicle.csv", encoding='windows-1252')
    merged_df = pd.merge(accidents_df, persons_df, on='ST_CASE')
    df = pd.merge(merged_df, vehicle_df, on='ST_CASE')
    combined_df = pd.read_csv("combined.csv")
    accidents_df = load_dataframe("accident.csv", encoding='windows-1252')
    persons_df = load_dataframe("person.csv")
    vehicle_df = load_dataframe("vehicle.csv", encoding='windows-1252')
    combined_df = load_dataframe("combined.csv")


    drivers = combined_df[combined_df["PER_NO"] == 1]
    drunk_drivers = combined_df[combined_df["DR_DRINK"] == 1]
    drunk_drivers = drunk_drivers[combined_df["YEAR"] >= 2018]
    drunk_drivers = drunk_drivers[~drunk_drivers['AGE'].isin([0, 998, 999])]
    drunk_drivers = drunk_drivers[~drunk_drivers['TRAV_SP'].isin([998, 999])]
    drunk_drivers.loc[drunk_drivers['TRAV_SP'] == 997, 'TRAV_SP'] = 151
    drunk_drivers = drunk_drivers[~drunk_drivers["VSPD_LIM"].isin([98, 99])]
    drunk_drivers = drunk_drivers[drunk_drivers['TRAV_SP'] > drunk_drivers['VSPD_LIM']]
    plt.figure(figsize=(12, 8))

    male_data = drunk_drivers[drunk_drivers['SEX'] == 1]
    female_data = drunk_drivers[drunk_drivers['SEX'] == 2]
    print(len(male_data))
    print(len(female_data))
    sns.kdeplot(data=female_data, x="AGE", y="TRAV_SP", fill=True, cmap="Reds", label="FEMALE", alpha = 0.5)
    sns.kdeplot(data=male_data, x="AGE", y="TRAV_SP", fill=True, cmap="Blues", label="MALE", alpha = 0.5)
    plt.legend()

    plt.xlabel('Age', fontsize=16, fontweight='bold', color='black')
    plt.ylabel('Travel Speed', fontsize=16, fontweight='bold', color='black')
    plt.title('Density Plot of Age vs. Travel Speed', fontsize=20, fontweight='bold', color='black')
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('age_vs_travel.png', dpi=300)

#insert pic here


