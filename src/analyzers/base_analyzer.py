from abc import ABC, abstractmethod
import pandas as pd

class BaseAnalyzer(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def analyze(self) -> None:
        """Base analysis method to be implemented by child classes."""
        pass 