from .models import Notification


def create_notification(
    receiver,
    sender,
    message,
    link=""
):

    if receiver == sender:
        return

    Notification.objects.create(
        receiver=receiver,
        sender=sender,
        message=message,
        link=link
    )