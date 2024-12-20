from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="DhXZ08QBEMU9zS965vsj1zBNxK7kkGvoBoApV3CD3DRg2OS1vJp38SZrkAbk9RVF",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa: F405
# Celery
# ------------------------------------------------------------------------------

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------
# Zendesk API
ZENDESK_API_KEY = env("ZENDESK_API_KEY")
ZENDESK_SUBDOMAIN = env("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = env("ZENDESK_EMAIL")

# Mailgun
MAILGUN_API_KEY = env("MAILGUN_API_KEY")
DJANGO_SERVER_EMAIL = env("DJANGO_SERVER_EMAIL")
MAILGUN_DOMAIN = env("MAILGUN_DOMAIN")
DJANGO_DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")

# GESD32 Inventory API
GESD32_INVENTORY_API_TOKEN = env("GESD32_INVENTORY_API_TOKEN")
GESD32_INVENTORY_API_BASE_URL = env("GESD32_INVENTORY_API_BASE_URL")

# Stirling API
STIRLING_API_BASE_URL = env("STIRLING_API_BASE_URL")
STIRLING_API_TOKEN = env("STIRLING_API_TOKEN")
