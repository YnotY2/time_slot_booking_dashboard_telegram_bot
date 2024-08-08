from utils.logger import setup_logger
logger = setup_logger(service_name="faq_data")

# Frequently asked questions
# The callback_data string argument is the same for answers and data, see 'faq_answers.py'
faq_data = {
    "faq_years_of_experience": "How many year's of experience?",
    "faq_opening_hours": "Openings hours?",
    "faq_accepted_payment_options": "What payment methods are accepted?",
    "faq_contact_info": "Contact Info?",
    "how_is_our_tattoo_made": "How is you're tattoo made?",
}


