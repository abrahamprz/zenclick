from celery import shared_task
from django.core.management import call_command


@shared_task
def create_weekly_repair_report():
    call_command("general")


@shared_task
def create_daily_lost_mode_report():
    call_command("lostmode")


@shared_task
def celery_test():
    print("Celery worked!")
