from dotenv import load_dotenv
import os

result = load_dotenv(dotenv_path="/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/.env", verbose=True)
print(f".env file loaded: {result}")

# Test environment variable
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"API Key Loaded: {api_key}")
else:
    print("Failed to load API Key")
