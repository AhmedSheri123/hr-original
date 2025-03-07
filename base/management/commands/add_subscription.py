# your_app/management/commands/add_subscription.py

from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionsModel, UserSubscriptionModel
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add a subscription and a user subscription to the database'

    def add_arguments(self, parser):
        # Add arguments for the SubscriptionsModel fields
        parser.add_argument('title', type=str, help='The title of the subscription')
        parser.add_argument('subtitle', type=str, help='The subtitle of the subscription')
        parser.add_argument('theem', type=str, help='The theme of the subscription')
        parser.add_argument('plan_type', type=str, help='The plan type of the subscription')
        parser.add_argument('number_of_days', type=int, default=30, help='Number of days for the subscription')
        parser.add_argument('price_monthly', type=float, help='The monthly price')
        parser.add_argument('discont_monthly', type=int, default=0, help='Discount on the monthly price')
        parser.add_argument('price_yearly', type=float, help='The yearly price')
        parser.add_argument('discont_yearly', type=int, default=0, help='Discount on the yearly price')
        parser.add_argument('currency', type=str, help='The currency used for the subscription')
        parser.add_argument('number_of_employees', type=int, default=4, help='Number of employees')
        parser.add_argument('number_of_managers', type=int, default=1, help='Number of managers')
        parser.add_argument('manage_employee', type=str, default="False", help='Manage employees feature')
        parser.add_argument('manage_recruitment', type=str, default="False", help='Manage recruitment feature')
        parser.add_argument('manage_onboarding', type=str, default="False", help='Manage onboarding feature')
        parser.add_argument('manage_attendance', type=str, default="False", help='Manage attendance feature')
        parser.add_argument('payroll_management', type=str, default="False", help='Manage payroll feature')
        parser.add_argument('leave_management', type=str, default="False", help='Manage leave feature')
        parser.add_argument('manage_assets', type=str, default="False", help='Manage assets feature')
        parser.add_argument('pms_management', type=str, default="False", help='Manage PMS feature')
        parser.add_argument('manage_offboarding', type=str, default="False", help='Manage offboarding feature')
        parser.add_argument('manage_helpdesk', type=str, default="False", help='Manage helpdesk feature')
        parser.add_argument('employee_attendance_report', type=str, default="False", help='Employee attendance report')
        parser.add_argument('employee_salary_report', type=str, default="False", help='Employee salary report')
        parser.add_argument('employee_leave_report', type=str, default="False", help='Employee leave report')
        parser.add_argument('performance_review_report', type=str, default="False", help='Performance review report')
        parser.add_argument('send_email_notifications', type=str, default="False", help='Send email notifications')
        parser.add_argument('live_chat_with_support', type=str, default="False", help='Live chat with support')
        parser.add_argument('is_enabled', type=str, default="True", help='Is subscription enabled')

        # Add arguments for the UserSubscriptionModel fields
        parser.add_argument('plan_scope', type=str, help='Plan scope for the user subscription')
        parser.add_argument('number_of_days_user', type=int, default=30, help='Number of days for the user subscription')

    def handle(self, *args, **options):
        for key, value in options.items():
            if value == "False":
                options[key] = False
            elif value == "True":
                options[key] = True  # Ensure "True" is properly converted

        # Create a new subscription
        subscription = SubscriptionsModel.objects.create(
            title=options['title'],
            subtitle=options['subtitle'],
            Theem=options['theem'],
            plan_type=options['plan_type'],
            number_of_days=options['number_of_days'],
            price_monthly=options['price_monthly'],
            discont_monthly=options['discont_monthly'],
            price_yearly=options['price_yearly'],
            discont_yearly=options['discont_yearly'],
            currency=options['currency'],
            number_of_employees=options['number_of_employees'],
            number_of_managers=options['number_of_managers'],
            manage_employee=options['manage_employee'],
            manage_recruitment=options['manage_recruitment'],
            manage_onboarding=options['manage_onboarding'],
            manage_attendance=options['manage_attendance'],
            payroll_management=options['payroll_management'],
            leave_management=options['leave_management'],
            manage_assets=options['manage_assets'],
            pms_management=options['pms_management'],
            manage_Offboarding=options['manage_offboarding'],
            manage_helpdesk=options['manage_helpdesk'],
            employee_attendance_report=options['employee_attendance_report'],
            employee_salary_report=options['employee_salary_report'],
            employee_leave_report=options['employee_leave_report'],
            performance_review_report=options['performance_review_report'],
            send_email_notifications=options['send_email_notifications'],
            live_chat_with_support=options['live_chat_with_support'],
            is_enabled=options['is_enabled'],
            creation_date=timezone.now()
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created subscription: {subscription.title}'))
        UserSubscriptionModel.objects.all().delete()
        # Create a user subscription
        user_subscription = UserSubscriptionModel.objects.create(
            subscription=subscription,
            number_of_days=options['number_of_days_user'],
            price=options['price_monthly'],
            plan_scope=options['plan_scope'],
            creation_date=timezone.now()
        )
        user_subscription.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created user subscription for: {user_subscription.subscription.title}'))
