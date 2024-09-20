"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""


import pytest

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

# Import the dict that holds all the counters
from src.counter import COUNTERS



@pytest.fixture()
def client():
  return app.test_client()


@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """ Test cases for Counter-related endpoints """

    # Basic Test To Test Creating a Counter
    def test_create_a_counter(self, client):
        """ It should create a counter """
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED
    """
    def test_create_a_counter():
        #It should create a counter
         client = app.test_client()
         result = client.post('/counters/foo')
         assert result.status_code == status.HTTP_201_CREATED
    """

    def test_duplicate_a_counter(self, client):
        """ It should return an error for duplicates """
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        """ It should update an existing counter """
        # Update Counter That Doesn't Exist
        result = client.put('/counters/uac')
        assert result.status_code == status.HTTP_404_NOT_FOUND

        # Make Counter To Exist
        result = client.post('/counters/uac')
        assert result.status_code == status.HTTP_201_CREATED

        # Check Counter Value
        assert COUNTERS["uac"] == 0

        # Update Counter
        result = client.put('/counters/uac')
        assert result.status_code == status.HTTP_200_OK

        # Test Counter Value
        assert COUNTERS["uac"] == 1

    def test_get_a_counter(self, client):
        """ It should get an existing counter """
        # Read Counter That Doesn't Exist
        result = client.get('/counters/gac')
        assert result.status_code == status.HTTP_404_NOT_FOUND

        # Make Counter To Exist
        result = client.post('/counters/gac')
        assert result.status_code == status.HTTP_201_CREATED

        # Retrieve Counter
        result = client.get('/counters/gac')
        assert result.status_code == status.HTTP_200_OK

        # Read Counter
        assert COUNTERS["gac"] == 0