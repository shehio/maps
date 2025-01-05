from .base_analyzer import BaseAnalyzer
import pandas as pd

class SpatialAnalyzer(BaseAnalyzer):
    def analyze(self) -> None:
        """Analyze spatial patterns in Citibike trips."""
        self.df['station_pair'] = self.df['start_station_name'] + ' → ' + self.df['end_station_name']
        popular_routes = self.df['station_pair'].value_counts().head(10)
        print("\nMost Popular Routes:")
        print("=" * 50)
        print(popular_routes) 