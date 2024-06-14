from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import cv2
from tensorflow.keras.applications.resnet50 import ResNet50
import numpy as np
from labels import lbl
import os
from datetime import datetime
import dotenv
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# accessing and printing value
print(os.getenv("mykey"))

import pyfiglet
from pyfiglet import Figlet

f = Figlet(font='slant')

def print_figlet(text):
    print(f.renderText(text))

print_figlet('Hello, Mr Mokkarala !')

model = ResNet50()

def start(updater, context): 
	updater.message.reply_text("Welcome to the classification bot!")

def help_(updater, context): 
	updater.message.reply_text("Just send the image you want to classify. - Not 100 % accurate.")

def message(updater, context):  # This function is called whenever the bot receives a message
	msg = updater.message.text
	print(msg)
	updater.message.reply_text(msg)

def image(updater, context):
    # Create a folder to store images if it doesn't exist
    if not os.path.exists("User_data"):
        os.makedirs("User_data")

    photo = updater.message.photo[-1].get_file()
    photo_path = os.path.join("User_data", "img.jpg")  # Save the image in the folder
    photo.download(photo_path)

    img = cv2.imread(photo_path)

    img = cv2.resize(img, (224, 224))
    img = np.reshape(img, (1, 224, 224, 3))

    pred = np.argmax(model.predict(img))

    pred = lbl[pred]

    print(pred)

    updater.message.reply_text(pred)

    # Move the saved image to a new unique filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_photo_path = os.path.join("User_data", f"img_{timestamp}.jpg")
    os.rename(photo_path, new_photo_path)



telegram_bot_api_token = os.getenv("telegram_bot_api_token")

updater = Updater(telegram_bot_api_token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_))

dispatcher.add_handler(MessageHandler(Filters.text, message))

dispatcher.add_handler(MessageHandler(Filters.photo, image))


updater.start_polling()
updater.idle()