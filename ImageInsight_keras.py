from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import io

# Replace with your actual Telegram bot token
TOKEN = "your_token_here"

# Path to your h5 model file
MODEL_PATH = 'cifar10.h5'

# Load the pre-trained model
model = load_model(MODEL_PATH)

def predict_image(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        # Download the photo
        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        file_data = file.download_as_bytearray()

        # Convert downloaded data to PIL Image
        image_data = Image.open(io.BytesIO(file_data))

        # Preprocess the image for prediction
        image_tensor = image.img_to_array(image_data.resize((32, 32)))
        image_tensor = image_tensor / 255.0
        image_tensor = image_tensor.reshape((1, 32, 32, 3))

        # Make a prediction using the model
        prediction = model.predict(image_tensor)
        predicted_class = np.argmax(prediction)

        # Map predictions to class names (adjust these if needed)
        class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

        # Send prediction to Telegram chat
        update.message.reply_text(f"Predicted Class: {class_names[predicted_class]}")
    else:
        update.message.reply_text('Please send an image for classification.')

def main() -> None:
    # Use the update queue with Updater
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(MessageHandler(Filters.photo, predict_image))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
