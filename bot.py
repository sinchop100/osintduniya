import telebot
import requests
import uuid  # For generating virtual user IDs

# Your Bot Token from BotFather
API_TOKEN = '7186439291:AAF0kKZCQfsEBvQ2CeucwE3oMzxqs3eC0Cg'
# Your OSINT API Key
OSINT_API_KEY = '7eabdc5f4568eed060134fe9a487230b'
BASE_URL = 'https://api.osint.industries/v1/search'

# Initialize bot
bot = telebot.TeleBot(API_TOKEN)

# Create a dictionary to store user data and virtual IDs
users = {}

# Function to create or retrieve a virtual ID and device ID for the user
def get_user_data(user_chat_id):
    if user_chat_id not in users:
        user_uuid = str(uuid.uuid4())  # Generate a new UUID for the user (Virtual ID)
        device_id = str(uuid.uuid4())  # Generate a new UUID for the device (Device ID)
        users[user_chat_id] = {
            'virtual_id': user_uuid,
            'device_id': device_id,
            'search_history': []  # Store search history if needed
        }
    return users[user_chat_id]

# Create a session object to store cookies
session = requests.Session()

# Function to make API requests with cookies, user agent, and device ID
def osint_search(query_type, query_value, device_id):
    headers = {
        'Authorization': f'Bearer {OSINT_API_KEY}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Device-ID': device_id  # Custom header to send device ID
    }
    params = {
        'type': query_type,
        'term': query_value
    }
    try:
        response = session.get(BASE_URL, headers=headers, params=params)  # Use session for cookies
        response.raise_for_status()  # Ensure we catch HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as err:
        if response.status_code == 451:
            return {'error': 'Unavailable For Legal Reasons'}
        else:
            return {'error': str(err)}
    except Exception as e:
        return {'error': f'Unknown error: {str(e)}'}

# Command: /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = get_user_data(message.chat.id)
    bot.reply_to(message, f"Welcome! Your Virtual ID is: {user_data['virtual_id']} and Device ID is: {user_data['device_id']}\n"
                          "Use the following commands to search:\n"
                          "/search_username <username>\n"
                          "/search_email <email>\n"
                          "/search_number <number>")

# Search by username
@bot.message_handler(commands=['search_username'])
def search_username(message):
    user_data = get_user_data(message.chat.id)
    username = message.text.split()[1] if len(message.text.split()) > 1 else None
    if username:
        result = osint_search('username', username, user_data['device_id'])
        if result and 'error' not in result and result.get('data'):
            if 'image_url' in result['data']:
                bot.send_photo(message.chat.id, result['data']['image_url'])
            else:
                bot.reply_to(message, f"Details for {username}: {result['data']}\nNo image available for this result.")
        elif result and 'error' in result:
            if result['error'] == 'Unavailable For Legal Reasons':
                bot.reply_to(message, f"Search for {username} is unavailable due to legal restrictions.")
            else:
                bot.reply_to(message, f"An error occurred: {result['error']}")
        else:
            bot.reply_to(message, f"No details found for username: {username}.")
        users[message.chat.id]['search_history'].append({'type': 'username', 'term': username})
    else:
        bot.reply_to(message, "Please provide a username to search. Example: /search_username johndoe")

# Search by email
@bot.message_handler(commands=['search_email'])
def search_email(message):
    user_data = get_user_data(message.chat.id)
    email = message.text.split()[1] if len(message.text.split()) > 1 else None
    if email:
        result = osint_search('email', email, user_data['device_id'])
        if result and 'error' not in result and result.get('data'):
            if 'image_url' in result['data']:
                bot.send_photo(message.chat.id, result['data']['image_url'])
            else:
                bot.reply_to(message, f"Details for {email}: {result['data']}\nNo image available for this result.")
        elif result and 'error' in result:
            if result['error'] == 'Unavailable For Legal Reasons':
                bot.reply_to(message, f"Search for {email} is unavailable due to legal restrictions.")
            else:
                bot.reply_to(message, f"An error occurred: {result['error']}")
        else:
            bot.reply_to(message, f"No details found for email: {email}.")
        users[message.chat.id]['search_history'].append({'type': 'email', 'term': email})
    else:
        bot.reply_to(message, "Please provide an email to search. Example: /search_email example@mail.com")

# Search by phone number
@bot.message_handler(commands=['search_number'])
def search_number(message):
    user_data = get_user_data(message.chat.id)
    number = message.text.split()[1] if len(message.text.split()) > 1 else None
    if number:
        result = osint_search('phone', number, user_data['device_id'])
        if result and 'error' not in result and result.get('data'):
            if 'image_url' in result['data']:
                bot.send_photo(message.chat.id, result['data']['image_url'])
            else:
                bot.reply_to(message, f"Details for {number}: {result['data']}\nNo image available for this result.")
        elif result and 'error' in result:
            if result['error'] == 'Unavailable For Legal Reasons':
                bot.reply_to(message, f"Search for {number} is unavailable due to legal restrictions.")
            else:
                bot.reply_to(message, f"An error occurred: {result['error']}")
        else:
            bot.reply_to(message, f"No details found for phone number: {number}.")
        users[message.chat.id]['search_history'].append({'type': 'phone', 'term': number})
    else:
        bot.reply_to(message, "Please provide a phone number to search. Example: /search_number +123456789")

# Start the bot
bot.polling()
