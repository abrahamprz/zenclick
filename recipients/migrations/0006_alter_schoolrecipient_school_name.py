# Generated by Django 4.2.7 on 2024-02-22 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipients", "0005_alter_schoolrecipient_school_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schoolrecipient",
            name="school_name",
            field=models.CharField(
                choices=[
                    ("ADS", "ADS"),
                    ("CCS", "CCS"),
                    ("DVS", "DVS"),
                    ("EPS", "EPS"),
                    ("GES", "GES"),
                    ("RCS", "RCS"),
                    ("SLMS", "SLMS"),
                    ("SLPS", "SLPS"),
                    ("SWJH", "SWJH"),
                    ("DAC", "DAC"),
                    ("ALL", "ALL"),
                    ("TEST", "TEST"),
                ],
                default="ALL",
                max_length=4,
            ),
        ),
    ]
