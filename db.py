from os import environ as env
from contextlib import contextmanager

from datetime import datetime, timezone

from flask import current_app

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor


"""
Constants
"""
DB_SCHEMA = env["DATABASE_SCHEMA"] if "DATABASE_SCHEMA" in env else "gas_tracker"

RECEIPT_RETURN = (
    "r.receipt_id, r.gallons, r.price_per_gallon, r.total_cost, "
    "gs.station_id, gs.company as station_company, "
    "v.vehicle_id, v.label as vehicle_label, "
    "r.created_on, r.updated_on, r.deleted_on "
)
"""
SQL Return String

Format:

{
    receipt_id: string,
    gallons: number,
    price_per_gallon: number,
    total_cost: number,

    station_id: number,
    station_company: string,

    vehicle_id: string,
    vehicle_label: string | null,

    created_on: Date,
    updated_on: Date,
    deleted_on: Date | null,
}
"""


"""
Database Setup
"""
pool = None

def setup():
    global pool

    URL = env["DATABASE_URL"]

    if current_app:
        current_app.logger.info("Creating database connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=URL, sslmode="require", connect_timeout=5)

@contextmanager
def get_db_conn():
    try:
        conn = pool.getconn()

        yield conn
    finally:
        pool.putconn(conn)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_conn() as conn:
        cursor = conn.cursor(cursor_factory=DictCursor)

        try:
            yield cursor

            if commit:
                conn.commit()
        finally:
            cursor.close()


"""
Database Helpers
"""
def user_exists(user_id):
    pass

def receipt_exists(receipt_id):
    pass


"""
Resource Functions
"""
# Receipts
def select_receipt(receipt_id):
    """
    TODO: docs
    """

    sqlQuery = (
        f"SELECT {RECEIPT_RETURN}"
        f" FROM {DB_SCHEMA}.receipts r"
        f" JOIN {DB_SCHEMA}.gas_stations gs USING (station_id)"
        f" JOIN {DB_SCHEMA}.vehicles v USING (vehicle_id)"
        " WHERE r.receipt_id=%s;"
    )
    params = (receipt_id,)

    with get_db_cursor() as curs:
        curs.execute(sqlQuery, params)

        receipt = curs.fetchone()

    if receipt is None:
        return None

    return dict(receipt)

def insert_receipt(
    user_id: str,
    vehicle_id: str,
    station_id: int,
    gallons: float,
    price_per_gallon: float,
):
    """
    TODO: docs
    """

    sqlQuery = (
        f"INSERT INTO {DB_SCHEMA}.receipts"
        " (user_id, vehicle_id, station_id, gallons, price_per_gallon)"
        " VALUES (%s, %s, %s, %s, %s)"
        " RETURNING receipt_id;"
    )
    params = (user_id, vehicle_id, station_id, gallons, price_per_gallon,)

    with get_db_cursor(commit=True) as curs:
        curs.execute(sqlQuery, params)

        row = curs.fetchone()

    receiptId = dict(row)["receipt_id"]

    return receiptId

def update_receipt(
    receipt_id: str,
    vehicle_id: str | None = None,
    station_id: int | None = None,
    gallons: float | None = None,
    price_per_gallon: float | None = None,
    deleted: bool | None = None,
):
    """
    TODO: docs
    """

    sqlQuery = (
        f"UPDATE {DB_SCHEMA}.receipts"
        " SET updated_on=%s"
    )
    params = [
        datetime.now().astimezone()
    ]
    if vehicle_id is not None:
        sqlQuery += ", vehicle_id=%s"
        params.append(vehicle_id)
    if station_id is not None:
        sqlQuery += ", station_id=%s"
        params.append(station_id)
    if gallons is not None:
        sqlQuery += ", gallons=%s"
        params.append(gallons)
    if price_per_gallon is not None:
        sqlQuery += ", price_per_gallon=%s"
        params.append(price_per_gallon)
    if deleted is not None:
        if deleted:
            sqlQuery += ", deleted_on=CURRENT_TIMESTAMP"
        else:
            sqlQuery += ", deleted_on=NULL"
    sqlQuery += " WHERE receipt_id=%s;"
    params.append(receipt_id)

    with get_db_cursor(commit=True) as curs:
        curs.execute(sqlQuery, tuple(params))

        if curs.rowcount != 1:
            return False

    return True

def delete_receipt(receipt_id):
    """
    TODO: docs
    """

    sqlQuery = (
        f"DELETE FROM {DB_SCHEMA}.receipts"
        " WHERE receipt_id=%s;"
    )
    params = (receipt_id,)

    with get_db_cursor(commit=True) as curs:
        curs.execute(sqlQuery, params)

        if curs.rowcount != 1:
            return False

    return True

def select_all_receipts(user_id, vehicle_id):
    """
    TODO: docs
    """

    sqlQuery = (
        f"SELECT {RECEIPT_RETURN}"
        f" FROM {DB_SCHEMA}.receipts r"
        f" JOIN {DB_SCHEMA}.gas_stations gs USING (station_id)"
        f" JOIN {DB_SCHEMA}.vehicles v USING (vehicle_id)"
        f" LEFT OUTER JOIN {DB_SCHEMA}.has_access ha ON ha.user_id=%(user_id)s"
        " WHERE (v.owner_id=%(user_id)s OR ha.user_id=%(user_id)s)"
    )
    params = {
        "user_id": user_id,
    }
    if vehicle_id is not None:
        sqlQuery += " AND v.vehicle_id=%(vehicle_id)s"
        params["vehicle_id"] = vehicle_id
    sqlQuery += ";"

    with get_db_cursor() as curs:
        curs.execute(sqlQuery, params)

        rows = curs.fetchall()

    return list(map(dict, rows))

# Gas Stations
def select_gas_station(station_id):
    """
    TODO: docs
    """

    pass

def insert_gas_station():
    """
    TODO: docs
    """

    pass

def update_gas_station():
    """
    TODO: docs
    """

    pass

def delete_gas_station():
    """
    TODO: docs
    """

    pass

def select_all_stations():
    """
    TODO: docs
    """

    sqlQuery = f"SELECT station_id, company FROM {DB_SCHEMA}.gas_stations"

    with get_db_cursor() as curs:
        curs.execute(sqlQuery)

        rows = curs.fetchall()

    return list(map(dict, rows))

# Vehicles
def select_vehicle(vehicle_id):
    """
    TODO: docs
    """

    pass

def insert_vehicle(user_id):
    """
    TODO: docs
    """

    pass

def update_vehicle(vehicle_id):
    """
    TODO: docs
    """

    pass

def delete_vehicle(user_id):
    """
    TODO: docs
    """

    pass

def select_all_vehicles(user_id):
    """
    TODO: docs
    """

    sqlQuery = (
        f"SELECT v.vehicle_id, v.label, v.make, v.model, v.color"
        f" FROM {DB_SCHEMA}.vehicles v"
        f" LEFT OUTER JOIN {DB_SCHEMA}.has_access ha ON v.vehicle_id=ha.vehicle_id"
        " WHERE v.owner_id=%(user_id)s OR ha.user_id=%(user_id)s"
        " ORDER BY (v.owner_id=%(user_id)s) DESC;"
    )
    params = {"user_id": user_id}

    with get_db_cursor() as curs:
        curs.execute(sqlQuery, params)

        rows = curs.fetchall()

    return list(map(dict, rows))
