# your_app/management/commands/change_user_password.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Change a user\'s password'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str, help='The id of the user')
        parser.add_argument('new_password', type=str, help='The new password for the user')

    def handle(self, *args, **options):
        user_id = options['user_id']
        new_password = options['new_password']

        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Password for user {user.username} successfully changed.'))
            exit(0)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with user_id {user_id} does not exist.'))
            exit(1)
