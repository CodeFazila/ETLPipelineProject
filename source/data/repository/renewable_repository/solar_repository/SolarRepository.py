import os
import json
import logging
from dotenv import load_dotenv
from resources.api_client.ApiClient import ApiClient
from source.data.repository.renewable_repository.Renewable import Renewable

# Load environment variables
load_dotenv()


class SolarRepository(Renewable):
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = ApiClient()
        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.solar_endpoint = os.getenv('SOLAR_ENDPOINT')

    async def fetch_solar_data(self, date):
        """
        Fetches solar data for a given date from an external API.
        """
        url = f"{self.base_url}{date}/{self.solar_endpoint}?api_key={self.api_key}"
        try:
            response = await self.api_client.get(url)
            return json.loads(response)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON from response: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to fetch solar data: {e}")
            raise

    def save_transformed_data(self, data):
        """
         Saves transformed solar data to a CSV file.
         """
        columns_order = ['timestamp_utc', 'variable', 'value', 'last_modified_utc']
        filename = 'solar_data.csv'
        self.save_data_to_file(data, filename, columns_order)
