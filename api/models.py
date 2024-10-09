from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api.constants import MAX_EMAIL_LENGTH, MAX_FIELD_LENGTH


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser."""

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name='E-mail',)

    username = models.CharField(
        unique=True,
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Name user', 
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=('Username must contain only letters, , '
                         'numbers and @/./+/-/_..')
            )
        ],
    )
    first_name = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Fisrt name'
    )

    last_name = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Last name'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class MemeTemplate(models.Model):
    """ Model representing a meme template."""

    name = models.CharField(max_length=MAX_FIELD_LENGTH)
    image_url = models.URLField()
    default_top_text = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        blank=True
    )
    default_bottom_text = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        blank=True
    )


class Meme(models.Model):
    """Model representing a meme created using a template."""

    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE)
    top_text = models.CharField(max_length=MAX_FIELD_LENGTH)
    bottom_text = models.CharField(max_length=MAX_FIELD_LENGTH)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    """ Model representing a rating given to a meme."""
    
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meme', 'user')