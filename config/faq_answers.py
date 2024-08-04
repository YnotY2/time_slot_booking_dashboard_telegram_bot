from utils.logger import setup_logger
logger = setup_logger(service_name="faq_answers")

# Frequently asked questions matching answers
# The callback_data string argument is the same for answers and data, see 'faq_data.py'
faq_answers = {
    "faq_origin_coffee_beans": (
        "♣️ Origin Country Coffee Beans;\n"
        "\n"
        "One of the most famous coffee beans in the world, the Ethiopian Yirgacheffe bean,"
        " originates from the Yirgacheffe region in Ethiopia. "
        "Ethiopia is often referred to as the birthplace of coffee, w"
        "ith its rich coffee culture and history dating back centuries. "
        "According to legend, a goat herder named Kaldi discovered the "
        "energizing effects of coffee beans when he noticed his goats becoming "
        "particularly lively after eating the berries from a certain tree. Today, "
        "Ethiopian Yirgacheffe coffee is celebrated for its unique and "
        "diverse flavor profiles, often featuring bright acidity and "
        "floral or fruity notes, making it a favorite among coffee enthusiasts globally."

        ),
    "faq_opening_hours": (
        "🕣 Openings Hours:\n"
         "\n"
         "🎴 Monday:       8:00 AM - 6:00 PM\n"
         "🎴 Tuesday:      8:00 AM - 6:00 PM\n"
         "🎴 Wednesday:    8:00 AM - 6:00 PM\n"
         "🎴 Thursday:     8:00 AM - 6:00 PM\n"
         "🎴 Friday:       8:00 AM - 8:00 PM\n"
         "🎴 Saturday:     9:00 AM - 8:00 PM\n"
         "🎴 Sunday:       9:00 AM - 4:00 PM\n"
         "\n"
    ),
    "faq_accepted_payment_options": (
        "️ We accept the following payment methods:\n"
        "\n"
        "🎴 Ideal\n"
        "\n"
        "🎴 Paypal\n"
        "\n"
        "🎴 Sepa\n"
    ),
    "faq_contact_info": (
        "️📋 Contact Info:\n"
        "\n"
        "📞 PhoneNumber:  (555) 123-4567\n"
        "✉️ Email:        contact@ciifecoffee.com\n"
    ),
    "how_is_our_coffee_made": (
        "\n"
        "Our Coffee Is made with love and care :\n"
        "\n"
    ),

}

