from django.contrib import admin
from .models import UserSubscriptionModel, SubscriptionsModel
# Register your models here.
admin.site.register(UserSubscriptionModel)
admin.site.register(SubscriptionsModel)