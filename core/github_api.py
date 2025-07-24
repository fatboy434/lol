import requests

class GitHubAPI:
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    def get_latest_release(self):
        """
        Gets the latest release from the GitHub repository.
        """
        try:
            response = requests.get(f"{self.api_url}/releases/latest")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting latest release: {e}")
            return None
