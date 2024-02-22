from django.db import models


# Create your models here.
class SchoolRecipient(models.Model):
    EMAIL_TYPES = [
        ("GENERAL", "Receive general report"),
        ("LOST", "Receive lost mode report"),
    ]

    school_name = models.CharField(max_length=255, blank=False)
    recipient_name = models.CharField(max_length=255, blank=False)
    recipient_email = models.EmailField(blank=False)
    email_type = models.CharField(max_length=7, choices=EMAIL_TYPES, default="GENERAL")

    class Meta:
        unique_together = ("school_name", "recipient_name", "recipient_email")
        ordering = ["school_name"]

    def __str__(self):
        return f"{self.school_name} - {self.recipient_name} ({self.recipient_email}) - {self.get_email_type_display()}"
