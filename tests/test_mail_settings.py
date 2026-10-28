"""Exercise every settings profile without opening an SMTP or SES connection."""

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from allauth.account.adapter import get_adapter
from anymail.backends.amazon_ses import EmailBackend as SESEmailBackend
from botocore.stub import ANY
from botocore.stub import Stubber
from django.core import mail

from config.logging import ResilientAdminEmailHandler

SMTP = "django.core.mail.backends.smtp.EmailBackend"
CONSOLE = "django.core.mail.backends.console.EmailBackend"
MEMORY = "django.core.mail.backends.locmem.EmailBackend"
SES = "anymail.backends.amazon_ses.EmailBackend"


@pytest.mark.parametrize(
    ("profile", "override", "backend"),
    [
        ("base", None, SMTP),
        ("base", CONSOLE, CONSOLE),
        ("local", None, CONSOLE),
        ("local", SMTP, SMTP),
        ("local", MEMORY, MEMORY),
        ("test", SMTP, MEMORY),
        ("production", None, SES),
        ("production", CONSOLE, SES),
    ],
)
def test_settings_create_mailers_without_deprecations(profile, override, backend):
    # Import each profile in isolation: local/production modify base app lists.
    # Do not inherit credentials or load local .env files in the subprocess.
    env = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT") if key in os.environ}
    env.update(
        DJANGO_SETTINGS_MODULE=f"config.settings.{profile}",
        DJANGO_READ_DOT_ENV_FILE="False",
        DATABASE_URL="postgres:///website",
        DJANGO_SECRET_KEY="test-only-mail-settings-key",  # noqa: S106 - Test fixture.
        DJANGO_ADMIN_URL="test-admin/",
        DJANGO_AWS_ACCESS_KEY_ID="test-only-access-key",
        DJANGO_AWS_SECRET_ACCESS_KEY="test-only-secret-key",  # noqa: S106 - Test fixture.
        DJANGO_AWS_STORAGE_BUCKET_NAME="test-only-bucket",
        AWS_EC2_METADATA_DISABLED="true",
    )
    if override is not None:
        env["DJANGO_EMAIL_BACKEND"] = override
    code = """
import json
import warnings
from unittest.mock import patch

warnings.simplefilter('error', DeprecationWarning)
from django.conf import settings
from django.core.mail import mailers

with patch('socket.socket.connect', side_effect=AssertionError('Network forbidden')):
    backend = mailers.default
    result = {
        'backend': type(backend).__module__ + '.' + type(backend).__name__,
        'alias': backend.alias,
        'host': getattr(backend, 'host', None),
        'timeout': getattr(backend, 'timeout', None),
        'connection': getattr(backend, 'connection', None),
        'client': getattr(backend, 'client', None),
    }
print(json.dumps(result))
"""
    result = subprocess.run(  # noqa: S603 - Fixed interpreter and test-only code.
        [sys.executable, "-c", code],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    actual = json.loads(result.stdout)
    assert actual["backend"] == backend
    assert actual["alias"] == "default"
    assert actual["connection"] is None
    assert actual["client"] is None
    if backend == SMTP:
        assert actual["host"] == "localhost"
        assert actual["timeout"] == 5  # noqa: PLR2004 - Existing SMTP timeout contract.


@pytest.mark.django_db
def test_allauth_mail_is_delivered_to_the_test_outbox(mailoutbox):
    message = get_adapter().render_mail(
        "account/email/password_reset_key",
        "recipient@example.test",
        {"password_reset_url": "https://example.test/reset/test-token/"},
    )
    assert message.send() == 1
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == ["recipient@example.test"]
    assert "https://example.test/reset/test-token/" in mailoutbox[0].body


def test_admin_notification_failure_preserves_original_error(monkeypatch, caplog):
    def fail(*args, **kwargs):
        msg = "Test-only delivery failure"
        raise OSError(msg)

    monkeypatch.setattr(mail, "mail_admins", fail)
    handler = ResilientAdminEmailHandler()
    handler.send_mail("Original error", "Original error details")
    assert "Could not deliver the administrator error email." in caplog.text


def test_admin_notification_uses_the_configured_mailer(settings, mailoutbox):
    settings.ADMINS = ["admin@example.test"]
    handler = ResilientAdminEmailHandler()
    handler.send_mail("Original error", "Original error details")
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == ["admin@example.test"]


def test_account_mail_delivery_failure_is_not_suppressed(monkeypatch):
    def fail(self, messages):
        msg = "Test-only delivery failure"
        raise OSError(msg)

    monkeypatch.setattr(type(mail.mailers.default), "send_messages", fail)
    message = mail.EmailMessage(
        subject="Account notification",
        body="Test message",
        to=["recipient@example.test"],
    )
    with pytest.raises(OSError, match="Test-only delivery failure"):
        message.send()


def test_ses_sending_works_with_outbound_dependencies_only():
    # Use explicit fake credentials and a stubbed AWS response: never send mail.
    with patch(
        "socket.socket.connect", side_effect=AssertionError("Network forbidden")
    ):
        backend = SESEmailBackend(
            client_params={
                "region_name": "us-east-1",
                "aws_access_key_id": "test-only-access-key",
                "aws_secret_access_key": "test-only-secret-key",
            },
        )
        with backend, Stubber(backend.client) as stub:
            stub.add_response(
                "send_email",
                {"MessageId": "test-only-message-id"},
                {
                    "Destination": {"ToAddresses": ["recipient@example.test"]},
                    "Content": {"Raw": {"Data": ANY}},
                },
            )
            message = mail.EmailMessage(
                subject="Test-only subject",
                body="Test-only body",
                from_email="sender@example.test",
                to=["recipient@example.test"],
            )
            assert backend.send_messages([message]) == 1
            stub.assert_no_pending_responses()
