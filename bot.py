import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import uuid
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("token"), parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=["say"])
def say(message):
    if message.reply_to_message and message.reply_to_message.text != "":
        img = Image.open("image.jpg")
        I1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype(font="Vazirmatn-Thin.ttf", size=500)
        I1.text((1800, 1000), message.reply_to_message.text, font=myFont, fill=(0, 0, 0))
        new_image = str(uuid.uuid4())+".jpg"
        img.save(new_image)
        ret_msg = bot.send_photo(message.chat.id, open(new_image, 'rb'))
        os.remove(new_image)
    elif message.text.removeprefix("/say") == "":
        bot.reply_to(message, "please type a text after /say")
    else:
        img = Image.open("image.jpg")
        I1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype(font="Vazirmatn-Thin.ttf", size=500)
        I1.text((1800, 1000), message.text.removeprefix("/say"), font=myFont, fill=(0, 0, 0))
        new__image = str(uuid.uuid4())+".jpg"
        img.save(new__image)
        ret_msg = bot.send_photo(message.chat.id, open(new__image, 'rb'))
        os.remove(new__image)


@bot.message_handler(commands=["flight"])
def flight(message):
    text = message.text.split(" ")
    if len(text) != 4:
        bot.reply_to(message, "i need from city and to city and date(example: /flight tehran bushehr 1402-07-07)")
        return
    _, source, destination, date = text
    '''
    source = text[1]
    destination = text[2]
    date = text[3]
    '''
    URL = "https://mz724.ir/Ticket-" + source + "-" + destination + ".html?t=" + date
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    all_flight = soup.find("div", {"class": "fromtab_container"})
    all_flights = soup.find_all("div", {"class": "resu", "data": "0"})
    all_response = []
    for flight in all_flights:
        flight_time = flight.find("div", {"class": "date"})
        flight_price = flight.find("span")
        flight_seat = flight.find("div", {"class": "user"})
        response = [flight_time.text.strip(), flight_price.text.strip(), flight_seat.text.strip()]
        response = "\n".join(response)
        all_response.append(response)
    if not all_response:
        bot.reply_to(message, "data not found")
        return
    bot.reply_to(message, "\n-----\n".join(all_response))


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    img = message.photo[3]
    file_info = bot.get_file(img.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image = str(uuid.uuid4())+".jpg"
    with open(image, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = Image.open(image)
    I1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype(font="Vazirmatn-Thin.ttf", size=50)
    I1.text((600, 350), "hi", font=myFont, fill=(0, 0, 0))
    img.save(image)
    ret_msg = bot.send_photo(message.chat.id, open(image, 'rb'))
    os.remove(image)


bot.infinity_polling()
