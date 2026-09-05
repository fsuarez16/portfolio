"""
XFAL ETL — normalize company/employee CSV into PostgreSQL tables.

Usage (from repo root):
    python ETL_process/etl_local.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2 import extras

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Data" / "Data.csv"

# Allow importing API config helpers when run from repo root
sys.path.insert(0, str(ROOT / "API"))

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass

from config import db_config  # noqa: E402


def normalize_frames(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df["company_id"] = (
        pd.factorize(
            df["company_name"].astype(str)
            + df["address"].astype(str)
            + df["city"].astype(str)
            + df["state"].astype(str)
            + df["zip"].astype(str)
        )[0]
        + 1
    )
    df["department_id"] = pd.factorize(df["department"].astype(str))[0] + 1

    df_company = df[
        ["company_id", "company_name", "address", "city", "state", "zip"]
    ].drop_duplicates()
    df_department = (
        df[["department_id", "department"]]
        .drop_duplicates()
        .rename(columns={"department": "department_name"})
    )
    df_employee = df[
        [
            "first_name",
            "last_name",
            "phone1",
            "phone2",
            "email",
            "company_id",
            "department_id",
        ]
    ]
    return df_company, df_department, df_employee


def insert_into_table(connection, df: pd.DataFrame, table_name: str) -> None:
    if df.empty:
        return
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ",".join(list(df.columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
    cursor = connection.cursor()
    try:
        extras.execute_values(cursor, query, tuples, template=None)
        connection.commit()
        print(f"Loaded {len(tuples)} rows into {table_name}")
    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error inserting into {table_name}: {e}")
        raise
    finally:
        cursor.close()


def run(config: dict | None = None) -> None:
    cfg = config or db_config
    # When API runs in Docker, host is "db"; from host machine use localhost
    if cfg.get("host") == "db":
        cfg = {**cfg, "host": os.getenv("POSTGRES_HOST", "localhost")}

    print(f"Reading {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    df_company, df_department, df_employee = normalize_frames(df)

    print(f"Connecting to {cfg['host']}:{cfg.get('port', 5432)} / {cfg['dbname']}")
    connection = psycopg2.connect(**cfg)
    try:
        insert_into_table(connection, df_company, "company")
        insert_into_table(connection, df_department, "department")
        insert_into_table(connection, df_employee, "employee")
    finally:
        connection.close()
    print("ETL finished successfully.")


if __name__ == "__main__":
    run()
