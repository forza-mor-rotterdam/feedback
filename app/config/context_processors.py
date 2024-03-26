import logging

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def general_settings(context):
    deploy_date_formatted = None
    if settings.DEPLOY_DATE:
        deploy_date = timezone.datetime.strptime(
            settings.DEPLOY_DATE, "%d-%m-%Y-%H-%M-%S"
        )
        deploy_date_formatted = deploy_date.strftime("%d-%m-%Y %H:%M:%S")
    return {
        "DEBUG": settings.DEBUG,
        "DEV_SOCKET_PORT": settings.DEV_SOCKET_PORT,
        "GET": context.GET,
        "OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID,
        "GIT_SHA": settings.GIT_SHA,
        "DEPLOY_DATE": deploy_date_formatted,
    }
