import requests
import os

def fetch_files_from_github(repo_owner, repo_name, folder_path="src", branch="main", output_dir="downloaded_files"):
    """
    Fetches files recursively from a specific folder in a GitHub repository.
    
    Args:
        repo_owner (str): The owner of the repository (e.g., "octocat").
        repo_name (str): The name of the repository (e.g., "Hello-World").
        folder_path (str): The folder path to fetch files from (default is "src").
        branch (str): The branch to fetch files from (default is "main").
        output_dir (str): The local directory to save the downloaded files.
    """
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}?ref={branch}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    def download_file(file_url, file_path):
        response = requests.get(file_url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download {file_url}: {response.status_code}")

    def fetch_folder_contents(url, local_path):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json()
            for item in items:
                if item["type"] == "file":
                    file_url = item["download_url"]
                    local_file_path = os.path.join(local_path, item["path"].replace(folder_path + "/", ""))
                    download_file(file_url, local_file_path)
                elif item["type"] == "dir":
                    fetch_folder_contents(item["url"], local_path)
        else:
            print(f"Failed to fetch folder contents: {response.status_code}")

    fetch_folder_contents(base_url, output_dir)

# Example usage
if __name__ == "__main__":
    repo_owner = "EshwaraSrinivas"  # Replace with the repository owner
    repo_name = "SampleSpringBootApp"  # Replace with the repository name
    folder_path = "src"  # Replace with the folder path you want to fetch
    branch = "main"  # Replace with the branch name
    fetch_files_from_github(repo_owner, repo_name, folder_path, branch)