#Triggers to denote user selected testing types
is_web_selected = False
is_api_selected = False
is_pdf_selected = False
is_package_selected = False

#Triggers to Show testing types Menu to user
REQUIRE_DOMAIN_MENU = False

# User Intent
web_user_intent = "Give me a report of failed web test executions in the latest baseline"
api_user_intent = ""
pdf_user_intent = ""
package_user_intent = ""

# JSON paths
web_json = "..\\Code\\Input\\web.json"
api_json = None
pdf_json = None
package_json = None