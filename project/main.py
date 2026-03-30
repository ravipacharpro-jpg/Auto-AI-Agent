import os
import subprocess

def test_github_working():
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], check=True)
    except subprocess.CalledProcessError:
        print("Git is not installed.")
        return

    # Check if the current directory is a git repository
    if not os.path.exists(".git"):
        print("This directory is not a git repository.")
        return

    # Test by fetching the latest changes
    try:
        subprocess.run(["git", "fetch"], check=True)
        print("Git fetch successful. Your GitHub setup is working.")
    except subprocess.CalledProcessError:
        print("Git fetch failed. Please check your GitHub setup.")

if __name__ == "__main__":
    test_github_working()