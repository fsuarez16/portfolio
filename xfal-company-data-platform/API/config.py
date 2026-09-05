import os


def _db_config(prefix: str = "") -> dict:
    """Build a psycopg2 connection dict from environment variables."""
    if prefix:
        prefix = prefix.rstrip("_") + "_"
    return {
        "dbname": os.getenv(f"{prefix}POSTGRES_DB", "xfal"),
        "user": os.getenv(f"{prefix}POSTGRES_USER", "postgres"),
        "password": os.getenv(f"{prefix}POSTGRES_PASSWORD", "example"),
        "host": os.getenv(f"{prefix}POSTGRES_HOST", "localhost"),
        "port": os.getenv(f"{prefix}POSTGRES_PORT", "5432"),
    }


# Primary database (local Docker / default)
db_config = _db_config()

# Optional remote database (AWS RDS, CentOS host, etc.)
remote_db_config = _db_config("REMOTE")
