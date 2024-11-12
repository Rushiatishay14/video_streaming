from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import CustomManager

# Create your models here.
class UserMaster(AbstractBaseUser):
    first_name = models.CharField(
        max_length=255, null=True, blank=True, help_text="First name of the user."
    )
    last_name = models.CharField(
        max_length=255, null=True, blank=True, help_text="Last name of the user."
    )
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField(
        default=False, help_text="Whether the user is a superuser."
    )
    is_staff = models.BooleanField(
        default=False, help_text="Whether the user is a staff member."
    )
    is_admin = models.BooleanField(
        default=False, help_text="Whether the user is an admin."
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether the user is active."
    )
    objects = CustomManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # # Check if the user is active
        # if not self.is_active:
        #     return False

        # # Check if the user has a specific permission based on role
        # if self.role:
        #     # Assuming your RoleMaster model has a 'permissions' field that stores permissions
        #     if perm in self.role.permissions:
        #         return True

        return True


class UserActivityTracking(models.Model):
    user = models.ForeignKey(
        UserMaster,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="user_activity",
        db_index=True,
    )
    ip_address = models.GenericIPAddressField(
        max_length=100, null=True, blank=True, editable=False
    )
    url = models.CharField(max_length=255, null=True, blank=True, editable=False)
    request_type = models.CharField(
        max_length=10, null=True, blank=True, editable=False
    )
    request_data = models.JSONField(null=True, blank=True, editable=False)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    referer = models.URLField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    status_code = models.IntegerField(null=True, blank=True, editable=False)
    response_time = models.FloatField(null=True, blank=True, editable=False)
    response = models.JSONField(null=True, blank=True, editable=False)
    #history = HistoricalRecords()

    def __str__(self) -> str:
        return f"  - {self.request_type} - "

    class Meta:
        db_table = "user_activity_tracking"
        ordering = ["-id"]
        verbose_name_plural = "User Activity Tracking"
        verbose_name = "User Activity Tracking"
