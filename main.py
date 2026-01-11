# My first Python project - Weather Dashboard

import requests   # for getting data from internet
import pandas as pd  # for making table of data
import matplotlib.pyplot as plt  # for making graphs
import seaborn as sns  # makes graphs look better

# ---------------------------
# Setting API and cities
# ---------------------------

API_KEY = "Enter your API Key"  # put your API key here
CITIES = ["London", "New York", "Mumbai", "Tokyo", "Dubai", "Sydney", "Paris"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ---------------------------
# Get weather function
# ---------------------------

def get_weather():
    weather_data = []  # empty list to store city weather
    print("Starting to get weather data...")
    
    for city in CITIES:
        print("Getting weather for", city)
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        r = requests.get(BASE_URL, params=params)
        
        if r.status_code == 200:
            data = r.json()
            temp = data['main']['temp']  # temperature
            hum = data['main']['humidity']  # humidity
            weather = data['weather'][0]['main']  # weather condition
            wind = data['wind']['speed']  # wind speed
            
            print(city, "data fetched!")
            
            # add data to list
            weather_data.append({
                "City": city,
                "Temperature": temp,
                "Humidity": hum,
                "Weather": weather,
                "Wind": wind
            })
        else:
            print("Failed to get data for", city)
    
    # convert list to DataFrame
    df = pd.DataFrame(weather_data)
    return df

# ---------------------------
# Make graphs function
# ---------------------------

def make_graphs(df):
    sns.set_theme(style="whitegrid")  # makes plots pretty
    
    print("Making graphs...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("Weather Dashboard", fontsize=20)
    
    # Temperature bar plot
    sns.barplot(ax=axes[0, 0], x="City", y="Temperature", data=df, palette="coolwarm")
    axes[0, 0].set_title("Temperature in Cities")
    
    # Humidity vs Temperature scatter
    sns.scatterplot(ax=axes[0, 1], x="Temperature", y="Humidity", hue="City", size="Wind", data=df, s=100)
    axes[0, 1].set_title("Humidity vs Temperature")
    
    # Wind bar plot
    sns.barplot(ax=axes[1, 0], x="City", y="Wind", data=df, palette="viridis")
    axes[1, 0].set_title("Wind Speed in Cities")
    
    # Weather pie chart
    weather_counts = df["Weather"].value_counts()
    axes[1, 1].pie(weather_counts, labels=weather_counts.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
    axes[1, 1].set_title("Weather Condition")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    plt.savefig("images/weather_plot.png")  # to save image
    print("Dashboard saved!")
    
    plt.show()

# ---------------------------
# MAIN CODE
# ---------------------------

print("Program started...")
weather_df = get_weather()

print("Here is the data we got:")
print(weather_df)

if not weather_df.empty:
    make_graphs(weather_df)
else:
    print("No data to show")
    
print("Program ended.")

