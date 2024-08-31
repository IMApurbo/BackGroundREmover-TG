import telebot
from rembg import remove
from PIL import Image
import io
from telebot import types

# Replace 'YOUR_TOKEN' with your bot's token
TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Send me a photo and I will remove the background!')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Get the photo file
    file_info = bot.get_file(message.photo[-1].file_id)
    photo_bytes = bot.download_file(file_info.file_path)

    # Open the photo with PIL
    image = Image.open(io.BytesIO(photo_bytes))

    # Remove the background
    output_image = remove(image)

    # Ensure the image has an alpha channel
    if output_image.mode != 'RGBA':
        output_image = output_image.convert('RGBA')

    # Save the result to a BytesIO object
    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format='PNG')
    output_bytes.seek(0)

    # Send the result back to the user
    bot.send_photo(message.chat.id, photo=output_bytes, caption='Here is your image with the background removed.')

# Start polling
bot.polling()
