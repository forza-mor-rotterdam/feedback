import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def general_settings(context):
    return {
        "DEBUG": settings.DEBUG,
        "DEV_SOCKET_PORT": settings.DEV_SOCKET_PORT,
        "GET": context.GET,
        "OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID,
    }
