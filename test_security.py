import sys
import os
from app.security import verify_password # type: ignore

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from security import verify_password

hashed_password = "$2b$12$2wWm1.c6/EvHOb4/uoApl.lwKX9miNXFvqrx/E03sc4bb7VEyWzpa"
print(verify_password("admin123", hashed_password))  # Expected Output: True
