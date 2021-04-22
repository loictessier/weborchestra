from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from user.models import Role

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('roles', nargs='+', type=int)

    def handle(self, *args, **options):
        create_activated_account(
            options['email'],
            options['password'],
            options['roles'])


def create_activated_account(email, password, roles=[]):
    user = User.objects.create_user(
        email=email,
        username=email,
        password=password
    )
    user.is_active = True
    user.signup_confirmation = True
    for role in roles:
        role = Role.objects.get_or_create(id=role)
        user.roles.add(role[0])
    user.save()
