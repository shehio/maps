from .base_analyzer import BaseAnalyzer
import pandas as pd

class TripAnalyzer(BaseAnalyzer):
    def analyze(self) -> None:
        self._analyze_basic_stats()
        self._analyze_membership()
        self._analyze_stations()
        self._analyze_temporal_patterns()
        self._analyze_bike_types()

    def _analyze_basic_stats(self) -> None:
        print("\n1. Basic Trip Statistics:")
        print("=" * 50)
        print(f"Total number of trips: {len(self.df):,}")
        print(f"Average trip duration: {self.df['trip_duration_mins'].mean():.2f} minutes")
        print(f"Median trip duration: {self.df['trip_duration_mins'].median():.2f} minutes")

    def _analyze_membership(self) -> None:
        print("\n2. Membership Analysis:")
        print("=" * 50)
        member_stats = self.df['member_casual'].value_counts()
        print("\nRider Types:")
        print(member_stats)
        print("\nPercentage:")
        print(member_stats / len(self.df) * 100)

    def _analyze_stations(self) -> None:
        print("\n3. Station Analysis:")
        print("=" * 50)
        print("\nTop Start Stations:")
        print(self.df['start_station_name'].value_counts().head())
        print("\nTop End Stations:")
        print(self.df['end_station_name'].value_counts().head())

    def _analyze_temporal_patterns(self) -> None:
        print("\n4. Temporal Patterns:")
        print("=" * 50)
        print("\nHourly Distribution:")
        hourly = self.df['started_at'].dt.hour.value_counts().sort_index()
        print(hourly)
        print("\nDay of Week Distribution:")
        daily = self.df['started_at'].dt.day_name().value_counts()
        print(daily)

    def _analyze_bike_types(self) -> None:
        print("\n5. Bike Type Analysis:")
        print("=" * 50)
        bike_stats = self.df['rideable_type'].value_counts()
        print("\nBike Types:")
        print(bike_stats)
        print("\nPercentage:")
        print(bike_stats / len(self.df) * 100)

    # ... (implement other analysis methods) 