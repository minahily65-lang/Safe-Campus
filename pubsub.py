# pubsub.py

from database import alerts_collection
from datetime import datetime


def send_sos_alert(user, location):
    """
    Save a new SOS alert to MongoDB.
    """

    alert = {
        "student_name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "location": location["location"],
        "time": location["timestamp"],
        "status": "Pending"
    }

    alerts_collection.insert_one(alert)

    return alert


def get_all_alerts():
    """
    Get all SOS alerts.
    """

    return list(alerts_collection.find())


def update_alert_status(alert_id, status):
    """
    Update alert status.
    """

    from bson import ObjectId

    alerts_collection.update_one(
        {"_id": ObjectId(alert_id)},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        }
    )


def delete_alert(alert_id):
    """
    Delete an SOS alert.
    """

    from bson import ObjectId

    alerts_collection.delete_one(
        {"_id": ObjectId(alert_id)}
    )