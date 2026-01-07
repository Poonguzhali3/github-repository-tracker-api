import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")


async def fetch_repo_details(owner: str, repo_name: str):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}"

    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(url)

        if response.status_code != 200:
            return None

        data = response.json()
        return {
            "stars": data.get("stargazers_count", 0),
            "language": data.get("language"),
            "description": data.get("description"),
        }
