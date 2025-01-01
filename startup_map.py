import webview
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load the dataset
dataset = pd.read_csv('startups_with_coordinates.csv')

# Define European countries
european_countries = [
    "Sweden", "United Kingdom", "Germany", "Netherlands", "Belgium", "Lithuania",
    "Estonia", "France", "Austria", "Ireland", "Switzerland", "Spain",
    "Luxembourg", "Finland", "Denmark", "Norway", "Czech Republic", "Croatia"
]

# Filter datasets by region
dataset_USA = dataset[dataset["Country"] == "United States"]
dataset_China = dataset[dataset["Country"] == "China"]
dataset_EU = dataset[dataset["Country"].isin(european_countries)]

# Function to add Circle Markers within Clusters
def add_circle_markers_to_cluster(data, color, cluster_obj, radius=5):
    for _, row in data.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=folium.Popup(
                    f"Company: {row['Company']}<br>City: {row['City']}<br>Country: {row['Country']}<br>Valuation ($B): {row['Valuation ($B)']}",
                    max_width=300
                )
            ).add_to(cluster_obj)

# Initialize the map
startup_map = folium.Map(location=[20, 0], zoom_start=2)

# Initialize Marker Clusters for each region
marker_cluster_usa = MarkerCluster(name="USA Startups").add_to(startup_map)
marker_cluster_china = MarkerCluster(name="China Startups").add_to(startup_map)
marker_cluster_eu = MarkerCluster(name="Europe Startups").add_to(startup_map)

# Add Circle Markers to clusters
add_circle_markers_to_cluster(dataset_USA, "blue", marker_cluster_usa, radius=7)
add_circle_markers_to_cluster(dataset_China, "red", marker_cluster_china, radius=7)
add_circle_markers_to_cluster(dataset_EU, "green", marker_cluster_eu, radius=6)

# Add Layer Control to toggle clusters
folium.LayerControl().add_to(startup_map)

# Save the map to an HTML file
map_file = "circle_marker_cluster_map.html"
startup_map.save(map_file)

# Open the map in a Tkinter window
webview.create_window("Carte des Startups", map_file)
webview.start()