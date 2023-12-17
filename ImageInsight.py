from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from telegram import Update
from torchvision import transforms
from PIL import Image
import torch
from torch import nn
import os

# Replace with the actual path to your PyTorch model file
MODEL_PATH = 'cifar10_model.pth'
# Define the transformation for the input image
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])

# Define the CIFAR-10 model
class SimpleCIFAR10Model(nn.Module):
    def __init__(self):
        super(SimpleCIFAR10Model, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 8 * 8, 128)  # Adjusted the size here
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load the CIFAR-10 model
model = SimpleCIFAR10Model()
model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
model.eval()

# Telegram bot token (replace with your actual token)
TOKEN = 'use_your_own_token'

def classify_image(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        # Create the 'downloads' directory if it doesn't exist
        os.makedirs("downloads", exist_ok=True)

        # Download the photo
        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        image_path = f"downloads/{file_id}.jpg"  # Adjust the path as needed
        file.download(image_path)

        # Open and preprocess the image
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0)

        # Make a prediction using the model
        with torch.no_grad():
            output = model(image_tensor)
            _, predicted_class = torch.max(output, 1)
            prediction = f"Predicted Class: {predicted_class.item()}"

        update.message.reply_text(prediction)
    else:
        update.message.reply_text('Please send an image for classification.')

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the MessageHandler to handle photo messages
    dispatcher.add_handler(MessageHandler(Filters.photo, classify_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
