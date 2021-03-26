from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    ADMIN = 1
    MUSIC_LIBRARY_MODERATOR = 2
    PHOTO_LIBRARY_MODERATOR = 3
    EVENTS_MODERATOR = 4
    SECRETARY = 5
    BOARD_MEMBER = 6
    MUSICIAN = 7
    ROLE_CHOICES = (
        (ADMIN, 'Administrateur'),
        (MUSIC_LIBRARY_MODERATOR, 'Modérateur partothèque'),
        (PHOTO_LIBRARY_MODERATOR, 'Modérateur photothèque'),
        (EVENTS_MODERATOR, 'Modérateur évènements'),
        (SECRETARY, 'Secrétaire'),
        (BOARD_MEMBER, 'Membre du bureau'),
        (MUSICIAN, 'Musicien'),
    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True
    )

    def __str__(self):
        return self.get_id_display()


class Profile(AbstractUser):
    signup_confirmation = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role)

    def has_any_role(self, *roles):
        return any(r in roles for r in [r.id for r in self.roles.all()])

    @property
    def is_admin(self):
        return self.has_any_role(Role.ADMIN)

    @property
    def is_music_library_moderator(self):
        return self.has_any_role(Role.MUSIC_LIBRARY_MODERATOR)

    @property
    def is_photo_library_moderator(self):
        return self.has_any_role(Role.PHOTO_LIBRARY_MODERATOR)

    @property
    def is_events_moderator(self):
        return self.has_any_role(Role.EVENTS_MODERATOR)

    @property
    def is_secretary(self):
        return self.has_any_role(Role.SECRETARY)

    @property
    def is_board_member(self):
        return self.has_any_role(Role.BOARD_MEMBER)

    @property
    def is_musician(self):
        return self.has_any_role(Role.MUSICIAN)

    class Meta:
        verbose_name = 'Profil'

    def __str__(self):
        return self.username
