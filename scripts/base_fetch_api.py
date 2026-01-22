from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime
import requests

class BaseFetchAPI(ABC):
    """Base class for all API scrapers"""

    def __init__(self, url: str, last_updated: str):
        self.url = url
        self.last_updated = datetime.strptime(last_updated, "%Y-%m-%d")

    def fetch_api(self) -> pd.DataFrame:
        """Fetch data from the URL"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching data from {self.url}: {e}")
            return pd.DataFrame()

    @abstractmethod
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Subclasses implement their own cleaning logic"""
        pass

    def run(self) -> pd.DataFrame:
        """Fetch + clean + filter new data"""
        try:
            df = self.fetch_api()
            if df.empty:
                return df

            df = self.clean(df)

            # Convert Date column to datetime for proper filtering and sorting
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df[df["Date"] > self.last_updated]
            df = df.sort_values(by="Date")

            return df

        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
            return pd.DataFrame()
