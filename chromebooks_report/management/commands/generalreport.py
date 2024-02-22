import logging  # noqa
from datetime import datetime, timedelta
from os import path as os_path
from sys import path as sys_path

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template.loader import render_to_string

from recipients.models import SchoolRecipient

logger = logging.getLogger(__name__)  # noqa
# ------------------------------------------------------------------------------

current = os_path.dirname(os_path.realpath(__file__))
parent = os_path.dirname(current)
parent_parent = os_path.dirname(parent)
# adding the parent directory to the sys.path
sys_path.append(parent_parent)

# ------------------------------------------------------------------------------

from apis.zendesk import ZendeskAPI  # noqa

TICKET_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_MDY = "%m-%d-%Y"


class Command(BaseCommand):
    """Creates a report of Chromebooks that need to be repaired."""

    help = "Creates a report of Chromebooks that need to be repaired."

    def __init__(self) -> None:
        """Initializes the command."""
        super().__init__()
        self.zendesk_api = ZendeskAPI(
            api_key=settings.ZENDESK_API_KEY, subdomain=settings.ZENDESK_SUBDOMAIN, email=settings.ZENDESK_EMAIL
        )
        self.logger = logging.getLogger(__name__)

    def handle(self, *args, **options) -> None:
        """Handles the command."""

        activity_list = self.get_chromebooks_activity()
        self.create_report(activity_list)
        # self.logger.info(activity_list)

        timestamp = datetime.now().strftime(DATE_TIME_FORMAT)
        self.stdout.write(self.style.SUCCESS(f"[{timestamp}] Report created successfully."))

    def get_chromebooks_activity(self) -> list:
        active_views = self.zendesk_api.get_active_views()

        search_view_title = "Chromebooks activity (last 7 days)"
        search_view_id = next((view["id"] for view in active_views["views"] if view["title"] == search_view_title), "")

        searched_view = self.zendesk_api.get_tickets_in_view(search_view_id)
        tickets_in_view = searched_view["tickets"]
        self.stdout.write(f"Tickets in view: {len(tickets_in_view)}")

        ticket_fields = self.zendesk_api.get_ticket_fields()
        fields = ticket_fields["ticket_fields"]

        # static ids for each field
        item_tag_field_id = next(field["id"] for field in fields if field["title"] == "Item Tag")
        category_field_id = next(field["id"] for field in fields if field["title"] == "Category")
        site_field_id = next(field["id"] for field in fields if field["title"] == "Site")

        sites = [field for field in fields if field["title"] == "Site"][0]
        categories = [field for field in fields if field["title"] == "Category"][0]
        statuses = [field for field in fields if field["title"] == "Ticket status"][0]
        sites_values_and_names = {site["value"]: site["name"] for site in sites["custom_field_options"]}
        categories_values_and_names = {
            category["value"]: category["name"] for category in categories["custom_field_options"]
        }
        statuses_ids_and_names = {status["id"]: status["end_user_label"] for status in statuses["custom_statuses"]}

        site_selected_tickets = {}
        for ticket in tickets_in_view:
            site = sites_values_and_names[
                [site for site in ticket["custom_fields"] if site["id"] == site_field_id][0]["value"]
            ]
            if site not in site_selected_tickets:
                site_selected_tickets[site] = []

            site_ticket = {}
            site_ticket["ticket_id"] = ticket["id"]
            site_ticket["ticket_status"] = statuses_ids_and_names[ticket["custom_status_id"]]
            site_ticket["ticket_subject"] = ticket["subject"]
            site_ticket["item_tag"] = [
                item_tag for item_tag in ticket["custom_fields"] if item_tag["id"] == item_tag_field_id
            ][0]["value"]
            site_ticket["requester"] = self.zendesk_api.get_user(ticket["requester_id"])["user"]["name"]
            # site_ticket["assignee"] = (
            #     self.zendesk_api.get_user(ticket["assignee_id"])["user"]["name"] if ticket["assignee_id"] else "NONE"
            # )
            creation_date_obj = datetime.strptime(ticket["created_at"], TICKET_DATE_FORMAT)
            site_ticket["requested_date"] = f"{creation_date_obj.strftime(DATE_FORMAT_MDY)}"
            site_ticket["category"] = str(
                categories_values_and_names[
                    [category for category in ticket["custom_fields"] if category["id"] == category_field_id][0][
                        "value"
                    ]
                ]
            ).split("::")[-1]

            site_selected_tickets[site].append(site_ticket)

        return site_selected_tickets

    def create_report(self, site_tickets: list) -> None:
        """Creates a report of Chromebooks that need to be repaired."""
        subject = "{site} Chromebooks report {date_seven_days_ago} - {date_today}"
        url_base = f"https://{settings.ZENDESK_SUBDOMAIN}.zendesk.com/agent/tickets/"
        for site in site_tickets:
            try:
                recipient_info = [
                    (p.recipient_email, p.recipient_name)
                    for p in SchoolRecipient.objects.filter(
                        Q(school_name=site) | Q(school_name="ALL"),
                        email_type="GENERAL",
                    )
                ]
            except SchoolRecipient.DoesNotExist:
                logger.error(f"Principal data for {site} is missing.")
                continue
            date_a_week_ago = (datetime.now() - timedelta(days=7)).strftime(DATE_FORMAT_MDY)
            date_now = datetime.now().strftime(DATE_FORMAT_MDY)
            for recipient_email, recipient_name in recipient_info:
                send_mail(
                    subject=subject.format(
                        site=site,
                        date_seven_days_ago=date_a_week_ago,
                        date_today=date_now,
                    ),
                    message="",  # the message is in html format
                    from_email=settings.DJANGO_DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient_email],
                    html_message=render_to_string(
                        template_name="chromebooks_repair_report_template.html",
                        context={
                            "principal_name": recipient_name,
                            "site": site,
                            "date_seven_days_ago": date_a_week_ago,
                            "date_today": date_now,
                            "data_list": site_tickets[site],
                            "base_url": url_base,
                            "tickets_count": len(site_tickets[site]),
                        },
                    ),
                )
