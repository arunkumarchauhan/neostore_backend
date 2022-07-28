from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail

from util.models import TimeStampModel
from util.helper.regex import phoneNumberRegex

# Create your models here.


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if not password == user.confirm_password:
            raise ValueError('The Passwords not same ')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super(CustomUserManager, self).get_queryset()


class User(AbstractBaseUser, TimeStampModel, PermissionsMixin):
    first_name = models.CharField(null=False, blank=False, max_length=254)
    last_name = models.CharField(null=False, blank=False, max_length=254)
    username = models.CharField(null=True, max_length=128, blank=True)
    is_staff = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=False)
    email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(null=False, blank=False, max_length=128)
    confirm_password = models.CharField(
        null=False, blank=False, max_length=128)
    gender = models.CharField(max_length=1, null=False, default="M", choices=(
        ("M", "M"), ("F", "F"), ("T", "T")))
    phone_no = models.CharField(
        validators=[phoneNumberRegex], null=False, blank=False, max_length=15)
    profile_pic = models.CharField(null=True, blank=True, max_length=1000)
    dob = models.DateField(null=False, blank=False)
    country_id = models.IntegerField(null=True, blank=True)
    REQUIRED_FIELDS = ["first_name", "last_name",
                       "password", "confirm_password", "gender", "phone_no", "dob"]
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = 'user'
