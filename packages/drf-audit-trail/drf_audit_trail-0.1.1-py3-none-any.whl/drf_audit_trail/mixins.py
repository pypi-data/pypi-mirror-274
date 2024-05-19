from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseModelMixin(models.Model):
    extra_informations = models.TextField(_("Extra information"), null=True, blank=True)
    datetime = models.DateTimeField(verbose_name=_("Datetime"), auto_now_add=True)

    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("User")
    )

    def __str__(self) -> str:
        return f"Id: {self.pk} - User: {self.user}"

    class Meta:
        abstract = True
        ordering = ["-datetime"]
