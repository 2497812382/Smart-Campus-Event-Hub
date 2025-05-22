from django.db import models

# Create your models here.

class EventParticipation(models.Model):
    date = models.DateField(unique=True)
    expected_count = models.PositiveIntegerField()
    actual_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.date} Participation: {self.actual_count}/{self.expected_count}"

    @property
    def participation_rate(self):
        if self.expected_count == 0:
            return 0
        return (self.actual_count / self.expected_count) * 100