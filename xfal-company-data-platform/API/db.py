"""Database access layer for XFAL company management API."""

import psycopg2
from psycopg2 import extras

from config import db_config, remote_db_config


def _connect(config=None):
    return psycopg2.connect(**(config or db_config))


def _serialize_rows(rows):
    return [dict(row) for row in rows]


def fetch_all_tables(config=None):
    try:
        connection = _connect(config)
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )
        tables = cursor.fetchall()
        all_tables_data = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f'SELECT * FROM "{table_name}"')
            all_tables_data[table_name] = _serialize_rows(cursor.fetchall())
        cursor.close()
        connection.close()
        return all_tables_data
    except psycopg2.Error as e:
        return {"error": str(e)}


def fetch_all_tables_remote():
    return fetch_all_tables(remote_db_config)


def validate_state(state):
    return isinstance(state, str) and len(state) == 2 and state.isalpha()


def create_company(company_name, address, city, state, zip_code):
    if not validate_state(state):
        return {"error": "Invalid state. It must be a 2-letter code and only contain letters."}

    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            INSERT INTO company (company_name, address, city, state, zip)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING company_id;
            """,
            (company_name, address, city, state, zip_code),
        )
        company_id = cursor.fetchone()[0]
        connection.commit()
        return {"company_id": company_id}
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_company(company_id, company_name, address, city, state, zip_code):
    if not validate_state(state):
        return {"error": "Invalid state. It must be a 2-letter code and only contain letters."}

    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            UPDATE company
            SET company_name = %s, address = %s, city = %s, state = %s, zip = %s
            WHERE company_id = %s;
            """,
            (company_name, address, city, state, zip_code, company_id),
        )
        updated_rows = cursor.rowcount
        connection.commit()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if updated_rows == 0:
        return {"error": "Company not found"}
    return {"message": "Company updated successfully", "company_id": company_id}


def delete_company(company_id):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute("DELETE FROM company WHERE company_id = %s;", (company_id,))
        deleted_rows = cursor.rowcount
        connection.commit()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if deleted_rows == 0:
        return {"error": "Company not found"}
    return {"message": "Company deleted successfully", "company_id": company_id}


def get_company_by_id(company_id):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute("SELECT * FROM company WHERE company_id = %s;", (company_id,))
        company = cursor.fetchone()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if company is None:
        return {"error": "Company not found"}
    return dict(company)


def create_department(department_name):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            INSERT INTO department (department_name)
            VALUES (%s)
            RETURNING department_id;
            """,
            (department_name,),
        )
        department_id = cursor.fetchone()[0]
        connection.commit()
        return {"department_id": department_id}
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_department_by_id(department_id):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            "SELECT * FROM department WHERE department_id = %s;", (department_id,)
        )
        department = cursor.fetchone()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if department is None:
        return {"error": "Department not found"}
    return dict(department)


def update_department(department_id, department_name):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            UPDATE department
            SET department_name = %s
            WHERE department_id = %s;
            """,
            (department_name, department_id),
        )
        updated_rows = cursor.rowcount
        connection.commit()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if updated_rows == 0:
        return {"error": "Department not found"}
    return {"message": "Department updated successfully", "department_id": department_id}


def delete_department(department_id):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            "DELETE FROM department WHERE department_id = %s;", (department_id,)
        )
        deleted_rows = cursor.rowcount
        connection.commit()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if deleted_rows == 0:
        return {"error": "Department not found"}
    return {"message": "Department deleted successfully", "department_id": department_id}


def create_employee(
    first_name, last_name, phone1, phone2, email, company_id, department_id
):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            INSERT INTO employee
                (first_name, last_name, phone1, phone2, email, company_id, department_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING employee_id;
            """,
            (first_name, last_name, phone1, phone2, email, company_id, department_id),
        )
        employee_id = cursor.fetchone()[0]
        connection.commit()
        return {"employee_id": employee_id}
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_employee_by_id(employee_id):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            "SELECT * FROM employee WHERE employee_id = %s;", (employee_id,)
        )
        employee = cursor.fetchone()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if employee is None:
        return {"error": "Employee not found"}
    return dict(employee)


def update_employee(
    employee_id,
    first_name,
    last_name,
    phone1,
    phone2,
    email,
    company_id,
    department_id,
):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """
            UPDATE employee
            SET first_name = %s,
                last_name = %s,
                phone1 = %s,
                phone2 = %s,
                email = %s,
                company_id = %s,
                department_id = %s
            WHERE employee_id = %s;
            """,
            (
                first_name,
                last_name,
                phone1,
                phone2,
                email,
                company_id,
                department_id,
                employee_id,
            ),
        )
        updated_rows = cursor.rowcount
        connection.commit()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if updated_rows == 0:
        return {"error": "Employee not found"}
    return {"message": "Employee updated successfully", "employee_id": employee_id}


def delete_employee(employee_id):
    connection = cursor = None
    try:
        connection = _connect()
        cursor = connection.cursor(cursor_factory=extras.DictCursor)
        cursor.execute("DELETE FROM employee WHERE employee_id = %s;", (employee_id,))
        deleted_rows = cursor.rowcount
        connection.commit()
    except psycopg2.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if deleted_rows == 0:
        return {"error": "Employee not found"}
    return {"message": "Employee deleted successfully", "employee_id": employee_id}
