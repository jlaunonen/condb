from __future__ import absolute_import

import logging

from django.conf import settings
from django.core.mail import EmailMessage

from celery import shared_task


logger = logging.getLogger('kompassi')


@shared_task(ignore_result=True)
def send_email(**opts):
    if settings.DEBUG:
        logger.debug(opts['body'])

    EmailMessage(**opts).send(fail_silently=False)