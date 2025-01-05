from .base_analyzer import BaseAnalyzer
import pandas as pd
import folium
from pathlib import Path
from geopy.distance import geodesic
import numpy as np
import requests
import polyline

class RouteAnalyzer(BaseAnalyzer):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.osrm_url = "http://router.project-osrm.org/route/v1/cycling/{}"

    def analyze(self) -> None:
        """Analyze and visualize the longest route in the Citibike system."""
        # Filter out rows with NaN coordinates
        valid_trips = self.df.dropna(subset=['start_lat', 'start_lng', 'end_lat', 'end_lng'])
        
        # Calculate straight-line distances for valid trips
        valid_trips['trip_distance_km'] = valid_trips.apply(
            lambda row: geodesic(
                (row['start_lat'], row['start_lng']),
                (row['end_lat'], row['end_lng'])
            ).kilometers,
            axis=1
        )
        
        # Find the longest trip
        longest_trip = valid_trips.loc[valid_trips['trip_distance_km'].idxmax()]
        
        # Get OSRM route
        route_coords = self._get_osrm_route(
            start_coords=(longest_trip['start_lng'], longest_trip['start_lat']),
            end_coords=(longest_trip['end_lng'], longest_trip['end_lat'])
        )
        
        print("\nLongest Route Analysis:")
        print("=" * 50)
        print(f"Start Station: {longest_trip['start_station_name']}")
        print(f"End Station: {longest_trip['end_station_name']}")
        print(f"Straight-line Distance: {longest_trip['trip_distance_km']:.2f} km")
        print(f"Actual Route Distance: {route_coords['distance']:.2f} km")
        print(f"Estimated Cycling Time: {route_coords['duration']/60:.1f} minutes")
        print(f"Actual Trip Duration: {longest_trip['trip_duration_mins']:.1f} minutes")
        
        # Create a map visualization
        self._visualize_route(longest_trip, route_coords['geometry'])

    def _get_osrm_route(self, start_coords: tuple, end_coords: tuple) -> dict:
        """Get cycling route from OSRM."""
        coords = f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
        url = self.osrm_url.format(coords)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            route = response.json()['routes'][0]
            return {
                'geometry': polyline.decode(route['geometry']),
                'distance': route['distance'] / 1000,  # Convert to km
                'duration': route['duration']  # In seconds
            }
        except Exception as e:
            print(f"Error getting OSRM route: {e}")
            return {
                'geometry': [(start_coords[1], start_coords[0]), (end_coords[1], end_coords[0])],
                'distance': geodesic(
                    (start_coords[1], start_coords[0]),
                    (end_coords[1], end_coords[0])
                ).kilometers,
                'duration': 0
            }
    
    def _visualize_route(self, trip: pd.Series, route_coords: list) -> None:
        """Create a Folium map showing the actual cycling route."""
        # Create base map centered between start and end points
        center_lat = (trip['start_lat'] + trip['end_lat']) / 2
        center_lng = (trip['start_lng'] + trip['end_lng']) / 2
        
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=12,
            tiles='cartodbpositron'
        )
        
        # Add start marker
        folium.Marker(
            [float(trip['start_lat']), float(trip['start_lng'])],
            popup=f"Start: {trip['start_station_name']}",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)
        
        # Add end marker
        folium.Marker(
            [float(trip['end_lat']), float(trip['end_lng'])],
            popup=f"End: {trip['end_station_name']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
        # Add actual route line
        folium.PolyLine(
            locations=route_coords,
            weight=3,
            color='blue',
            opacity=0.8,
            popup=f"Cycling Route: {trip['trip_distance_km']:.2f} km"
        ).add_to(m)
        
        # Save the map
        output_dir = Path(__file__).parent.parent.parent / 'output'
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / 'longest_route.html'
        m.save(str(output_path))
        print(f"\nLongest route visualization saved to: {output_path}") 