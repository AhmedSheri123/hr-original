from django.db import models

# Create your models here.

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import string, pytz, datetime, random
from django.conf import settings
languages_choices = settings.LANGUAGES

SubscriptionsTheemChoices = (
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('success', 'success'),
    ('danger', 'danger'),
    ('warning', 'warning'),
    ('info', 'info'),
    ('light', 'light'),
    ('dark', 'dark'),
)

CurrencyChoices = (
    ("SAR", "ريال سعودي"),
    ("USD", "دولار"),
    ("EUR", "يورو"),
)

plan_type_choices = [
    ('premium', 'Premium'),
    ('pro', 'PRO'),
    ('basic', 'Basic'),
]

plan_scope_choices = [
    ('1', 'Monthly'),
    ('2', 'Yearly')
]



# Create your models here.
def payOrderCodeGen():
    N = 16
    res = ''.join(random.choices(string.digits, k=N))
    return 'order' + str(res)

# Create your models here.

class SubscriptionsModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='العنوان')
    subtitle = models.TextField(verbose_name='العنوان الفرعي')
    ico = models.ImageField(upload_to='subscription/ico/', blank=True)

    Theem = models.CharField(max_length=255, choices=SubscriptionsTheemChoices, null=True, verbose_name='الثيم')
    plan_type = models.CharField(max_length=255, choices=plan_type_choices, null=True, verbose_name='نو الاشتراك')

    number_of_days = models.IntegerField(default=30, verbose_name='عدد الأيام')

    price_monthly = models.DecimalField(max_digits=6, null=True, decimal_places=2, verbose_name='السعر')
    discont_monthly = models.IntegerField(default=0, null=True, verbose_name='خصم')

    price_yearly = models.DecimalField(max_digits=6, null=True, decimal_places=2, verbose_name='السعر')
    discont_yearly = models.IntegerField(default=0, null=True, verbose_name='خصم')

    currency = models.CharField(max_length=250, choices=CurrencyChoices, default='USD', null=True, verbose_name='العملة')


    # حدود المستخدمين
    number_of_employees = models.IntegerField(default=4, verbose_name='عدد الموظفين')
    number_of_managers = models.IntegerField(default=1, verbose_name='عدد المدراء')

    # ميزات الاشتراك المتعلقة بالموارد البشرية
    manage_employee = models.BooleanField(default=False, verbose_name='إدارة الموظفين')
    manage_recruitment = models.BooleanField(default=False, verbose_name='إدارة التوظيف')
    manage_onboarding = models.BooleanField(default=False, verbose_name='إدارة التدريب والاختبارات')
    manage_attendance = models.BooleanField(default=False, verbose_name='إدارة الحضور')
    payroll_management = models.BooleanField(default=False, verbose_name='إدارة الرواتب')
    leave_management = models.BooleanField(default=False, verbose_name='إدارة الإجازات')
    manage_assets = models.BooleanField(default=False, verbose_name='إدارة الأصول')
    pms_management = models.BooleanField(default=False, verbose_name='إدارة الأداء')
    manage_Offboarding = models.BooleanField(default=False, verbose_name='إدارة الخروج')
    manage_helpdesk = models.BooleanField(default=False, verbose_name='إدارة الدعم الفني')

    # تقارير إضافية متعلقة بالموارد البشرية
    employee_attendance_report = models.BooleanField(default=False, verbose_name='تقرير حضور الموظفين')
    employee_salary_report = models.BooleanField(default=False, verbose_name='تقرير رواتب الموظفين')
    employee_leave_report = models.BooleanField(default=False, verbose_name='تقرير إجازات الموظفين')
    performance_review_report = models.BooleanField(default=False, verbose_name='تقرير مراجعة الأداء')

    # إشعارات عبر البريد الإلكتروني أو الرسائل النصية
    send_email_notifications = models.BooleanField(default=False, verbose_name='إرسال إشعارات عبر البريد الإلكتروني')

    live_chat_with_support = models.BooleanField(default=False, verbose_name='دردشة مباشرة مع الدعم الفني')

    
    is_enabled = models.BooleanField(default=True, verbose_name='هل الاشتراك قابل للشراء')

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return str(self.title)
    



class UserSubscriptionModel(models.Model):
    subscription = models.ForeignKey('SubscriptionsModel', on_delete=models.CASCADE)
    number_of_days = models.IntegerField(default=30)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    plan_scope = models.CharField(max_length=254, choices=plan_scope_choices,  null=True)
    currency = models.CharField(max_length=250, choices=CurrencyChoices, default='USD', null=True, verbose_name='العملة')
    
    creation_date = models.DateTimeField(null=True, default=timezone.now, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return str(self.subscription.title)

    @property
    def get_expiry_date(self):
        expiry_date = self.creation_date + timezone.timedelta(days=self.number_of_days)
        return expiry_date
    
    @property
    def is_active(self):
        """ التحقق مما إذا كان الاشتراك لا يزال نشطًا """
        expiry_date = self.get_expiry_date
        return timezone.now() < expiry_date

class UserPaymentOrderModel(models.Model):
    subscription = models.ForeignKey(SubscriptionsModel, on_delete=models.SET_NULL, null=True)
    orderID = models.CharField(max_length=250, default=payOrderCodeGen, null=True, verbose_name="الاسم الثلاثي")
    transactionNo = models.CharField(max_length=250, null=True)
    is_buyed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
