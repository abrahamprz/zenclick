from apis.zendesk import ZendeskAPI
# from json import dumps

zendesk_api = ZendeskAPI(
    api_key="",
    subdomain="",
    email=""
)

active_views = zendesk_api.get_active_views()

search_view_title = "Copy of SLMS Chromebooks (1 week)"
search_view_id = ""

for view in active_views["views"]:
    if view["title"] == search_view_title:
        search_view_id = view["id"]
        break

searched_view = zendesk_api.get_tickets_in_view(search_view_id)
tickets_in_view = searched_view["tickets"]

ticket_fields = zendesk_api.get_ticket_fields()
fields = ticket_fields["ticket_fields"]

# static ids for each field
item_tag_field_id = [field["id"] for field in fields if field["title"] == "Item Tag"][0]
category_field_id = [field["id"] for field in fields if field["title"] == "Category"][0]
site_field_id = [field["id"] for field in fields if field["title"] == "Site"][0]


sites = [field for field in fields if field["title"] == "Site"][0]
sites_values_and_names = {site["value"]: site["name"] for site in sites["custom_field_options"]}
categories = [field for field in fields if field["title"] == "Category"][0]
categories_values_and_names = {category["value"]: category["name"] for category in categories["custom_field_options"]}
statuses = [field for field in fields if field["title"] == "Ticket status"][0]
statuses_ids_and_names = {status["id"]: status["end_user_label"] for status in statuses["custom_statuses"]}


for ticket in tickets_in_view:
    # print(dumps(ticket, indent=4))
    print(f"Ticket ID: {ticket['id']}")
    print(f"Ticket status: {statuses_ids_and_names[ticket['custom_status_id']]}")
    print(f"Ticket Subject: {ticket['subject']}")
    print(f"Item tag: {[item_tag for item_tag in ticket['custom_fields'] if item_tag['id'] == item_tag_field_id][0]['value']}")
    print(f"Requester: {zendesk_api.get_user(ticket['requester_id'])['user']['name']}")
    print(f"Assignee: {zendesk_api.get_user(ticket['assignee_id'])['user']['name'] if ticket['assignee_id'] else 'NONE'}")
    print(f"Site: {sites_values_and_names[[site for site in ticket['custom_fields'] if site['id'] == site_field_id][0]['value']]}")
    print(f"Requested date: {ticket['created_at']}")    
    print(f"Category: {categories_values_and_names[[category for category in ticket['custom_fields'] if category['id'] == category_field_id][0]['value']]}")
    print("\n------------------------\n")

