import os
import subprocess
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads from ".env" in the current directory

# Set these before running
GITHUB_USER = "chungtony83"
REPO_NAME = "tokens"
REPO_DIR = "./tokens"
GITHUB_PAT = os.getenv("GITHUB_PAT")  # Store this securely

REPO_URL = f"https://{GITHUB_USER}:{GITHUB_PAT}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

def generate_key(save_path: str) -> None:
    key = Fernet.generate_key()
    with open(save_path, "wb") as f:
        f.write(key)
    return
    
def write_env_var(key, value, env_path=".env"):
    lines = []
    updated = False

    try:
        with open(env_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        pass  # No existing file, will create a new one

    with open(env_path, "w") as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={value}\n")
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f"{key}={value}\n")

def clone_or_pull_repo():
    if not os.path.exists(REPO_DIR):
        print("Cloning private repo...")
        subprocess.run(["git", "clone", REPO_URL, REPO_DIR], check=True)
    else:
        print("Pulling latest tokens...")
        subprocess.run(["git", "-C", REPO_DIR, "pull"], check=True)

def push_updated_tokens(commit_message="Update tokens"):
    print("Pushing updated tokens...")
    subprocess.run(["git", "-C", REPO_DIR, "add", "."], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "push"], check=True)

def get_token_file(filename: str) -> bytes:
    with open(os.path.join(REPO_DIR, filename), "rb") as f:
        return f.read()

def write_token_file(filename: str, data: bytes):
    with open(os.path.join(REPO_DIR, filename), "wb") as f:
        f.write(data)
        
if __name__ == "__main__":
    path = 