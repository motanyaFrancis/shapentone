import datetime
from tabnanny import verbose

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
from django.utils.translation import gettext_lazy as _

from dashboard.models import LevelSetup, Program
from setup.models import NumberSeries, Setup


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("username is required")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=60, blank=True)
    middle_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, default="2008-01-01")
    current_weight = models.FloatField(default=0, blank=True)
    starting_weight = models.FloatField(default=0, blank=True)
    Target_weight = models.FloatField(default=0, blank=True)
    height = models.FloatField(default=0, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", 'date_of_birth']

    objects = MyUserManager()

    def full_name(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    full_name.short_description = "Name"
    full_name.allow_tags = True

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class MemberCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class SubscriptionSetup(models.Model):
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    applications_allowed = models.BooleanField()
    level = models.ForeignKey(LevelSetup, on_delete=models.PROTECT)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SubscriptionFeatures(models.Model):
    sub_plan = models.ManyToManyField(SubscriptionSetup)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Subscription Setup Feature"

    def __str__(self):
        return self.title


class SubscriptionPeriodSetup(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()


class UserSubscription(models.Model):
    subscription = models.ForeignKey(
        SubscriptionSetup, on_delete=models.PROTECT)
    user = models.ForeignKey(NewUser, on_delete=models.PROTECT)
    invoice_no = models.CharField(max_length=160, editable=False, null=True)
    paid_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(editable=False)
    end_date = models.DateField(editable=False, verbose_name="Expiry Date")
    amount_paid = models.FloatField(blank=True, default=0)
    invoiced_amount = models.FloatField()
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-end_date"]

    def __str__(self):
        return self.invoice_no

    def init_rec(self):
        if self.invoice_no is not None:
            return
        setup = Setup.objects.first()
        if not setup:
            raise Exception("Setup Not Created")
        if setup.invoice_nos is None:
            raise Exception("Invoice Nos not setup")
        no_series = NumberSeries.objects.get(pk=setup.invoice_nos.pk)
        self.invoice_no = no_series.get_next_no()

    def save(self, *args, **kwargs) -> None:

        if self.invoiced_amount is None:
            self.invoiced_amount = self.subscription.amount

        if self.start_date is None:
            self.start_date = datetime.date.today()
        if self.end_date is None:
            self.end_date = self.start_date + datetime.timedelta(days=30)
        self.init_rec()
        return super(UserSubscription, self).save(*args, **kwargs)


class UserPrograms(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    active = models.BooleanField(default=False)
    custom = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Program"

    def __str__(self):
        return f"{self.program}-{self.user}"


class CustomerInfomation(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('text', 'Text'),
        ('other', 'Other')
    ]

    WORK_ACTIVITY_CHOICES = [
        ('standing', 'Standing'),
        ('sitting', 'Sitting'),
        ('driving', 'Driving'),
        ('active', 'Active')
    ]

    MORNING_FATIGUE_CHOICES = [
        ('tired', 'Tired and find it difficult to pull yourself out of bed'),
        ('active', 'Active, refreshed and ready to face the day')
    ]

    TRAVEL_INFO_CHOICES = [
        ('rarely', 'Rarely'),
        ('yearly', 'A few times a year'),
        ('monthly', 'A few times a month'),
        ('weekly', 'Weekly')
    ]

    BODY_WEIGHT_CHOICES = [
        ('underweight', 'Underweight'),
        ('ideal', 'Ideal'),
        ('overweight', 'A bit overweight'),
        ('veryoverweight', 'Very overweight')
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('moderatelyactive', 'Moderately Active'),
        ('active', 'Active'),
        ('highlyactive', 'Highly Active')
    ]

    STRESS_LEVEL_CHOICES = [(str(i), str(i)) for i in range(1, 11)]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    WORK_SCHEDULE_CHOICES = [
        ('days', 'Days'),
        ('afternoons', 'Afternoons'),
        ('nights', 'Nights')
    ]

    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    height = models.DecimalField(max_digits=50, decimal_places=2)
    weight = models.DecimalField(max_digits=50, decimal_places=2)
    phone_number = models.CharField(max_length=50)
    contact_method = models.CharField(
        max_length=16, choices=CONTACT_METHOD_CHOICES, verbose_name="How would you like to be contacted?")
    living_description = models.CharField(
        max_length=255, verbose_name="What do you do for a living?")
    working_hours = models.TextField(
        verbose_name='How many hours on average do you work each week?')
    work_activity = models.CharField(max_length=50, choices=WORK_ACTIVITY_CHOICES,
                                     verbose_name="How do you spend the majority of your time at work?")
    work_schedule = models.CharField(max_length=50, choices=WORK_SCHEDULE_CHOICES,
                                     verbose_name='Do you follow a regular working schedule, do you work days, afternoon or nights?')
    morning_fatigue = models.CharField(
        max_length=50, choices=MORNING_FATIGUE_CHOICES, verbose_name="When you wake up are you: ")
    travel_info = models.CharField(
        max_length=50, choices=TRAVEL_INFO_CHOICES, verbose_name="How often do you travel?")
    body_weight = models.CharField(max_length=50, choices=BODY_WEIGHT_CHOICES,
                                   verbose_name="How would you consider your current body weight?")
    activity_level = models.CharField(max_length=16, choices=ACTIVITY_LEVEL_CHOICES,
                                      verbose_name="How would you describe your current activity level?")
    job_stress_level = models.CharField(
        max_length=16, choices=STRESS_LEVEL_CHOICES, verbose_name="How would you rate the stress of your job?")
    lifestyle_stress_level = models.CharField(
        max_length=16, choices=STRESS_LEVEL_CHOICES, verbose_name="How would you rate the stress of your lifestyle?")
    activities_outside_gym = models.TextField(
        verbose_name="Please list the physical activities that you participate in outside of the gym and outside of work.")
    lifestyle_review_reason = models.TextField(
        verbose_name="Why have you decided to have a lifestyle review?")
    focus_area = models.TextField(
        verbose_name="What is the main area that you would like to focus on?")
    heart_condition_check = models.CharField(
        max_length=16, choices=YES_NO_CHOICES, verbose_name="Has your doctor ever said you have a heart condition?")
    chest_pain_check = models.CharField(max_length=50, choices=YES_NO_CHOICES,
                                        verbose_name="Do you feel pain in your chest at rest, during your daily activities of living, or when you do physical activity?")
    dizziness_check = models.CharField(max_length=50, choices=YES_NO_CHOICES,
                                       verbose_name="Do you lose balance because of dizziness or have you lost consciousness in the last 12 months?")
    bone_muscle_disorder_check = models.CharField(
        max_length=50, choices=YES_NO_CHOICES, verbose_name="Have you ever been diagnosed with another chronic medical condition (other than heart disease or high blood pressure)?")
    blood_pressure_check = models.CharField(max_length=50, choices=YES_NO_CHOICES,
                                            verbose_name="Are you currently taking prescribed medication for high blood pressure or a heart condition?")
    physical_activity_check = models.CharField(
        max_length=50, choices=YES_NO_CHOICES, verbose_name="Do you know of any other reason why you should not engage in physical activity?")

# health and medication
    diagnosed_health_problems = models.TextField(
        verbose_name="Diagnosed Health Problems",
        blank=True,
        null=True
    )

    current_medication = models.TextField(
        verbose_name="Current Medication",
        blank=True,
        null=True
    )

    additional_therapies = models.TextField(
        verbose_name="Additional Therapies",
        blank=True,
        null=True
    )

    injury_or_surgery_history = models.TextField(
        verbose_name="Injury or Surgery History",
        blank=True,
        null=True
    )

    injury_therapy = models.TextField(
        verbose_name="Injury Therapy",
        blank=True,
        null=True
    )

    stress_or_motivation = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Experiencing Stress or Motivation Problems",
        blank=True,
        null=True
    )

    family_heart_disease = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Immediate Family Developed Heart Disease Before 60",
        blank=True,
        null=True
    )

    family_general_diseases = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Diseases Running in Family",
        blank=True,
        null=True
    )

    other_health_diseases = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Suffer from Diabetes, Asthma, High or Low Blood Pressure, Arthritis",
        blank=True,
        null=True
    )

    other_health_diseases_list = models.TextField(
        verbose_name="Other Health Diseases List",
        blank=True,
        null=True
    )

    body_pain = models.CharField(
        max_length=20,
        choices=[
            ('head/neck', 'Head/neck'),
            ('upperback', 'Upper Back'),
            ('shoulders', 'Shoulders'),
            ('arm/leg', 'Arm/leg'),
            ('lowerback', 'Lower Back'),
            ('hips/pelvis', 'Hips/pelvis'),
            ('thigh/knees', 'Thigh/knees'),
            ('other', 'Other')
        ],
        verbose_name="Body Pain Location",
        blank=True,
        null=True
    )

    # Nutrition

    cigarette_smoker = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Are you a current cigarette smoker?",
        blank=True,
        null=True
    )

    alcohol_intake = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Do you drink alcohol?",
        blank=True,
        null=True
    )

    water_intake = models.TextField(
        verbose_name="How much water do you drink each day?(glasses/litres)",
        blank=True,
        null=True
    )

    current_diet = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Are you on any specific food/diet plan at this time?",
        blank=True,
        null=True
    )

    daily_meal_count = models.CharField(
        max_length=10,
        choices=[
            ('1-2', '1-2'),
            ('2-3', '2-3'),
            ('3-4', '3-4'),
            ('5+', '5+')
        ],
        verbose_name="How many meals do you eat each day?",
        blank=True,
        null=True
    )

    raw_salt_meals = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Do you add raw salt in your meals?",
        blank=True,
        null=True
    )

    skip_meals = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Do you skip meals?",
        blank=True,
        null=True
    )

    skipped_meals = models.TextField(
        verbose_name="If yes which ones and how regularly.",
        blank=True,
        null=True
    )

    breakfast_time = models.CharField(
        max_length=50,
        verbose_name="Breakfast Time",
        blank=True,
        null=True
    )

    snack_one_time = models.CharField(
        max_length=50,
        verbose_name="Snack One Time",
        blank=True,
        null=True
    )

    lunch_time = models.CharField(
        max_length=50,
        verbose_name="Lunch Time",
        blank=True,
        null=True
    )

    snack_two_time = models.CharField(
        max_length=50,
        verbose_name="Snack Two Time",
        blank=True,
        null=True
    )

    evening_meal_time = models.CharField(
        max_length=50,
        verbose_name="Evening Meal Time",
        blank=True,
        null=True
    )

    dinner_time = models.CharField(
        max_length=50,
        verbose_name="Dinner Time",
        blank=True,
        null=True
    )

    meal_portions = models.CharField(
        max_length=15,
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
            ('extralarge', 'Extra Large')
        ],
        verbose_name="Which best describes your meal portions",
        blank=True,
        null=True
    )

    hunger_between_meals = models.CharField(
        max_length=10,
        choices=[
            ('no', 'No'),
            ('sometimes', 'Sometimes'),
            ('yes', 'Yes'),
            ('extreme', 'Extreme')
        ],
        verbose_name="Do you ever get hungry between meals?",
        blank=True,
        null=True
    )

    snack_choices = models.TextField(
        verbose_name="If you snack or have any weaknesses, what do you generally tend to eat/drink?",
        blank=True,
        null=True
    )

    recent_weight_gain = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Have you had any recent weight gain or loss?",
        blank=True,
        null=True
    )

    dietary_supplements = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Are you taking any dietary supplement?",
        blank=True,
        null=True
    )

    current_allergies = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Do you have any allergies?",
        blank=True,
        null=True
    )

    current_nutrition_opinion = models.CharField(
        max_length=2,
        choices=[(str(i), str(i)) for i in range(1, 11)],
        verbose_name="Please rate how you feel your current nutritional habits are",
        blank=True,
        null=True
    )

    other_exercise_program_complications = models.CharField(
        max_length=16,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Is there any reason not mentioned why you should not follow a regular exercise program?",
        blank=True,
        null=True
    )

    program_complications_explain = models.TextField(
        verbose_name="If any explain",
        blank=True,
        null=True
    )

    # Fitness Survey Response

    readiness_for_change = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name='Readiness for Change'
    )
    goal_alignment = models.CharField(
        max_length=50,
        choices=[
            ('improvedhealth', 'Improved Health'),
            ('improvedendurance', 'Improved Endurance'),
            ('increasedstrength', 'Increased Strength'),
            ('increasedmusclemass', 'Increased Muscle Mass'),
            ('fatloss', 'Fat Loss'),
            ('improvedflexibility', 'Improved Flexibility'),
            ('improvedposture', 'Improved Posture'),
            ('other', 'Other'),
        ],
        verbose_name='Goal Alignment'
    )
    top_three_goals = models.TextField(verbose_name='Top Three Goals')
    goals_reason = models.TextField(verbose_name='Reason for Goals')
    personal_barriers = models.CharField(
        max_length=50,
        choices=[
            ('lackofmotivation', 'Lack of Motivation'),
            ('time', 'Time'),
            ('selfconscious', 'Self Conscious'),
            ('lackofequipment', 'Lack of Equipment'),
            ('lackofprogress', 'Lack of Progress'),
            ('hittingaplateau', 'Hitting a Plateau'),
            ('how/wheretobegin', 'Not knowing how/where to begin'),
            ('other', 'Other'),
        ],
        verbose_name='Personal Barriers'
    )
    goal_timeline = models.CharField(
        max_length=50,
        choices=[
            ('8wks', '8 weeks'),
            ('16wks', '16 weeks'),
            ('24wks', '24 weeks'),
            ('32wks', '32 weeks'),
            ('40wks', '40 weeks'),
            ('1year', '1 year'),
        ],
        verbose_name='Goal Timeline'
    )

    weekly_training = models.TextField(verbose_name='Weekly Training')

    expected_results_date = models.TextField(
        verbose_name='Expected Results Date')

    goal_motivation = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        verbose_name='Goal Motivation'
    )

    # Fitness Survey

    currently_exercising = models.CharField(
        max_length=16,
        choices=(('yes', 'Yes'), ('no', 'No')),
        verbose_name='Are you currently exercising?'
    )

    previous_exercise = models.CharField(
        max_length=16,
        choices=(('yes', 'Yes'), ('no', 'No')),
        verbose_name='Any previous regular exercise?'
    )

    exercise_efficiency = models.CharField(
        max_length=16,
        choices=(
            ('ineffective', 'Ineffective'),
            ('effective', 'Effective'),
            ('veryeffective', 'Very Effective')
        ),
        verbose_name='Exercise routine efficiency'
    )

    exercise_routine = models.TextField(
        verbose_name='Briefly describe your exercise routine')

    training_weekly_count = models.CharField(
        max_length=16,
        choices=(
            ('1-2time/week', '1-2 times/week'),
            ('2-3time/week', '2-3 times/week'),
            ('3-4time/week', '3-4 times/week'),
            ('5+time/week', '5+ times/week')
        ),
        verbose_name='How often do you train?'
    )

    current_fitness_level = models.CharField(
        max_length=16,
        choices=(
            ('unfit', 'Unfit'),
            ('moderatelyfit',
             'Moderately Fit'),
            ('trained', 'Trained'),
            ('highlytrained', 'Highly Trained')
        ),
        verbose_name='Current fitness level'
    )

    exercise_location = models.CharField(
        max_length=16,
        choices=(
            ('gym', 'Gym'),
            ('home', 'Home'),
            ('outdoors', 'Outdoors'),
            ('other', 'Other')
        ),
        verbose_name='Where do you exercise?'
    )

    current_sports = models.CharField(
        max_length=16, choices=(
            ('yes', 'Yes'), ('no', 'No')),
        verbose_name='Do you participate in any particular sport?'
    )

    movement_restriction = models.TextField(
        verbose_name='Describe any issues restricting your movement during exercise')

    exercise_point_of_dislike = models.TextField(
        verbose_name='What did/do you like the least about exercise?')

    exercise_point_of_enjoyment = models.TextField(
        verbose_name='What did/do you like about exercise?')

    stairs_or_lift = models.CharField(
        max_length=16,
        choices=(
            ('always', 'Always'),
            ('often', 'Often'),
            ('sometimes', 'Sometimes'),
            ('never', 'Never')
        ),
        verbose_name='Stairs or lifts?'
    )
    alternate_activity_choices = models.CharField(
        max_length=16,
        choices=(
            ('always', 'Always'),
            ('often', 'Often'),
            ('sometimes', 'Sometimes'),
            ('never', 'Never')
        ),
        verbose_name='Alternate activity during bad weather/holidays?'
    )
    personal_trainer = models.CharField(
        max_length=16, 
        choices=(('yes', 'Yes'), ('no', 'No')),
        verbose_name='Trained with a personal trainer before?'
    )
    personal_trainer_routine = models.TextField(
        verbose_name='If yes, what kind of training did you do?')

    personal_trainer_experience = models.TextField(
        verbose_name='Experience with previous trainer')

    home_equipment = models.CharField(
        max_length=16,
        choices=(
            ('dumbells', 'Dumbbells'),
            ('barbells', 'Barbells'),
            ('cardiomachines', 'Cardio Machines'),
            ('weightbench', 'Weight Bench'),
            ('mats', 'Mats'),
            ('kettlebells', 'Kettle Bells'),
            ('resistancebands', 'Resistance Bands'),
            ('other', 'Other')
        ),
        verbose_name='Home equipment available'
    )
    training_schedule = models.CharField(
        max_length=19,
        choices=(
            ('morning', 'Morning'),
            ('midday', 'Midday'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening')
        ),
        verbose_name='Preferred training time'
    )
    personal_training_schedule = models.CharField(
        max_length=16,
        choices=(
            ('1day', '1 day'),
            ('2days', '2 days'),
            ('3days', '3 days'),
            ('4days', '4 days'),
            ('5days', '5 days'),
            ('6days', '6 days'),
            ('7days', '7 days')
        ),
        verbose_name='Days per week for Personal Training')

    personal_trainer_expectations = models.TextField(
        verbose_name='Expectations from Personal Trainer')

    personal_responsibility = models.CharField(
        max_length=16,
        choices=(('yes', 'Yes'), ('no', 'No')),
        verbose_name='Accept responsibility for current body condition?'
    )

    class Meta:
        verbose_name_plural = 'Customers Infomation'

    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    full_name.short_description = "User"
    full_name.allow_tags = True

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
