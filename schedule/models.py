from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your models here.
class MedicationSchedule(models.Model):
    medication_name = models.CharField(max_length=255)
    # frequency of doses per day
    frequency = models.PositiveSmallIntegerField()
    # days count, if None -> indefinitely
    duration_days = models.PositiveSmallIntegerField(null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = datetime.now()
        if self.duration_days is not None:
            self.end_date = self.start_date + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"medicine: {self.medication_name} for user: {self.user}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(frequency__gte=1, frequency__lte=15),
                name="valid_frequency",
            )
        ]
