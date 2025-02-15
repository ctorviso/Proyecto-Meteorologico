from src.shared.helpers import get_env_var

host = get_env_var("HOST")

if host == "localhost":
    aemet_url = f"http://{host}:8000/api/aemet"
    db_url = f"http://{host}:8000/api/db"
else:
    aemet_url = f"https://{host}/api/aemet"
    db_url = f"https://{host}/api/db"
