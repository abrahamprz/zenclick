from celery import shared_task
from django.core.management import call_command


@shared_task
def create_weekly_repair_report():
    call_command("generalreport")


@shared_task
def create_lost_mode_report():
    call_command("lostmodereport")


@shared_task
def celery_test():
    print("Celery worked!")
