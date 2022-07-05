import json
import random
from bs4 import BeautifulSoup
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import time
import schedule

# specify discord webhook url below
webhook_url = "https://discord.com/api/webhooks/993701834155900938/yv-aLBqUKuZKeaLud8tCQu7lrcFak8ig7Z9Z6BYQ2Ew-EjiVPqKZa1q4NYNTgHLtgCXM"


#specify amazon product url below
url = "https://www.amazon.in/gp/product/B08N5XSG8Z/ref=ewc_pr_img_1?smid=A14CZOWI0VEHLG&psc=1"

#specify user agent below. can be traced via google
HEADERS = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"}

# declaring and initialising variables outside the function so that they can be used later whenever needed.
product_title = None
price = None

#declaring function
def get_price():

#globalising the variables that were created earlier outside the scope of the function. Global keyword allows you to modify the variable outside of the current scope.
    global product_title
    global price

#requesting the contents of the amazon url specified earlier
    page = requests.get(url, headers=HEADERS)

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
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(description=product_title, color= random.randint(0, 0xffffff))
        embed.set_author(name="Price Drop ALERT!!!!", icon_url='https://c.tenor.com/8vSJsVW-1pQAAAAj/police-car-light-joypixels.gif')
        embed.set_footer(text="Notifed at:")
        embed.set_timestamp()
        embed.set_thumbnail(url='https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/macbook-air-gallery3-20201110?wid=2000&hei=1536&fmt=jpeg&qlt=95&.v=1632937845000')
        embed.add_embed_field(name='Click Link To Buy:', value=url)
        embed.add_embed_field(name='Price:', value= f"INR {price}")
        webhook.add_embed(embed)
        response = webhook.execute()
    else:
        print("price is not affordable enough")



# m1_air()

#scheduling the two functions to run at specified times/intervals.
schedule.every(30).minutes.do(get_price)
schedule.every(31).minutes.do(m1_air)

while True:
    schedule.run_pending()
    time.sleep(1)






