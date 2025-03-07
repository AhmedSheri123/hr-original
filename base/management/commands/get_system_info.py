import json
from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionsModel
from django.contrib.auth.models import User  # Assuming you're using the default User model
from subscriptions.models import UserSubscriptionModel
class Command(BaseCommand):
    help = 'This command returns JSON data'

    def add_arguments(self, parser):
        # Add argument for the user id (or any other relevant identifier)
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **kwargs):
        # Retrieve user_id from the command arguments
        user_id = kwargs['user_id']

        try:
            user = User.objects.get(id=user_id)  # Get the user by ID
            # Assuming there's a relation between user and subscription (via foreign key or reverse relation)
            subscription = UserSubscriptionModel.objects.all().order_by('-id').first()  # Adjust according to your actual relation setup

            # Preparing the data to return
            data = {
                'username': user.username,
                'subscription': {
                    'title': subscription.subscription.title,
                    'price': float(subscription.price),
                    'plan_scope': subscription.get_plan_scope_display(),
                    'plan_scope_id': subscription.plan_scope,
                    'creation_date': subscription.creation_date.strftime("%Y-%m-%d"),
                    'end_date': subscription.get_expiry_date.strftime("%Y-%m-%d"),  # Adjust field name as per your model
                    'has_subscription': subscription.is_active,
                },
            }

            # Convert data to JSON
            response_data = json.dumps(data, ensure_ascii=False, indent=4)

            # Print the JSON response
            self.stdout.write(response_data)
            exit(0)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with id {user_id} not found."))
            exit(1)
        except SubscriptionsModel.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Subscription for user with id {user_id} not found."))
            exit(1)
        