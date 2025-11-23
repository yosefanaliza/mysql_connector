from dotenv import load_dotenv
import os

load_dotenv()

"""
Database configuration module.
Store database credentials separately from main code (security best practice).
"""

# Database configuration dictionary
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME'),
}


CONNECTION_ATTEMPTS = 3
CONNECTION_DELAY = 2
