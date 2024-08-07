from aiogram.utils.i18n import gettext as _

GREETING_ENG = ('''
Hello! 👋 Welcome to FlySaverBot! ✈️

I will help you find the cheapest airline tickets and track price changes for your favorite flights.

Here’s what I can do:
🔍 Ticket search: Enter the departure city, destination, and travel dates.
💼 Favorite flights: Save a flight to favorites to track its price.
📉 Notifications: Get notifications about price drops and increases for your favorite flights.

Shall we begin? Enter a command or departure city to find tickets!
''').strip()

ABOUT_BOT_ENG = "FlySaverBot helps you find and track cheap airline tickets. Developer: Danyil Kozlov - @leyofficial."


HELP_ENG = ('''
    Command list:

    /start - Start the bot and welcome message.
    /help - Information about available commands and how to use the bot.
    /search - Search for airline tickets.
    /favorites - View list of favorite flights.
    /track - Add a flight to favorites.
    /untrack - Remove a flight from favorites.
    /notifications - Set up notifications.
    /settings - Bot settings.
    /about - About the bot.
    ''')


FLIGHT_DETAILS_TEMPLATE_ENG = (
    "🛫 **Airline:** {company}\n"
    "📍 **From:** {departure_city}\n"
    "📍 **To:** {arrival_city}\n"
    "🕒 **Duration:** {duration}\n"
    "📅 **Departure Date:** {departure_date}\n"
    "📅 **Return Date:** {return_date}\n"
    "⏰ **Departure Time:** {departure_time}\n"
    "⏰ **Arrival Time:** {arrival_time}\n"
    "💵 **Price:** {price}\n"
)


FINISHED_SEARCH_ENG = (
    "🎉 **Search Complete!**\n\n"
    "🚀 Thank you for using our bot to search for airline tickets. "
    "We were happy to help you find a suitable flight.\n\n"
    "🗂️ Your data has been cleared, and the search is complete.\n\n"
    "🔄 **New search:** You can start a new search right now. "
    "Just click the button below!"
)
