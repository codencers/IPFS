import requests
import os
from dotenv import load_dotenv

# Dynamically locate the .env file in the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# Retrieve API keys from environment variables
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")

# Validate that the API keys are loaded
if not PINATA_API_KEY or not PINATA_SECRET_API_KEY:
    raise Exception("Pinata API keys are not set in the environment variables. Ensure the .env file is correctly configured.")

PINATA_BASE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

def upload_file_to_pinata(file_path):
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    with open(file_path, "rb") as file:
        files = {"file": file}
        try:
            response = requests.post(
                PINATA_BASE_URL,
                files=files,
                headers=headers
            )
            response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses
        except requests.exceptions.RequestException as e:
            raise Exception(f"Pinata API request failed: {str(e)}")

    if response.status_code == 200:
        ipfs_hash = response.json().get("IpfsHash")
        if not ipfs_hash:
            raise Exception("Pinata API response did not contain an IPFS hash.")
        return ipfs_hash
    else:
        raise Exception(f"Failed to upload to Pinata: {response.text}")