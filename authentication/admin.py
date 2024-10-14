import datetime

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from authentication.models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ('email', 'password', 'date_of_birth', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'current_weight', 'starting_weight', 'Target_weight', 'height',
                  'is_active', 'is_admin', 'is_staff', 'is_superuser', 'is_email_verified',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdminConfig(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("full_name", "email", "is_staff",
                    "is_active", "is_email_verified")
    list_filter = (
        'is_active',
        'is_admin',
        'is_email_verified',
    )
    search_fields = ("username", "email", "is_staff")

    list_display_links = (
        "email",
        "full_name",
    )

    ordering = ['email', ]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth',)}),
        ('Body Status', {'fields': ('current_weight',
         'starting_weight', 'Target_weight')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'is_admin',
            'is_email_verified',
        )}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ("User Details", {'fields': ('email', 'password1', 'password2')}),
        ("Permission", {'fields': ('is_active', 'is_email_verified')}),
    )

    ordering = ('email',)
    filter_horizontal = ()
    list_per_page = 25


admin.site.register(get_user_model(), UserAdminConfig)


@admin.action(description="suggest Dates")
def suggest_subscription_periods(modeladmin, request, queryset):
    periods = 1
    end_date = datetime.date(datetime.datetime.now().year, 1, 31)
    start_date = datetime.date(datetime.datetime.now().year, 1, 1)
    last_subscription_period = SubscriptionPeriodSetup.objects.last()

    if last_subscription_period:
        start_date = last_subscription_period.end_date + \
            datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=30)

    for i in range(periods):
        SubscriptionPeriodSetup.objects.create(
            start_date=start_date, end_date=end_date)
        start_date = end_date + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=30)


class SubscriptionPeriodSetupAdmin(admin.ModelAdmin):
    actions = (suggest_subscription_periods,)


class SubscriptionSetupAdmin(admin.ModelAdmin):
    list_display = ["name", "amount", "active"]
    list_editable = [
        "active",
    ]


admin.site.register(SubscriptionSetup, SubscriptionSetupAdmin)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "subscription",
        "invoice_no",
        "invoiced_amount",
        "amount_paid",
        "start_date",
        "end_date",
        "active",
        "paid",
    ]
    list_filter = ["active", "paid", "subscription"]
    search_fields = ["user", "subscription"]
    readonly_fields = [
        "invoiced_amount",
        "end_date",
    ]

    def full_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name


admin.site.register(UserSubscription, UserSubscriptionAdmin)


class UserProgramsAdmin(admin.ModelAdmin):
    list_display = ["user", "program", "active", "custom"]
    list_filter = ["active", "program", "custom"]
    search_fields = ["user", "program"]
    autocomplete_fields = [
        "user",
    ]


admin.site.register(UserPrograms, UserProgramsAdmin)


class SubscriptionFeaturesAdmin(admin.ModelAdmin):
    list_display = ["title", "subscription_plans"]
    list_filter = ["sub_plan"]

    def subscription_plans(self, obj):
        return ", ".join([sub.name for sub in obj.sub_plan.all()])


admin.site.register(SubscriptionFeatures, SubscriptionFeaturesAdmin)


class CustomerInfomationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'height', 'weight',
                    'phone_number', 'contact_method')
    list_filter = ('gender', 'height', 'weight', 'contact_method')

    ordering = ['user', ]

    fieldsets = (
        ('Basic information',
         {
             "classes": ["wide", "extrapretty"],
             'fields': ('user', 'gender', 'height', 'weight', 'phone_number', 'contact_method',)
         }),
        ('Lifestyle information',
         {
             "classes": ["collapse", "wide", "extrapretty"],
             'fields': (
                 'living_description', 'working_hours', 'work_activity', 'work_schedule', 'morning_fatigue', 'travel_info', 'body_weight', 'activity_level', 'job_stress_level', 'lifestyle_stress_level', 'activities_outside_gym', 'lifestyle_review_reason', 'focus_area',
             )
         }),
        ('Physical Activity Readiness Questionaire (PAR-Q)',
         {
             "classes": ["collapse", "wide", "extrapretty"],
             'fields': (
                 'heart_condition_check', 'chest_pain_check', 'dizziness_check', 'bone_muscle_disorder_check', 'blood_pressure_check', 'physical_activity_check',
             )
         }),
        ('Medical and Health Information',
         {
             "classes": ["collapse", "wide", "extrapretty"],
             'fields': (
                 'diagnosed_health_problems', 'current_medication', 'additional_therapies', 'injury_or_surgery_history', 'injury_therapy', 'stress_or_motivation', 'family_heart_disease', 'family_general_diseases', 'other_health_diseases', 'other_health_diseases_list', 'body_pain',
             )
         }),
        ('Nutrition',
         {
             "classes": ["collapse", "wide", "extrapretty"],
             'fields': (
                 'cigarette_smoker', 'alcohol_intake', 'water_intake', 'current_diet', 'daily_meal_count', 'raw_salt_meals', 'skip_meals', 'skipped_meals', 'breakfast_time', 'snack_one_time', 'lunch_time', 'snack_two_time', 'evening_meal_time', 'dinner_time', 'meal_portions', 'hunger_between_meals', 'snack_choices', 'recent_weight_gain', 'dietary_supplements', 'current_allergies', 'current_nutrition_opinion', 'other_exercise_program_complications', 'program_complications_explain',
             )
         }),
        ('Goals',
         {
             "classes": ["collapse", "wide", "extrapretty"],
             'fields': (
                 'readiness_for_change', 'goal_alignment', 'top_three_goals', 'goals_reason', 'personal_barriers', 'goal_timeline', 'weekly_training', 'expected_results_date', 'goal_motivation',
             )
         }),
        ('Fitness and Movement',
         {
             "classes": ["collapse", "wide", "extrapretty"],
             'fields': (
                 'currently_exercising', 'previous_exercise', 'exercise_efficiency', 'exercise_routine', 'training_weekly_count', 'current_fitness_level', 'exercise_location', 'current_sports', 'movement_restriction', 'exercise_point_of_dislike', 'exercise_point_of_enjoyment', 'stairs_or_lift', 'alternate_activity_choices', 'personal_trainer', 'personal_trainer_routine', 'personal_trainer_experience', 'home_equipment', 'training_schedule', 'personal_training_schedule', 'personal_trainer_expectations', 'personal_responsibility',
             )
         }),
    )


admin.site.register(CustomerInfomation, CustomerInfomationAdmin)
