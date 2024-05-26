from core.celery import celery_app


@celery_app.task(name="send_welcome_email")
def send_welcome_email(user_id):
    """
    Task to send a welcome email to a new user.

    Parameters:
        user_id (int): The ID of the user to whom the welcome email is sent.
    """
    # Logic to send an email would go here
    print(f"Sending welcome email to user {user_id}")
    # Simulate email sending delay
    import time

    time.sleep(5)
    return f"Welcome email sent to user {user_id}"


@celery_app.task(name="log_user_activity")
def log_user_activity(user_id, activity):
    """
    Task to log user activity.

    Parameters:
        user_id (int): The ID of the user.
        activity (str): Description of the activity.
    """
    # Logic to log the activity would go here
    print(f"Logging activity for user {user_id}: {activity}")
    # Simulate logging delay
    import time

    time.sleep(2)
    return f"Activity logged for user {user_id}: {activity}"
