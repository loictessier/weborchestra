from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('password')

    def handle(self, *args, **options):
        user = create_activated_account(options['email', 'password'])
        self.stdout.write(user)


def create_activated_account(email, password):
    user = User.objects.create_user(email=email, username=email, password=password)
    user.is_active = True
    user.profile.signup_confirmation = True
    user.save()
    return user
