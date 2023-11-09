from django.db import models


# Create your models here.
class SchoolRecipient(models.Model):
    school_name = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField()

    class Meta:
        unique_together = ("school_name", "recipient_name", "recipient_email")

    def __str__(self):
        return f"{self.school_name} - {self.recipient_name}"
