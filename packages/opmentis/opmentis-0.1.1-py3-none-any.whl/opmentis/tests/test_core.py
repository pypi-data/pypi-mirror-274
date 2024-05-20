import pytest
import requests_mock
from opmentis import register_miners, userdata

def test_register_miners_success():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = "http://54.74.133.71/register_user"
    expected_response = f"Miner registered successfully with wallet address: {wallet_address}"

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"success": True, "wallet_address": wallet_address}, status_code=200)
        response = register_miners(wallet_address)
        
        # Assert that the response matches the expected success message
        assert response == expected_response, f"Expected response was '{expected_response}', but got '{response}'"
        
        # Check if the correct data was sent to the server
        assert m.last_request.json() == {"wallet_address": wallet_address}, "The request payload is not correct"

def test_register_miners_duplicate():
    wallet_address = "0x0EDA10bE51C5458E00Af47d16751250ce188aC37"
    endpoint = "http://54.74.133.71/register_user"
    expected_response = {"error": "Unexpected server response: {'message': 'User already exists'}"}

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"message": "User already exists"}, status_code=200)
        response = register_miners(wallet_address)
        
        # Assert that the response matches the expected error message
        assert response == expected_response, f"Expected response was '{expected_response}', but got '{response}'"


def test_register_miners_invalid():
    wallet_address = "0x42C58401622D09827EF8dD33d93Dc"  # Invalid wallet address
    endpoint = "http://54.74.133.71/register_user"
    expected_response = {"error": "Unexpected server response: {'message': 'Invalid wallet address format'}"}

    # Setup mock for an invalid wallet address attempt
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"message": "Invalid wallet address format"}, status_code=200)  # Assuming 400 Bad Request
        response = register_miners(wallet_address)
        
        # Assert that the response matches the expected error message
        assert response == expected_response, f"Expected response was '{expected_response}', but got '{response}'"



def test_register_miners_failure():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = "http://54.74.133.71/register_user"

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"error": "Failed to register user."}, status_code=400)
        response = register_miners(wallet_address)
        assert response == {"error": "Failed to register user.", "status_code": 400}
        assert m.last_request.json() == {"wallet_address": wallet_address}

def test_userdata_success():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = "http://54.74.133.71/user_data/table"

    # Define sample user data
    user_data = {
        "Point": 100,
        "Incentive": 50,
        "Daily Attempt": 5,
        "Broken": 2,
        "Stake": 500,
        "Total Attempt": 50
    }

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"user_table": "Mocked table data"}, status_code=200)
        response = userdata(wallet_address)
        
        # Assert response
        assert response == "Mocked table data"
        
        # Assert last request payload
        assert m.last_request.json() == {"wallet_address": wallet_address}


def test_userdata_failure():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = "http://54.74.133.71/user_data/table"

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"error": "Failed to fetch user data."}, status_code=500)
        response = userdata(wallet_address)
        
        # Assert response
        assert response == {"error": "Failed to fetch user data.", "status_code": 500}
        
        # Assert last request payload
        assert m.last_request.json() == {"wallet_address": wallet_address}

