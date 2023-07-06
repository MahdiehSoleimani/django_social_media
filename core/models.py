from django.db.models import Manager, Q
from django.utils import timezone
from django.db import models
from uuid import uuid4
from django.db.models.query import QuerySet


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class MyManage(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_delet=False)


class SoftManager(Manager):

    def get_queryset(self):
        return SoftQuerySet(self.model, self._db).filter(Q(is_deleted=False) | Q(is_deleted__isnull=True))


class SoftQuerySet(QuerySet):
    def delete(self):
        return self.update(is_deleted=True, delete_at=timezone.now())


class SoftDelete(models.Model):
    is_deleted = models.BooleanField(null=True,
                                     blank=True,
                                     editable=False, )
    deleted_at = models.BooleanField(null=True,
                                     blank=True,
                                     editable=False,)
    objects = SoftManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

