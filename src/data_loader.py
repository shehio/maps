import pandas as pd
from pathlib import Path

class CitibikeDataLoader:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        """Load and preprocess Citibike trip data."""
        try:
            df = pd.read_csv(self.file_path)
            return self._preprocess_data(df)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")

    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data with necessary transformations."""
        # Convert datetime columns
        datetime_cols = ['started_at', 'ended_at']
        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col])
        
        # Calculate trip duration
        df['trip_duration_mins'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
        
        return df 