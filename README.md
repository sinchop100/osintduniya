Telegram OSINT Bot
A Python-based Telegram bot that uses the OSINT Industries API to search for usernames, emails, and phone numbers. The bot generates a unique virtual user ID and device ID for each user and supports session cookies and user-agent headers for API requests.

Features
Search for user details using a username, email, or phone number.
Automatically generates a virtual user ID and device ID for each user.
Supports session cookies and user-agent headers.
Fetches and displays images related to the search results, if available.
Prerequisites
Python 3.x
Termux (for running the bot on Android)
Git (for cloning the project repository)
Installation
1. Install Termux
Install Termux from the Google Play Store or F-Droid.

2. Install Python and Git in Termux
Open Termux and install Python and Git:

bash
Copy code
pkg update
pkg upgrade
pkg install python git
3. Clone the Repository
Clone the GitHub repository and navigate into the project directory:

bash
Copy code
git clone https://github.com/yourusername/telebot_project.git
cd telebot_project
4. Install the Required Libraries
Install the required Python libraries listed in the requirements.txt file:

bash
Copy code
pip install -r requirements.txt
5. Add Bot Token and OSINT API Key
Before running the bot, make sure to update the following variables in the bot.py file:

Replace API_TOKEN with your Telegram bot token from BotFather.
Replace OSINT_API_KEY with your OSINT Industries API key.
6. Run the Bot
Once everything is set up, run the bot using:

bash
Copy code
python bot.py
Usage
Once the bot is running, you can interact with it on Telegram using the following commands:

/start - Initialize the bot and receive your virtual ID and device ID.
/search_username <username> - Search for details using a username.
/search_email <email> - Search for details using an email address.
/search_number <phone number> - Search for details using a phone number.
Example commands:

bash
Copy code
/search_username johndoe
/search_email example@mail.com
/search_number +123456789
Running in the Background (Optional)
To keep the bot running in the background on Termux, use tmux:

Install tmux:

bash
Copy code
pkg install tmux
Start a new tmux session:

bash
Copy code
tmux new -s mybot
Run the bot inside the tmux session.

Detach the tmux session (Ctrl+B, then D).

To reattach the session later:

bash
Copy code
tmux attach-session -t mybot
Project Structure
bash
Copy code
telebot_project/
├── bot.py              # Main bot script
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request with your improvements or new features.
