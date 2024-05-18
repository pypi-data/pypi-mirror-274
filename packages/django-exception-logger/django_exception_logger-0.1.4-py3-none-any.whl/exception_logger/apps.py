from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExceptionLoggerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exception_logger"
    verbose_name = _("Exception Logger")

    def ready(self):
        from . import signals
