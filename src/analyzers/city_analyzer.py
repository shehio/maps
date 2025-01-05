from .base_analyzer import BaseAnalyzer
import pandas as pd

class CityAnalyzer(BaseAnalyzer):
    def analyze(self) -> None:
        """Analyze patterns between different cities."""
        print("\nCity-based Analysis:")
        print("=" * 50)
        
        # Basic station analysis
        print("\nTop Start Stations:")
        print(self.df['start_station_name'].value_counts().head())
        
        print("\nTop End Stations:")
        print(self.df['end_station_name'].value_counts().head()) 