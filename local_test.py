from apis.zendesk import ZendeskAPI
from json import dumps

zendesk_api = ZendeskAPI(
    api_key="",
    subdomain="",
    email=""
)

active_views = zendesk_api.get_active_views()
# print(dumps(active_views, indent=4))

search_view_title = "Copy of SLMS Chromebooks (1 week)"
search_view_id = ""

for view in active_views["views"]:
    if view["title"] == search_view_title:
        search_view_id = view["id"]
        break

searched_view = zendesk_api.get_tickets_in_view(search_view_id)
tickets_in_view = searched_view["tickets"]

ticket_fields = zendesk_api.get_ticket_fields()

for ticket in tickets_in_view:
    print(f"Ticket ID: {ticket['id']}")
    custom_status_id = ticket['custom_status_id']
    custom_status = zendesk_api.get_custom_status(custom_status_id)
    custom_status_title = custom_status['custom_status']['title']
    print(f"Ticket status: {custom_status_title}")
    print(f"Ticket Subject: {ticket['subject']}")
    print(f"Item tag: {MISSING}")
    print(f"Requester: {REQUESTER_ID}")
    print(f"Requested date: {ticket['created_at']}")
    print(f"Category: {CATEGORY}")