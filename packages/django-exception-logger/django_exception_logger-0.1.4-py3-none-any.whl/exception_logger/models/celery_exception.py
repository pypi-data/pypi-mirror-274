from django.db.models import (
    Model,
    Manager,
    CharField,
    DateTimeField,
    TextField,
    JSONField,
    PositiveIntegerField,
    ForeignKey,
    CASCADE,
    UniqueConstraint,
)
from django.utils.translation import gettext_lazy as _


class CeleryExceptionManager(Manager):
    @staticmethod
    def save_exception(*, task, exception, traceback, args, kwargs):
        unique_data = {"task": task, "exception": exception}

        exception_model = CeleryExceptionModel.objects.filter(**unique_data).first()
        if exception_model is None:
            exception_model = CeleryExceptionModel(**unique_data)

        exception_model.traceback = traceback
        exception_model.save()

        CeleryExceptionDataModel.objects.create(
            exception=exception_model, args=args, kwargs=kwargs
        )


class CeleryExceptionModel(Model):
    task = CharField(_("Task"), max_length=512)

    exception = TextField()
    traceback = TextField()

    count = PositiveIntegerField(_("Quantity"), default=1)
    last_throw = DateTimeField(_("Last throw"), auto_now=True)
    first_throw = DateTimeField(_("First throw"), auto_now_add=True)

    objects = CeleryExceptionManager()

    class Meta:
        verbose_name = _("Celery Exception")
        verbose_name_plural = _("Celery Exceptions")
        constraints = (
            UniqueConstraint(fields=("task", "exception"), name="exception_task"),
        )

    def __str__(self):
        return ""

    @property
    def short_exception(self):
        max_length = 30
        if len(self.exception) <= max_length:
            return self.exception

        return f"{self.exception[:max_length-3]}..."


class CeleryExceptionDataModel(Model):
    exception = ForeignKey(CeleryExceptionModel, on_delete=CASCADE)

    args = JSONField("args", default=list)
    kwargs = JSONField("kwargs", default=dict)

    datetime = DateTimeField(_("Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Throw data")
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.pk or "-")


class NoLogCeleryException(Model):
    exception = CharField(max_length=256)

    class Meta:
        verbose_name = _("No log Celery Exception")
        verbose_name_plural = _("No log Celery Exceptions")

    def __str__(self):
        return self.exception
