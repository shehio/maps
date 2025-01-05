from pathlib import Path
from data_loader import CitibikeDataLoader
from analyzers.trip_analyzer import TripAnalyzer
from analyzers.spatial_analyzer import SpatialAnalyzer
from analyzers.city_analyzer import CityAnalyzer
from analyzers.route_analyzer import RouteAnalyzer
from visualizers.h3_visualizer import H3Visualizer

def main():
    # Initialize paths
    data_path = Path(__file__).parent.parent / 'data' / 'JC-202501-citibike-tripdata.csv'
    
    try:
        # Load data
        print("Loading and processing data...")
        loader = CitibikeDataLoader(data_path)
        df = loader.load()
        
        # Run analyses
        print("\nAnalyzing Citibike data for January 2025...")
        
        analyzers = [
            TripAnalyzer(df),
            SpatialAnalyzer(df),
            CityAnalyzer(df),
            RouteAnalyzer(df)
        ]
        
        for analyzer in analyzers:
            analyzer.analyze()
        
        # Create visualizations
        visualizer = H3Visualizer(df)
        visualizer.create_visualizations()
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 