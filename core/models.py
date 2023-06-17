from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


