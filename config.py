import os
from dotenv import load_dotenv

load_dotenv()

_secret_key = os.getenv("SECRET_KEY")
if _secret_key is None:
    raise RuntimeError("SECRET_KEY environment variable is missing")
SECRET_KEY: str = _secret_key