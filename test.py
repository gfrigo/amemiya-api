import os
from src.core.utils import get_hash
from dotenv import load_dotenv
from pathlib import Path
from src.core.database import start_connection, start_cursor, Statements
from src.register import Register
import reverse_geocode as rg

coords = (-23.5505, -46.6333)

result = rg.search([coords])

print(result)