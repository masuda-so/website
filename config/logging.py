"""Error notification handling that cannot obscure the original request failure."""

import logging

from django.utils.log import AdminEmailHandler

logger = logging.getLogger(__name__)


class ResilientAdminEmailHandler(AdminEmailHandler):
    """Report notification failures to the console without failing error handling."""

    def send_mail(self, subject, message, *args, **kwargs):
        try:
            super().send_mail(subject, message, *args, **kwargs)
        except Exception:  # noqa: BLE001 - Error reporting must not raise a second error.
            # This logger uses the console-only root handler in production.
            logger.warning("Could not deliver the administrator error email.")
