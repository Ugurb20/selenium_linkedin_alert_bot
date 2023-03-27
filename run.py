from bot.scraper import Booking


with Booking() as bot:
    bot.land_first_page()
    bot.login()
    bot.search()
    bot.scrap_jobs()

print("Bot finished....")