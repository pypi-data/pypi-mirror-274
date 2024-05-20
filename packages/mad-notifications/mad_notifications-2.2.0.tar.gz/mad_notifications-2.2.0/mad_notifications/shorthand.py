from mad_notifications.models import get_email_template_model
from mad_notifications.notification import Notification


def newNotification(user, title, content, template_slug=None, data={}, actions={}):
    """
    Shorthand method to create and send notification

    `title`, `content` will be overridden if `template_slug` is provided

    """
    # get email template from db
    try:
        if template_slug is not None:
            notification_template = get_email_template_model().objects.get(
                slug=template_slug
            )
        else:
            raise  # pylint: disable=E0704
    except Exception:
        notification_template = None

    # create a notification for user
    notification = Notification(
        user=user,
        title=title,
        content=str(content),
        mobile_content=str(content),
        template=notification_template,
        data=data,
        actions=actions,
    )

    return notification.notify()
