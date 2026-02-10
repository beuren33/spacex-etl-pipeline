import pytest
from src.extract.spacex_extractor import SpaceXExtractor
import requests


def test_get_data_success(mocker):

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Test Launch"}]

    mocker.patch("requests.get", return_value=mock_response)

    extractor = SpaceXExtractor("http://fakeapi.com", "v4", 10, 1)
    data = extractor.get_data("/launches")

    assert data is not None
    assert len(data) == 1
    assert data[0]["name"] == "Test Launch"


def test_get_data_failure(mocker):
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException)

    extractor = SpaceXExtractor("http://fakeapi.com", "v4", 10, 2)
    data = extractor.get_data("/launches")

    assert data is None
