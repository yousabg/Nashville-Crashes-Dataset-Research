#part 1:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def prepare_data(filepath):
    data = pd.read_csv(filepath)
    data['date_and_time'] = pd.to_datetime(data['date_and_time'])
    data['hour'] = data['date_and_time'].dt.hour
    data = data[data['date_and_time'].dt.time != pd.to_datetime("00:00:00").time()]
    return data

def analyze_hourly_accidents(data):
    hourly_accidents = data.groupby('hour').size().reset_index(name='accidents_per_hour')
    total_accidents = data.shape[0]
    hourly_accidents['percentage'] = (hourly_accidents['accidents_per_hour'] / total_accidents) * 100
    return hourly_accidents

def plot_hourly_accidents(hourly_accidents):
    plt.figure(figsize=(20, 15))
    sns.set_style("whitegrid")
    sns.lineplot(x='hour', y='percentage', data=hourly_accidents, linewidth=3, color='skyblue')
    plt.title('Percentage of Yearly Accidents per Hour', fontsize=24, fontweight='bold')
    plt.xlabel('Hour of the Day', fontsize=20, fontweight='bold')
    plt.ylabel('Percentage of Accidents', fontsize=20, fontweight='bold')
    plt.xticks(range(0, 24), [f'{h}:00' for h in range(24)], rotation=45, fontsize=16)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('pictures/accidents_per_hour.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    data = prepare_data("nashville_data.csv")
    hourly_accidents = analyze_hourly_accidents(data)
    plot_hourly_accidents(hourly_accidents)

#part 2:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def load_and_process_elevation_data(filepath):
    df = pd.read_csv(filepath)
    df['elevation'] = df['mapped_location'].apply(lambda loc: get_elevation(*parse_mapped_location(loc)))
    return df

def plot_elevation_distribution(data, avg_elevation_nashville):
    random_variables = norm.rvs(loc=data['elevation'].mean(), scale=data['elevation'].std(), size=10000)
    plt.figure(figsize=(15, 10))
    plt.hist(random_variables, bins=30, edgecolor='black', color='skyblue')
    plt.axvline(avg_elevation_nashville, color='blue', linewidth=2, linestyle='--', label='Avg. Elevation of Nashville')
    plt.title('Distribution of Accident Elevations', fontsize=25, fontweight='bold')
    plt.xlabel('Elevation (feet)', fontsize=20, fontweight='bold')
    plt.ylabel('Frequency', fontsize=20, fontweight='bold')
    plt.legend(fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('pictures/elevation_distribution.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    data = load_and_process_elevation_data("nashville_data_2.csv")
    avg_elevation_nashville = 604 / 3.281  # meters to feet conversion for Nashville
    plot_elevation_distribution(data, avg_elevation_nashville)

#part 3:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(*filepaths):
    return [pd.read_csv(file) for file in filepaths]

def merge_datasets(*dfs):
    return dfs[0].merge(dfs[1], on='ST_CASE').merge(dfs[2], on='ST_CASE')

def plot_density(data):
    plt.figure(figsize=(12, 8))
    sns.kdeplot(data=data[data['SEX'] == 2], x="AGE", y="TRAV_SP", fill=True, cmap="Reds", label="FEMALE", alpha=0.5)
    sns.kdeplot(data=data[data['SEX'] == 1], x="AGE", y="TRAV_SP", fill=True, cmap="Blues", label="MALE", alpha=0.5)
    plt.legend()
    plt.xlabel('Age', fontsize=16, fontweight='bold')
    plt.ylabel('Travel Speed (mph)', fontsize=16, fontweight='bold')
    plt.title('Density Plot of Age vs. Travel Speed', fontsize=20, fontweight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig('pictures/age_vs_travel.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    accident_df, person_df, vehicle_df = load_data("accident.csv", "person.csv", "vehicle.csv")
    combined_df = merge_datasets(accident_df, person_df, vehicle_df)
    plot_density(combined_df)


