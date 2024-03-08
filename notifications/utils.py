from .models import Notification
from account.models import UserProfile


def get_content(action):
    # TODO set string content from a file to content var
    if action == "vote":
        content = "{} voted! --> This is testing"
    return content


def send_notification(profile: UserProfile, action, to_mail=False):
    if to_mail:
        pass  # TODO send notification to email
    try:
        content = get_content(action)
        Notification.objects.create(profile=profile, action=action, content=content)
    except:
        return False
    else:
        return True
