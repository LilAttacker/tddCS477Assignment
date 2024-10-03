import pytest

# we need to import the unit under test - counter
# Import the dict that holds all the counters
from src.counter import app, COUNTERS

# we need to import the file that contains the status codes
from src import status


@pytest.fixture()
def client():
    return app.test_client()


@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    # Basic Test To Test Creating a Counter
    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post("/counters/foo")
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post("/counters/bar")
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post("/counters/bar")
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        """It should update an existing counter"""
        # Update Counter That Doesn't Exist
        result = client.put("/counters/uac")
        assert result.status_code == status.HTTP_404_NOT_FOUND

        # Make Counter To Exist
        result = client.post("/counters/uac")
        assert result.status_code == status.HTTP_201_CREATED

        # Check Counter Value
        assert COUNTERS["uac"] == 0

        # Update Counter
        result = client.put("/counters/uac")
        assert result.status_code == status.HTTP_200_OK

        # Test Counter Value
        assert COUNTERS["uac"] == 1

    def test_get_a_counter(self, client):
        """It should get an existing counter"""
        # Read Counter That Doesn't Exist
        result = client.get("/counters/gac")
        assert result.status_code == status.HTTP_404_NOT_FOUND

        # Make Counter To Exist
        result = client.post("/counters/gac")
        assert result.status_code == status.HTTP_201_CREATED

        # Retrieve Counter
        result = client.get("/counters/gac")
        assert result.status_code == status.HTTP_200_OK

        # Read Counter
        assert COUNTERS["gac"] == 0

    def test_delete_a_counter(self, client):
        """It should delete a counter"""
        # Delete Counter That Doesn't Exist
        result = client.delete("/counters/grave")
        assert result.status_code == status.HTTP_404_NOT_FOUND

        # Make Counter To Exist
        result = client.post("/counters/grave")
        assert result.status_code == status.HTTP_201_CREATED

        # Retrieve Counter to Prove Existence
        result = client.get("/counters/grave")
        assert result.status_code == status.HTTP_200_OK

        # Delete Counter
        result = client.delete("/counters/grave")
        assert result.status_code == status.HTTP_204_NO_CONTENT

        # Try to Read Counter to Prove Nonexistence Again
        result = client.get("/counters/grave")
        assert result.status_code == status.HTTP_404_NOT_FOUND
