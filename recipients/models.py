from django.db import models


# Create your models here.
class SchoolRecipient(models.Model):
    school_name = models.CharField(max_length=255, blank=False)
    recipient_name = models.CharField(max_length=255, blank=False)
    recipient_email = models.EmailField(blank=False)

    class Meta:
        unique_together = ("school_name", "recipient_name", "recipient_email")
        ordering = ["school_name"]

    def __str__(self):
        return f"{self.school_name} - {self.recipient_name} ({self.recipient_email})"
