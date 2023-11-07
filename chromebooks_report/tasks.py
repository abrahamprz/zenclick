from celery import shared_task
from django.core.management import call_command


@shared_task
def create_weekly_report():
    call_command('createreport')