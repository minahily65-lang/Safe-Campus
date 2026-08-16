from database import (
    create_sos,
    get_all_alerts,
    update_alert_status,
    delete_alert,
)


def send_sos_alert(user, location):
    """
    Create and save a new SOS alert.
    """

    try:

        alert_id = create_sos(
            student_id=user["_id"],
            student_name=user["name"],
            latitude=location["latitude"],
            longitude=location["longitude"],
        )

        return {
            "success": True,
            "alert_id": str(alert_id),
            "message": "SOS alert sent successfully."
        }

    except Exception as error:

        print("SOS Alert Error:", error)

        return {
            "success": False,
            "alert_id": None,
            "message": "Unable to send SOS alert."
        }


def get_sos_alerts():
    """
    Get all SOS alerts.
    """

    try:

        return get_all_alerts()

    except Exception as error:

        print("Get Alerts Error:", error)

        return []


def change_alert_status(alert_id, status):
    """
    Change the status of an SOS alert.
    """

    try:

        result = update_alert_status(
            alert_id,
            status
        )

        return result

    except Exception as error:

        print(
            "Update Alert Status Error:",
            error
        )

        return False


def remove_alert(alert_id):
    """
    Delete an SOS alert.
    """

    try:

        return delete_alert(alert_id)

    except Exception as error:

        print(
            "Delete Alert Error:",
            error
        )

        return False
