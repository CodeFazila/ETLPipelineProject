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
    mock.fetch_wind_data = AsyncMock(return_value=[
        {'Naive_Timestamp ': '2024-06-23 00:00:00+00:00', ' Variable': 282, 'value': 13.251143780434838,
         'Last Modified utc': '2024-06-23 00:00:00+00:00'}])
    mock.save_transformed_data = AsyncMock()
    return mock


@pytest.fixture
def use_case(solar_repo, wind_repo):
    return RenewablesETLUseCase(solar_repo, wind_repo)


def test_solar_process_and_transform_data_pass(use_case):
    raw_data = [{"Naive_Timestamp ": 1719100800000, " Variable": 973, "value": -33.9277882476,
                 "Last Modified utc": 1719100800000}]
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.SOLAR)[1]
    assert processed_data[0]['Timestamp_UTC'] == '2024-06-23 00:00:00 UTC'


def test_empty_solar_process_and_transform_data_pass(use_case):
    raw_data = []
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.SOLAR)
    assert processed_data == (False, 0)


def test_wrong_solar_data_process_and_transform_data_pass(use_case):
    raw_data = [{'hello': 'world'}]
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.SOLAR)
    assert processed_data == (False, 0)


def test_wrong_correct_solar_data_process_and_transform_data_pass(use_case):
    raw_data = [{'hello': 'world'}, {"Naive_Timestamp ": 1719100800000, " Variable": 973, "value": -33.9277882476,
                 "Last Modified utc": 1719100800000}]
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.SOLAR)
    assert processed_data == (False, 0)


def test_wind_process_and_transform_data_pass(use_case):
    raw_data = [{'Naive_Timestamp ': '2024-06-23 00:00:00+00:00', ' Variable': 282,
                 'value': 13.251143780434838, 'Last Modified utc': '2024-06-23 00:00:00+00:00'}]
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.WIND)[1]
    assert processed_data[0]['Timestamp_UTC'] == '2024-06-23 00:00:00 UTC'


def test_empty_wind_process_and_transform_data_pass(use_case):
    raw_data = []
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.WIND)
    assert processed_data == (False, 0)


def test_wrong_wind_data_process_and_transform_data_pass(use_case):
    raw_data = [{'hello': 'world'}]
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.WIND)
    assert processed_data == (False, 0)


def test_wrong_correct_wind_data_process_and_transform_data_pass(use_case):
    raw_data = [{'hello': 'world'}, {'Naive_Timestamp ': '2024-06-23 00:00:00+00:00', ' Variable': 282,
                 'value': 13.251143780434838, 'Last Modified utc': '2024-06-23 00:00:00+00:00'}]
    processed_data = use_case._process_and_transform_data(raw_data, RenewablesETLUseCase.RENEWABLE.WIND)
    assert processed_data == (False, 0)

def test_get_week_dates_pass(use_case):
    expected_dates = ['2024-06-23', '2024-06-24', '2024-06-25', '2024-06-26', '2024-06-27', '2024-06-28', '2024-06-29']
    calculated_dates = use_case._get_week_dates()
    assert expected_dates == calculated_dates, f"Expected dates {expected_dates} do not match calculated dates {calculated_dates}"
