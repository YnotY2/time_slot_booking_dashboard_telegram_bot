from utils.logger import setup_logger
logger = setup_logger(service_name="faq_data")

# Frequently asked questions
# The callback_data string argument is the same for answers and data, see 'faq_answers.py'
faq_data = {
    "faq_origin_coffee_beans": "Origin of the coffee beans?",
    "faq_opening_hours": "Openings hours?",
    "faq_accepted_payment_options": "What payment methods are accepted?",
    "faq_contact_info": "Contact Info?",
    "how_is_our_coffee_made": "How is our coffee made?",
}


