import os
from dotenv import load_dotenv
from io import StringIO
import pandas as pd
import logging
from resources.api_client.ApiClient import ApiClient
from source.data.repository.renewable_repository.Renewable import Renewable

# Load environment variables
load_dotenv()


class WindRepository(Renewable):
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = ApiClient()
        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.wind_endpoint = os.getenv('WIND_ENDPOINT')

    async def fetch_wind_data(self, date='2024-06-28'):
        """
        Fetches wind data for a given date from an external API and returns it as a list of dictionaries.
        """
        url = f"{self.base_url}{date}/{self.wind_endpoint}?api_key={self.api_key}"
        try:
            csv_text = await self.api_client.get(url)
            return pd.read_csv(StringIO(csv_text)).to_dict(orient='records')
        except Exception as e:
            logging.error(f"Failed to fetch or parse wind data: {e}")
        raise

    def save_transformed_data(self, data):
        """
         Saves transformed wind data to a CSV file.
         """
        columns_order = ['timestamp_utc', 'variable', 'value', 'last_modified_utc']
        filename = 'wind_data.csv'
        self.save_data_to_file(data, filename, columns_order)
