# LLM-Based WhatsApp Bot for Food Ordering System
Welcome to the LLM-Based WhatsApp Bot for Food Ordering System repository! This project aims to provide users with a convenient way to query dishes and restaurant information using multilingual natural language prompts on WhatsApp. The bot is built using various technologies including Flask, Twilio, MongoDB Atlas, and the OpenAI API.

## Features
- **Multilingual Natural Language Processing:** Users can interact with the bot using natural language prompts in multiple languages.
- **Query Dishes and Restaurants:** Users can query information about dishes and restaurants, including names, portion sizing, prices, and addresses.
- **Order Placement:** Users can place orders for dishes through the bot, and the bot records and confirms the orders.
- **Integration with WhatsApp:** The bot interacts with users via WhatsApp, providing a familiar and accessible platform for communication.
## Technologies Used
- **Flask:** Flask is used to develop the web application framework for the bot.
- **Twilio:** Twilio provides the API for integrating WhatsApp messaging functionality into the bot.
- **MongoDB Atlas:** MongoDB Atlas is used as the cloud database to store restaurant and user data.
- **OpenAI API:** The OpenAI API is utilized for natural language processing and conversation generation.
- **QR Code Generator:** A QR code is generated to provide users with an entry point to interact with the bot on WhatsApp.

## Installation
- **To run the bot locally, follow these steps:**
- **Clone the repository to your local machine:** git clone https://github.com/mohd-adeeb011/LLM-Based-Whatsapp-bot.git
- **Install the required dependencies:** pip install -r requirements.txt
- **Set up environment variables:** Create a .env file in the root directory of the project and add the following variables:
OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
**Run the Flask application:**
- python app.py
- Expose the Flask application to the internet (e.g., using ngrok) to receive incoming messages from WhatsApp.

## Usage
- Use the provided QR code (whatsapp_qr1.png) to access the bot on WhatsApp.
- Start a conversation with the bot by sending a message containing your query or order.
- Follow the prompts provided by the bot to interact and place your orde
