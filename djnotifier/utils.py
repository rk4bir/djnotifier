# djnotifier/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

AuthModel = get_user_model()


def push_notification_to_anonymous_users(data: dict) -> None:
    """
    Send message/notification (dictionary data) to non-authenticated users/visitors,
    related to `djnotifier/utils.py`.
    """
    try:
        channel_layer = get_channel_layer()
        group_name = 'dj_notifier_anonymous'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "dj_notifier", "data": data}
        )
    except Exception as err:
        print(f"djnotifier->utils->push_notification_to_anonymous_user: {err}")


def push_notification_to_user(data: dict, user: AuthModel) -> None:
    """
    Send message/notification (dictionary data) to authenticated user.
    related to `djnotifier/utils.py`.
    """
    try:
        channel_layer = get_channel_layer()
        group_name = f'dj_notifier_{user.pk}'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "dj_notifier", "data": data}
        )
    except Exception as err:
        print(f"djnotifier->utils->push_notification_to_user: {err}")
