# Image Insight Bot

Image Insight Bot is a simple Telegram bot designed to identify and describe images. Users can send an image to the bot, and it will provide information about the contents of the image.

## Features

- Image identification using a pre-trained model
- Telegram integration for easy interaction

## Requirements

Ensure you have the following requirements installed before running the bot:

```bash
pip install torch torchvision python-telegram-bot Pillow
``



# Hardware Used

## Model
The bot uses a pre-trained image identification model. The current version of the bot uses a custom-trained model on the CIFAR-10 dataset. The PyTorch framework is utilized for the model implementation.

## Usage                                            
Clone the repository:
git clone 
cd image-insight-bot

Install the required dependencies:
pip install -r requirements.txt

Run the bot:
python imageinsightbot.py



Interact with the bot on Telegram by sending images for identification.
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
