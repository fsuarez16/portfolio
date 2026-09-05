"""XFAL Flask API — CRUD for companies, departments, and employees."""

from pathlib import Path

from flask import Flask, jsonify, request

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass

from db import (
    create_company,
    create_department,
    create_employee,
    delete_company,
    delete_department,
    delete_employee,
    fetch_all_tables,
    fetch_all_tables_remote,
    get_company_by_id,
    get_department_by_id,
    get_employee_by_id,
    update_company,
    update_department,
    update_employee,
)

app = Flask(__name__)


def validate_company_data(data):
    if not data:
        return False
    required_keys = ["company_name", "address", "city", "state", "zip_code"]
    return all(key in data for key in required_keys)


def validate_employee_data(data):
    if not data:
        return False
    required_keys = [
        "first_name",
        "last_name",
        "phone1",
        "phone2",
        "email",
        "company_id",
        "department_id",
    ]
    return all(key in data for key in required_keys)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "xfal-api"}), 200


@app.route("/data", methods=["GET"])
def get_data():
    data = fetch_all_tables()
    status = 500 if isinstance(data, dict) and "error" in data else 200
    return jsonify(data), status


@app.route("/data_remote", methods=["GET"])
def get_data_remote():
    data = fetch_all_tables_remote()
    status = 500 if isinstance(data, dict) and "error" in data else 200
    return jsonify(data), status


@app.route("/companies/<int:company_id>", methods=["GET"])
def get_company_route(company_id):
    result = get_company_by_id(company_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result), 200


@app.route("/companies", methods=["POST"])
def create_company_route():
    data = request.get_json()
    if not validate_company_data(data):
        return jsonify({"error": "Missing required company information"}), 400
    result = create_company(**data)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return (
        jsonify(
            {
                "message": "Company created successfully",
                "company_id": result["company_id"],
            }
        ),
        201,
    )


@app.route("/companies/<int:company_id>", methods=["PUT"])
def update_company_route(company_id):
    data = request.get_json()
    if not validate_company_data(data):
        return jsonify({"error": "Missing required company information"}), 400
    result = update_company(company_id, **data)
    if "error" in result:
        code = 404 if result["error"] == "Company not found" else 500
        return jsonify({"error": result["error"]}), code
    return jsonify({"message": "Company updated successfully", "company_id": company_id}), 200


@app.route("/companies/<int:company_id>", methods=["DELETE"])
def delete_company_route(company_id):
    result = delete_company(company_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify({"message": "Company deleted successfully", "company_id": company_id}), 200


@app.route("/departments", methods=["POST"])
def create_department_route():
    data = request.get_json()
    if not data or "department_name" not in data:
        return jsonify({"error": "Missing department_name"}), 400
    result = create_department(data["department_name"])
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return (
        jsonify(
            {
                "message": "Department created successfully",
                "department_id": result["department_id"],
            }
        ),
        201,
    )


@app.route("/departments/<int:department_id>", methods=["GET"])
def get_department_route(department_id):
    result = get_department_by_id(department_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result), 200


@app.route("/departments/<int:department_id>", methods=["PUT"])
def update_department_route(department_id):
    data = request.get_json()
    if not data or "department_name" not in data:
        return jsonify({"error": "Missing department_name"}), 400
    result = update_department(department_id, data["department_name"])
    if "error" in result:
        code = 404 if result["error"] == "Department not found" else 500
        return jsonify({"error": result["error"]}), code
    return (
        jsonify(
            {
                "message": "Department updated successfully",
                "department_id": department_id,
            }
        ),
        200,
    )


@app.route("/departments/<int:department_id>", methods=["DELETE"])
def delete_department_route(department_id):
    result = delete_department(department_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return (
        jsonify(
            {
                "message": "Department deleted successfully",
                "department_id": department_id,
            }
        ),
        200,
    )


@app.route("/employees", methods=["POST"])
def create_employee_route():
    data = request.get_json()
    if not validate_employee_data(data):
        return jsonify({"error": "Missing required employee information"}), 400
    result = create_employee(**data)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    return (
        jsonify(
            {
                "message": "Employee created successfully",
                "employee_id": result["employee_id"],
            }
        ),
        201,
    )


@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee_route(employee_id):
    result = get_employee_by_id(employee_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result), 200


@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee_route(employee_id):
    data = request.get_json()
    if not validate_employee_data(data):
        return jsonify({"error": "Missing required employee information"}), 400
    result = update_employee(employee_id, **data)
    if "error" in result:
        code = 404 if result["error"] == "Employee not found" else 500
        return jsonify({"error": result["error"]}), code
    return (
        jsonify(
            {"message": "Employee updated successfully", "employee_id": employee_id}
        ),
        200,
    )


@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee_route(employee_id):
    result = delete_employee(employee_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404
    return (
        jsonify(
            {"message": "Employee deleted successfully", "employee_id": employee_id}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
