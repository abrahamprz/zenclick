# Generated by Django 4.2.6 on 2023-11-09 17:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SchoolRecipient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("school_name", models.CharField(max_length=255)),
                ("recipient_name", models.CharField(max_length=255)),
                ("recipient_email", models.EmailField(max_length=254)),
            ],
            options={
                "unique_together": {("school_name", "recipient_name", "recipient_email")},
            },
        ),
    ]
