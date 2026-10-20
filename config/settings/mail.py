"""Shared mailer configuration for the base and local settings."""


def default_mailers(backend: str) -> dict[str, dict[str, object]]:
    """Keep SMTP defaults without passing SMTP options to other backends."""
    config: dict[str, object] = {"BACKEND": backend}
    if backend == "django.core.mail.backends.smtp.EmailBackend":
        config["OPTIONS"] = {"host": "localhost", "timeout": 5}
    return {"default": config}
