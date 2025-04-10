import builtins
from unittest.mock import patch, MagicMock
import pytest

@patch("builtins.print")
@patch("pymongo.MongoClient")
@patch.dict("os.environ", {"MONGO_URI": "mongodb://testserver:27017/"})
def test_main_runs(mock_mongo_client, mock_print):
    # Mock list_database_names
    mock_client_instance = MagicMock()
    mock_client_instance.list_database_names.return_value = ["test_db"]
    mock_mongo_client.return_value = mock_client_instance

    # Importing main will run all code
    import main  # noqa: F401

    printed = [args[0] for args, _ in mock_print.call_args_list]

    assert any("Python version:" in line for line in printed)
    assert any("NumPy version:" in line for line in printed)
    assert any("TensorFlow version:" in line for line in printed)
    assert any("OpenCV version:" in line for line in printed)
    assert any("PyMongo version:" in line for line in printed)
    assert any("MongoDB connection attempt made" in line for line in printed)
    assert any("Database connection successful" in line for line in printed)
    assert any("ML client test completed successfully!" in line for line in printed)
