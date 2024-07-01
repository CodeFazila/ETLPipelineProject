import asyncio
import logging

from source.data.repository.renewable_repository.solar_repository.SolarRepository import SolarRepository
from source.data.repository.renewable_repository.wind_repository.WindRepository import WindRepository
from source.domain.usecase.RenewablesETLUseCase import FetchSolarAndWindDataUseCase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    try:
        use_case = FetchSolarAndWindDataUseCase(SolarRepository(), WindRepository())
        asyncio.run(use_case.execute())
    except Exception as e:
        logging.error("An error occurred during execution: %s", e)
        raise


if __name__ == '__main__':
    main()
