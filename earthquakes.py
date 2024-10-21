import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import matplotlib.ticker as mticker

def get_data():
    # Get earthquake information from the USGS Seismic Data API
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"
        }
    )
    data = response.json()
    return data

def get_year(earthquake):
    """ Extract the year of the earthquake event. """
    timestamp = earthquake['properties']['time'] / 1000  # convert to seconds
    date = datetime.utcfromtimestamp(timestamp)
    return date.year

def get_magnitude(earthquake):
    """ Get the magnitude of a single seismic event. """
    return earthquake['properties']['mag']

def calculate_annual_stats(data):
    """ Number of earthquakes and average magnitude by year """
    yearly_counts = defaultdict(int)
    yearly_magnitudes = defaultdict(list)

    for eq in data['features']:
        year = get_year(eq)
        magnitude = get_magnitude(eq)
        if magnitude is not None:  # Exclude data without magnitude
            yearly_counts[year] += 1
            yearly_magnitudes[year].append(magnitude)

    # Calculate the average magnitude for each year
    yearly_avg_magnitude = {
        year: sum(mags) / len(mags) for year, mags in yearly_magnitudes.items()
    }

    return yearly_counts, yearly_avg_magnitude

def plot_earthquake_frequency(yearly_counts):
    """ Plot the number of earthquakes per year. """
    years = sorted(yearly_counts.keys())
    counts = [yearly_counts[year] for year in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, color='tab:blue', label="Earthquake Count")
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.title('Number of Earthquakes Per Year')
    plt.grid(True)

    # Make sure the year axis is an integer
    plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    plt.tight_layout()  # ensures that layouts do not overlap
    plt.show()

def plot_average_magnitude(yearly_avg_magnitude):
    """ Plot the average magnitude of earthquakes for each year. """
    years = sorted(yearly_avg_magnitude.keys())
    avg_magnitudes = [yearly_avg_magnitude[year] for year in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_magnitudes, color='tab:red', label="Average Magnitude")
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.title('Average Earthquake Magnitude Per Year')
    plt.grid(True)

    # Make sure the year axis is an integer
    plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    plt.tight_layout()  # ensures that layouts do not overlap
    plt.show()

# Main function
data = get_data()
yearly_counts, yearly_avg_magnitude = calculate_annual_stats(data)

# Plot two plots
plot_earthquake_frequency(yearly_counts)
plot_average_magnitude(yearly_avg_magnitude)
