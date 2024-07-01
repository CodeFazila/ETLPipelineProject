import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone, timedelta
from source.domain.usecase.RenewablesETLUseCase import RenewablesETLUseCase


@pytest.fixture
def solar_repo():
    mock = AsyncMock()
    mock.fetch_solar_data = AsyncMock(return_value=[
        {"Naive_Timestamp ": 1719100800000, " Variable": 973, "value": -33.9277882476,
         "Last Modified utc": 1719100800000}])
    mock.save_transformed_data = AsyncMock()
    return mock


@pytest.fixture
def wind_repo():
    mock = AsyncMock()
    mock.fetch_wind_data = AsyncMock(return_value=[{'Naive_Timestamp ': '2024-06-23 00:00:00+00:00', ' Variable': 282, 'value': 13.251143780434838, 'Last Modified utc': '2024-06-23 00:00:00+00:00'}])
    mock.save_transformed_data = AsyncMock()
    return mock


@pytest.fixture
def use_case(solar_repo, wind_repo):
    return RenewablesETLUseCase(solar_repo, wind_repo)

@pytest.mark.asyncio
async def test_execute(use_case, solar_repo, wind_repo):
    await use_case.execute()

    solar_repo.fetch_solar_data.assert_called()
    wind_repo.fetch_wind_data.assert_called()
    solar_repo.save_transformed_data.assert_called()
    wind_repo.save_transformed_data.assert_called()


@pytest.mark.asyncio
async def test_fetch_data_solar(use_case, solar_repo):
    dates = ["2024-06-25", "2024-06-26"]
    await use_case._fetch_data_for_period(dates, RenewablesETLUseCase.RENEWABLE.SOLAR)
    solar_repo.fetch_solar_data.assert_called_with("2024-06-26")

@pytest.mark.asyncio
async def test_fetch_data_wind(use_case, wind_repo):
    dates = ["2023-06-01", "2023-06-02"]
    await use_case._fetch_data_for_period(dates, RenewablesETLUseCase.RENEWABLE.WIND)
    wind_repo.fetch_wind_data.assert_called_with("2023-06-02")

def test_process_and_transform_data(use_case):
    raw_data = [{'Naive_Timestamp ': '2023-06-01T12:00:00Z'}]
    processed_data = use_case._process_and_transform_data(raw_data)
    assert processed_data[0]['Timestamp_UTC'] == '2023-06-01 12:00:00 UTC'

def test_get_week_dates(use_case):
    expected_dates = ['2024-06-23', '2024-06-24', '2024-06-25', '2024-06-26', '2024-06-27', '2024-06-28', '2024-06-29']
    calculated_dates = use_case._get_week_dates()
    assert expected_dates == calculated_dates, f"Expected dates {expected_dates} do not match calculated dates {calculated_dates}"

# Testing error handling
@pytest.mark.asyncio
async def test_fetch_data_solar_api_failure(use_case, solar_repo):
    solar_repo.fetch_solar_data.side_effect = Exception("API Failure")
    with pytest.raises(Exception, match="API Failure"):
        await use_case._fetch_data_for_period(["2024-06-25"], RenewablesETLUseCase.RENEWABLE.SOLAR)

# Testing edge cases with empty data
@pytest.mark.asyncio
async def test_fetch_data_solar_empty_data(use_case, solar_repo):
    solar_repo.fetch_solar_data.return_value = []
    data = await use_case._fetch_data_for_period(["2024-06-25"], RenewablesETLUseCase.RENEWABLE.SOLAR)
    assert data == [], "Expected empty data list when API returns no data"

# Testing data type validation
def test_transform_data_type_validation(use_case):
    raw_data = [{'Naive_Timestamp ': '2023-06-01T12:00:00Z', 'value': 'not_a_number'}]
    processed_data = use_case._process_and_transform_data(raw_data)
    assert isinstance(processed_data[0]['value'], float), "Value should be converted to float type"

# Testing handling of multiple concurrent fetches
@pytest.mark.asyncio
async def test_concurrent_data_fetches(use_case):
    with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
        await use_case.execute()
        assert mock_gather.called, "asyncio.gather should be called to handle concurrent fetching"