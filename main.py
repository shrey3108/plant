import telebot
import requests
import traceback

Token = '7094792264:AAEH-QrZhteAOaFoHoCZEk54iyzhud1Tck4'
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Please send an image or video for disease detection.")

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{Token}/{file_info.file_path}"

        # Send the image to Flask API for disease detection
        response = requests.post("http://127.0.0.1:5000/upload_image", files={"image": requests.get(file_url).content})
        data = response.json()

        # Get the disease prediction and solution from Flask API response
        if "message" in data:
            bot.reply_to(message, data["message"])
        else:
            # Extract disease name, confidence, and solution from the Flask API response
            disease_name = data.get("disease_name", "Unknown Disease")
            confidence = data.get("confidence", 0.0)
            solution = data.get("solution", "No solution available.")

            # Send the disease prediction and solution to the user
            bot.reply_to(message, f"Disease: {disease_name}\nConfidence: {confidence}\nSolution: {solution}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{Token}/{file_info.file_path}"

        # Send the video to Flask API for disease detection
        response = requests.post("http://127.0.0.1:5000/upload_image", files={"file": requests.get(file_url).content})
        data = response.json()

        # Get the disease prediction and solution from Flask API response
        if "message" in data:
            bot.reply_to(message, data["message"])
        else:
            # Extract disease name, confidence, and solution from the Flask API response
            disease_name = data.get("disease_name", "Unknown Disease")
            confidence = data.get("confidence", 0.0)
            solution = data.get("solution", "No solution available.")

            # Send the disease prediction and solution to the user
            bot.reply_to(message, f"Disease: {disease_name}\nConfidence: {confidence}\nSolution: {solution}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()


try:
    bot.polling()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
