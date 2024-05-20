# pylint: disable=E1101
# pylint: disable=W0612

from django.template import Template, Context
from mad_notifications.models import get_notification_model

import logging

logger = logging.getLogger(__name__)


class Notification:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.notification_obj = kwargs

        try:
            context = Context({})

            #
            #
            title = Template(self.notification_obj.title)
            content = Template(self.notification_obj.content)
            mobile_content = Template(self.notification_obj.mobile_content)

            # rendering context from data param if it it not empty.
            if self.notification_obj.data:
                context = Context(self.notification_obj.data)

            #
            # if template slug passed to this class,
            # use the template content/mobile content to create the Notification object
            # override, passed title/content/mobile_content
            if self.notification_obj.template is not None:
                self.notification_obj.template = get_notification_model().objects.get(
                    slug=self.notification_obj.template
                )
                title = self.notification_obj.template.subject
                content = self.notification_obj.template.content
                mobile_content = self.notification_obj.template.mobile_content

            #
            self.notification_obj.title = title.render(context)
            self.notification_obj.content = content.render(context)
            self.notification_obj.mobile_content = mobile_content.render(context)

        except Exception as e:
            # logger.error(str("Notification Class...") + str(e))
            pass

    def notify(self, fail_silently=False):
        try:
            return get_notification_model().objects.create(**self.notification_obj)
        except Exception as e:
            logger.warning(str(e))
            if fail_silently is True:
                return None
            else:
                raise
