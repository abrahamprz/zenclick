from django.conf import settings
from apis.zendesk import ZendeskAPI
from json import dumps, dump

zendesk_api = ZendeskAPI(
    api_key=settings.ZENDESK_API_KEY,
    subdomain=settings.ZENDESK_SUBDOMAIN,
    email=settings.ZENDESK_EMAIL
)

active_views = zendesk_api.get_active_views()

search_view_title = "Chromebooks activity (last 7 days)"
search_view_id = next((view["id"] for view in active_views["views"] if view["title"] == search_view_title), "")

searched_view = zendesk_api.get_tickets_in_view(search_view_id)
tickets_in_view = searched_view["tickets"]

with open('tickets_in_view.json', 'w') as f:
    dump(tickets_in_view, f, indent=4)

ticket_fields = zendesk_api.get_ticket_fields()
fields = ticket_fields["ticket_fields"]

# static ids for each field
item_tag_field_id = next(field["id"] for field in fields if field["title"] == "Item Tag")
category_field_id = next(field["id"] for field in fields if field["title"] == "Category")
site_field_id = next(field["id"] for field in fields if field["title"] == "Site")


sites = [field for field in fields if field["title"] == "Site"][0]
categories = [field for field in fields if field["title"] == "Category"][0]
statuses = [field for field in fields if field["title"] == "Ticket status"][0]
sites_values_and_names = {site["value"]: site["name"] for site in sites["custom_field_options"]}
categories_values_and_names = {category["value"]: category["name"] for category in categories["custom_field_options"]}
statuses_ids_and_names = {status["id"]: status["end_user_label"] for status in statuses["custom_statuses"]}


site_selected_tickets = {}
for ticket in tickets_in_view:
    site = sites_values_and_names[[site for site in ticket['custom_fields'] if site['id'] == site_field_id][0]['value']]
    if site not in site_selected_tickets:
        site_selected_tickets[site] = []

    site_ticket = {}
    site_ticket["ticket_id"] = ticket["id"]
    site_ticket["ticket_status"] = statuses_ids_and_names[ticket['custom_status_id']]
    site_ticket["ticket_subject"] = ticket["subject"]
    site_ticket["item_tag"] = [item_tag for item_tag in ticket["custom_fields"] if item_tag["id"] == item_tag_field_id][0]["value"]
    site_ticket["requester"] = zendesk_api.get_user(ticket["requester_id"])['user']['name']
    site_ticket["assignee"] = zendesk_api.get_user(ticket['assignee_id'])['user']['name'] if ticket['assignee_id'] else 'NONE'
    site_ticket["requested_date"] = ticket["created_at"]
    site_ticket["category"] = str(categories_values_and_names[[category for category in ticket['custom_fields'] if category['id'] == category_field_id][0]['value']]).split("::")[-1]

    site_selected_tickets[site].append(site_ticket)
print(dumps(site_selected_tickets, indent=4))
print(sum([len(site_selected_tickets[site]) for site in site_selected_tickets]))


for site in site_selected_tickets:
    print(site_selected_tickets[site])
        

subject = "{site} Chromebooks report {date_seven_days_ago} - {date_today}"
email_template = """
Dear {principal_name},

I hope this email finds you well.

Please find attached the report of the Chromebook repair activities from {site} for the period between {date_seven_days_ago} and {date_today}.

{data_table}

Thank you for your attention.

Regards,
IT Department
"""
