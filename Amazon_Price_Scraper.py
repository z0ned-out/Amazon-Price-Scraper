import config
import json
import random
from types import NoneType
from bs4 import BeautifulSoup
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import time
import schedule


# declaring and initialising variables outside the function so that they can be used later whenever needed.
product_title = None
price = None

#declaring function
def get_price():

#globalising the variables that were created earlier outside the scope of the function. Global keyword allows you to modify the variable outside of the current scope.
    global product_title
    global price

#requesting the contents of the amazon url specified in the config py
    page = requests.get(config.product_url, headers=config.HEADERS)

#making an instance of beautiful soup, which is a python library to parse HTML/XML documents.
    soup = BeautifulSoup(page.content, 'lxml')

#creating a while loop with try/except statement. Note that the except block of the code below is recursive since it calls the function itself. This is done to overcome the amazon scraping detection in place that prevents from extracting information from elements. So here, the below loop would continue to run until the error resides once and then once it finally resides, the loop breaks itself.
    while True:
        try:
            product_title = soup.find("span", {'id': "productTitle"}).text.strip()
            price = float((soup.find("span",{'class': "a-offscreen"}).text.split("₹")[1]).replace(',',""))
            price = int(price)
            # f = open("Textfile.txt", "w")
            # f.write(product_title + "\n")
            # f.write(f"{price}")
            # f.close()
            break
        except AttributeError:
            get_price()
            break
        
get_price()
print(product_title)
print(price)


#creating another function to post the price and product details that been scraped from Amazon via the above function, to post messages to discord channels using embeds & webhooks.
def m1_air():
    if price < 92900:
        webhook = DiscordWebhook(url=config.webhook_url)
        embed = DiscordEmbed(description=product_title, color= random.randint(0, 0xffffff))
        embed.set_author(name="Price Drop ALERT!!!!", icon_url=config.icon_url)
        embed.set_footer(text="Notifed at:")
        embed.set_timestamp()
        embed.set_thumbnail(url=config.thumbnail_url)
        embed.add_embed_field(name='Click Link To Buy:', value=config.product_url)
        embed.add_embed_field(name='Price:', value= f"INR {price}")
        webhook.add_embed(embed)
        response = webhook.execute()
    else:
        print("price is not affordable enough")



m1_air()

#scheduling the two functions to run at specified times/intervals
schedule.every(30).minutes.do(get_price)
schedule.every(31).minutes.do(m1_air)

while True:
    schedule.run_pending()
    time.sleep(1)






