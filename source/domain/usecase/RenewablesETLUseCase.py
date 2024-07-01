import asyncio
import logging
from datetime import datetime, timedelta, timezone
from enum import Enum
from dateutil import parser


class FetchSolarAndWindDataUseCase:

    def __init__(self, solar_repository, wind_repository):
        self.solar_repo = solar_repository
        self.wind_repo = wind_repository

    class RENEWABLE(Enum):
        SOLAR = 1
        WIND = 2

    async def execute(self):
        dates = self._get_week_dates()

        renewable_tasks = [
            self._handle_solar_data(dates),
            self._handle_wind_data(dates)
        ]
        await asyncio.gather(*renewable_tasks)

    async def _handle_wind_data(self, dates):
        data = await self._fetch_data_for_period(dates, self.RENEWABLE.WIND)
        print(data)
        transformed_data = self._process_and_transform_data(data)
        self.wind_repo.save_transformed_data(transformed_data)

    async def _handle_solar_data(self, dates):
        data = await self._fetch_data_for_period(dates, self.RENEWABLE.SOLAR)
        transformed_data = self._process_and_transform_data(data)
        self.solar_repo.save_transformed_data(transformed_data)

    def _get_week_dates(self):
        """Calculate the dates of the last full week ending on Saturday."""
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)
        start_of_week = last_saturday - timedelta(days=6)
        dates = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        return dates

    async def _fetch_data_for_period(self, dates, renewable=RENEWABLE.SOLAR):
        """Fetch data for each date and renewable type."""
        # tasks = [asyncio.create_task(self.solar_repo.fetch_solar_data(date)) for date in dates]
        # return await asyncio.gather(*tasks, return_exceptions=True)
        results = []
        for date in dates:
            try:
                if renewable == self.RENEWABLE.SOLAR:
                    result = await self.solar_repo.fetch_solar_data(date)
                else:
                    result = await self.wind_repo.fetch_wind_data(date)
                for record in result:
                    results.append(record)
            except Exception as e:
                logging.error(f"Exception when fetching data on {date}: {e}")
        return results

    def _process_and_transform_data(self, data, timestamp_key='Naive_Timestamp ', new_key='Timestamp_UTC'):
        for record in data:
            try:
                if timestamp_key in record:
                    transformed_timestamp = self._transform_timestamp(record[timestamp_key])
                    record[new_key] = transformed_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
                    del record[timestamp_key]
            except Exception as e:
                logging.error(f"Failed to transform data for record {record}. Error: {str(e)}")
        return data

    def _transform_timestamp(self, timestamp):
        try:
            if isinstance(timestamp, str):
                return parser.parse(timestamp).astimezone(timezone.utc)
            elif isinstance(timestamp, (int, float)):  # Unix timestamp in milliseconds
                return datetime.fromtimestamp(timestamp / 1000, timezone.utc)
            else:
                raise TypeError(f"Unsupported timestamp type: {type(timestamp)}")
        except Exception as e:
            logging.error(f"Error transforming timestamp {timestamp}: {str(e)}")
