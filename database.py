from datetime import datetime
from bson.objectid import ObjectId
from config import (
    users_collection,
    alerts_collection,
    history_collection
)


# =========================================================
# USERS
# =========================================================

def register_user(name, email, phone, password, role):
    """
    Register a new user.
    Returns True if successful, False if email already exists.
    """

    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        return False

    users_collection.insert_one({
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "role": role,
        "created_at": datetime.now()
    })

    return True


def login_user(email, password):
    """
    Find user using email and password.
    """

    return users_collection.find_one({
        "email": email,
        "password": password
    })


def get_all_users():
    """
    Return all registered users.
    """

    return list(
        users_collection.find().sort("created_at", -1)
    )


def get_user_by_id(user_id):
    """
    Find a user by MongoDB ObjectId.
    """

    try:
        return users_collection.find_one({
            "_id": ObjectId(user_id)
        })
    except Exception:
        return None


def get_user_by_email(email):
    """
    Find a user by email.
    """

    return users_collection.find_one({
        "email": email
    })


def delete_user(user_id):
    """
    Delete a user by ID.
    """

    try:
        result = users_collection.delete_one({
            "_id": ObjectId(user_id)
        })

        return result.deleted_count > 0

    except Exception:
        return False


# =========================================================
# SOS ALERTS
# =========================================================

def create_sos(
    student_id,
    student_name,
    latitude,
    longitude
):
    """
    Create a new SOS emergency alert.
    """

    alert = {
        "student_id": ObjectId(student_id),
        "student_name": student_name,
        "latitude": latitude,
        "longitude": longitude,
        "status": "Pending",
        "created_at": datetime.now()
    }

    result = alerts_collection.insert_one(alert)

    return result.inserted_id


def get_all_alerts():
    """
    Get all SOS alerts.
    Newest alerts appear first.
    """

    return list(
        alerts_collection.find().sort("created_at", -1)
    )


def get_active_alerts():
    """
    Get only active/pending SOS alerts.
    """

    return list(
        alerts_collection.find({
            "status": "Pending"
        }).sort("created_at", -1)
    )


def update_alert_status(alert_id, status):
    """
    Update SOS alert status.
    """

    try:
        result = alerts_collection.update_one(
            {
                "_id": ObjectId(alert_id)
            },
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.now()
                }
            }
        )

        return result.modified_count > 0

    except Exception:
        return False


def delete_alert(alert_id):
    """
    Delete an SOS alert.
    """

    try:
        result = alerts_collection.delete_one({
            "_id": ObjectId(alert_id)
        })

        return result.deleted_count > 0

    except Exception:
        return False


# =========================================================
# EMERGENCY HISTORY
# =========================================================

def save_history(
    alert_id,
    student_name,
    security_name,
    latitude,
    longitude,
    remarks
):
    """
    Save a resolved emergency into history.
    """

    history = {
        "alert_id": ObjectId(alert_id),
        "student_name": student_name,
        "security_name": security_name,
        "latitude": latitude,
        "longitude": longitude,
        "resolved_at": datetime.now(),
        "remarks": remarks
    }

    result = history_collection.insert_one(history)

    return result.inserted_id


def get_history():
    """
    Get emergency history.
    Newest records appear first.
    """

    return list(
        history_collection.find().sort("resolved_at", -1)
    )


# =========================================================
# DEFAULT ADMIN
# =========================================================

def create_default_admin():
    """
    Create default administrator if no Admin exists.
    """

    admin = users_collection.find_one({
        "role": "Admin"
    })

    if admin is None:

        users_collection.insert_one({
            "name": "Administrator",
            "email": "admin@gmail.com",
            "password": "admin123",
            "phone": "03000000000",
            "role": "Admin",
            "created_at": datetime.now()
        })

        print("Default Admin Created.")


# =========================================================
# DATABASE STARTUP
# =========================================================

create_default_admin()

print("Safe Campus Database Connected Successfully!")
