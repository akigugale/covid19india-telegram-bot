from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(verbose=True)

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

def getenv(var_name):
    return os.getenv(var_name)
