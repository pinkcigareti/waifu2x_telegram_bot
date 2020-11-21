import telebot
import requests
import json
import urllib

bot = telebot.TeleBot("TELEGRAM_TOKEN")


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Waifu2x Telegram Bot \n \n How to use: send photo")
    pass


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        photo_info = bot.get_file(message.photo[0].file_id)
        downloaded_file = bot.download_file(photo_info.file_path)
        src = 'Your path to output image' + message.photo[0].file_id
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            r = requests.post(
                "https://api.deepai.org/api/waifu2x",
                files={
                    'image': downloaded_file,
                },
                headers={'api-key': 'YOUR_API_KEY'}
            )
            data1 = json.dumps(r.json())
            data2 = json.loads(data1)
        bot.reply_to(message, "Please wait")
        url = data2['output_url']
        f = open('output.png', 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()
        photo = open('output.png', 'rb')

        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "Done. Enjoy")

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'Your path to output image' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            r = requests.post(
                "https://api.deepai.org/api/waifu2x",
                files={
                    'image': downloaded_file,
                },
                headers={'api-key': 'YOUR_API_KEY'}
            )
            data1 = json.dumps(r.json())
            data2 = json.loads(data1)
        bot.reply_to(message, "Please wait")
        url = data2['output_url']
        f = open('output.png', 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()
        doc = open('output.png', 'rb')

        bot.send_document(message.chat.id, doc)
        bot.send_message(message.chat.id, "Done. Enjoy")

    except Exception as e:
        bot.reply_to(message, e)


bot.polling()
