import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

User = get_user_model()


class AbstractBase(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at',]
    
    @property
    def created_by_user(self):
        created_by = self.created_by
        if not created_by:
            return None
        
        try:
            user = User.objects.get(id=created_by)
        except User.DoesNotExist:
            return None

        return user
    
    @property
    def created_by_user_name(self):
        return self.created_by_user.full_name if self.created_by_user else ""
    
    @property
    def updated_by_user(self):
        updated_by = self.updated_by
        if not updated_by:
            return None
        
        try:
            user = User.objects.get(id=updated_by)
        except User.DoesNotExist:
            return None

        return user
    
    @property
    def updated_by_user_name(self):
        return self.updated_by_user.full_name if self.updated_by_user else ""


class OrgAbstractMixin(AbstractBase):

    org_id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        abstract = True
    
    @property
    def organization(self):
        from organizations.models import Organization
        try:
            return Organization.objects.get(id=self.org_id)
        except Organization.DoesNotExist:
            return None
    
    # def validate_organization_exists(self):
    #     try:
    #         Account.objects.get(id=self.account_id)
    #     except Account.DoesNotExist:
    #         raise ValidationError({'account_id': 'No account with the given account_id exists.'})
        
    # def clean(self, *args, **kwargs):
    #     self.validate_user_exist()
    #     super().clean(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save()


class OwnedAbstractMixin(AbstractBase):

    owner = models.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        abstract = True


def get_file_name(instance, filename):
    file_name = '-'.join([filename]) 
    return '/'.join(['attachments', instance.attachment_type, file_name])


class Attachment(AbstractBase):

    file = models.FileField(upload_to=get_file_name)
    # attachment_type = models.CharField(max_length=255, choices=AttachmentTypeEnum.choices)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()
