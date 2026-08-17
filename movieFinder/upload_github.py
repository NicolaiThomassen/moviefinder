import base64
import requests
import os

def upload_to_github():
    """
    Uploads the all_movies.pkl file to the specified GitHub repository.
    """
    OWNER = "NicolaiThomassen"
    REPO = "moviefinder"
    PATH = "all_movies.pkl"
    BRANCH = "main"

    token = os.environ["GITHUB_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"

    # Find SHA for eksisterende fil
    response = requests.get(
        url,
        headers=headers,
        params={"ref": BRANCH},
    )
    response.raise_for_status()

    sha = response.json()["sha"]

    # Læs den nye PKL
    with open("all_movies.pkl", "rb") as f:
        content = base64.b64encode(f.read()).decode("ascii")

    # Erstat filen
    response = requests.put(
        url,
        headers=headers,
        json={
            "message": "Update movie database",
            "content": content,
            "sha": sha,
            "branch": BRANCH,
        },
    )

    response.raise_for_status()
    print(response.json()["commit"]["html_url"])