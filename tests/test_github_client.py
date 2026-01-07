import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.github_client import fetch_repo_details


@pytest.mark.asyncio
@patch("app.github_client.httpx.AsyncClient.get")
async def test_fetch_repo_details_success(mock_get):
    # Create a fake response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "stargazers_count": 123,
        "language": "Python",
        "description": "Mocked repo"
    }

    # Mock the async get() call to return this response
    mock_get.return_value = mock_response

    data = await fetch_repo_details("tiangolo", "fastapi")

    assert data is not None
    assert data["stars"] == 123
    assert data["language"] == "Python"
