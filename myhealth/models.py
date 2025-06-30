from datetime import date
from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    source = models.CharField(max_length=20, default='cycle')

    class Meta:
        unique_together = 'user', 'date'

    def user_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Mood(models.Model):
    class Options(models.TextChoices):
        HAPPY = 'HAPPY', _('Happy')
        SAD = 'SAD', _('Sad')
        NEUTRAL = 'NEUTRAL', _('Neutral')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(
        max_length=20,
        choices=Options.choices,
        default=Options.HAPPY,
    )
    date = models.DateField()
    source = models.CharField(max_length=20, default='mood')

    class Meta:
        unique_together = 'user', 'date'

    def get_mood(self) -> Options:
        # Get value from choices enum
        return self.Options[self.mood].label

    def user_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Appointment(models.Model):
    # APPOINTMENT_TYPES = [
    #     ('work', 'Work'),
    #     ('personal', 'Personal'),
    #     ('medical', 'Medical'),
    # ]

    # APPOINTMENT_STATUSES = [
    #     ('upcoming', 'Upcoming'),
    #     ('completed', 'Completed'),
    #     ('canceled', 'Canceled'),
    # ]

    class Options(models.TextChoices):
        WORK = 'WORK', _('Work')
        PERSONAL = 'PERSONAL', _('Personal')
        MEDICAL = 'MEDICAL', _('Medical')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    doctor = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=20, default='appointment')
    type = models.CharField(
        max_length=20, choices=Options.choices, default=Options.MEDICAL,)
    # status = models.CharField(max_length = 20, choices = APPOINTMENT_STATUSES, default = 'upcoming')
    # cancel_reason = models.TextField(blank = True, null = True)

    def user_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name

    def __str__(self) -> str:
        return self.full_name()


class Intercourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    protection_used = models.BooleanField(default=False)
    contraception_method = models.CharField(
        max_length=100, blank=True, null=True)
    with_whom = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, blank=True, null=True)

    source = models.CharField(max_length=20, default='intercourse')

    # def __str__(self):
    #     return f"Intercourse on {self.date_time} by {self.user.username} with {self.with_whom}"


class PhysicalActivity(models.Model):
    class ActivityType(models.TextChoices):
        CARDIOVASCULAR = 'CARDIO', _('Cardiovascular')
        STRENGTH_TRAINING = 'STRENGTH', _('Strength/Weight Training')
        FLEXIBILITY_BALANCE_TRAINING = 'FLEXIBILITY_BALANCE', _(
            'Flexibility and Balance')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.CARDIOVASCULAR,
    )
    specific_activity = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    calories_burned = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        verbose_name = _("Physical Activity")
        verbose_name_plural = _("Physical Activities")

    def get_activity_type(self) -> ActivityType:
        return self.ActivityType[self.activity_type].label    

    def __str__(self):
        return f"{self.specific_activity} ({self.get_activity_type_display()}) - {self.date}"



class Sleep(models.Model):
    class QualityType(models.TextChoices):
        EXCELLENT = 'EXCELLENT', _('Excellent')
        GOOD = 'GOOD', _('Good')
        FAIR = 'FAIR', _('Fair')
        POOR = 'POOR', _('Poor')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    quality = models.CharField(
        max_length=20,
        choices=QualityType.choices,
        default=QualityType.GOOD,
    )
    total_hours = models.FloatField(default=8)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quality} Sleep ({self.total_hours} hours)"

