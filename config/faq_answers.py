from utils.logger import setup_logger
logger = setup_logger(service_name="faq_answers")

# Frequently asked questions matching answers
# The callback_data string argument is the same for answers and data, see 'faq_data.py'
faq_answers = {
    "faq_years_of_experience": (
        "♣️ Years of Experience:\n"
        "\n"
        "With over a decade of experience in the tattoo industry, our talented artists "
        "bring a wealth of knowledge and skill to every design. Their journey began "
        "in the early 2010s, and since then, they've honed their craft through countless "
        "hours of practice and a deep passion for body art. From mastering traditional "
        "styles to exploring contemporary trends, our artists have developed a reputation "
        "for exceptional artistry and precision. Each tattoo is a testament to their "
        "commitment to quality and their dedication to making every client's vision come to life. "
        "Their extensive experience ensures that you receive not only a beautiful tattoo but "
        "also a professional and enjoyable experience."
    ),
    "faq_opening_hours": (
        "🕣 Openings Hours:\n"
         "\n"
         "🎴 Monday:       16:00 - 23:00\n"
         "🎴 Tuesday:      16:00 - 22:00\n"
         "🎴 Wednesday:    16:00 - 0:00\n"
         "🎴 Thursday:     16:00 - 2:00 PM\n"
         "🎴 Friday:       16:00 - 2:00 PM\n"
         "🎴 Saturday:     17:00 - 4:00\n"
         "🎴 Sunday:       17:00 - 4:00\n"
         "\n"
    ),
    "faq_accepted_payment_options": (
        "️ We accept the following payment methods:\n"
        "\n"
        "🎴 Ideal\n"
        "\n"
        "🎴 Paypal\n"
        "\n"
        "🎴 Cash\n"
    ),
    "faq_contact_info": (
        "️📋 Contact Info:\n"
        "\n"
        "📞 PhoneNumber:     (555) 123-4567\n"
        "✉️ Email:              contact@lucytattoo.com\n"
    ),
    "how_is_our_tattoo_made": (
        "\n"
        "Our Coffee Is made with love and care :\n"
        "\n"
    ),

}

