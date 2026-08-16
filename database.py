from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# -----------------------------
# MongoDB Connection
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")

db = client["safe_campus"]

users = db["users"]
sos_alerts = db["sos_alerts"]
emergency_history = db["emergency_history"]

# -----------------------------
# USERS COLLECTION
# -----------------------------

def register_user(name, email, password, phone, role):

    # Check if email already exists
    if users.find_one({"email": email}):
        return False

    users.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "phone": phone,
        "role": role,
        "created_at": datetime.now()
    })

    return True


def login_user(email, password):

    return users.find_one({
        "email": email,
        "password": password
    })


def get_all_users():

    return list(users.find())


def get_user_by_id(user_id):

    return users.find_one({
        "_id": ObjectId(user_id)
    })


def delete_user(user_id):

    users.delete_one({
        "_id": ObjectId(user_id)
    })

def get_user_by_email(email):
    return users.find_one({"email": email})


def register_user(name, email, phone, password, role):

    users.insert_one({
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "role": role
    })

# -----------------------------
# SOS ALERTS COLLECTION
# -----------------------------

def create_sos(student_id,
               student_name,
               latitude,
               longitude):

    sos_alerts.insert_one({

        "student_id": ObjectId(student_id),

        "student_name": student_name,

        "latitude": latitude,

        "longitude": longitude,

        "status": "Pending",

        "created_at": datetime.now()

    })


def get_all_alerts():

    return list(
        sos_alerts.find().sort("created_at", -1)
    )


def update_alert_status(alert_id, status):

    sos_alerts.update_one(

        {
            "_id": ObjectId(alert_id)
        },

        {
            "$set":
            {
                "status": status
            }
        }

    )


def delete_alert(alert_id):

    sos_alerts.delete_one({
        "_id": ObjectId(alert_id)
    })

# -----------------------------
# EMERGENCY HISTORY COLLECTION
# -----------------------------

def save_history(alert_id,
                 student_name,
                 security_name,
                 latitude,
                 longitude,
                 remarks):

    emergency_history.insert_one({

        "alert_id": ObjectId(alert_id),

        "student_name": student_name,

        "security_name": security_name,

        "latitude": latitude,

        "longitude": longitude,

        "resolved_at": datetime.now(),

        "remarks": remarks

    })


def get_history():

    return list(
        emergency_history.find().sort("resolved_at", -1)
    )


# -----------------------------
# DEFAULT ADMIN
# -----------------------------

def create_default_admin():

    admin = users.find_one({
        "role": "Admin"
    })

    if admin is None:

        users.insert_one({

            "name": "Administrator",

            "email": "admin@gmail.com",

            "password": "admin123",

            "phone": "03000000000",

            "role": "Admin",

            "created_at": datetime.now()

        })
    
    


create_default_admin()

print("Safe Campus Database Connected Successfully!")