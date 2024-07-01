import os
import pandas as pd
import logging
from abc import ABC, abstractmethod


class IRenewableRepository(ABC):
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)

    @abstractmethod
    async def fetch_renewable(self, date):
        pass

    @abstractmethod
    def save_transformed_data(self, data):
        pass

    def save_data_to_file(self, data, filename, columns_order=None):
        if columns_order is None:
            columns_order = ['timestamp_utc', 'variable', 'value', 'last_modified_utc']
        file_path = os.path.join(self.output_dir, filename)

        try:
            df = pd.DataFrame(data)
            df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]

            if columns_order:
                df = df[columns_order]

            df.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save data to {file_path}. Error: {str(e)}")