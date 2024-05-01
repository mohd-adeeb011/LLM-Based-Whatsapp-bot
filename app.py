from flask import Flask, request, jsonify
import json
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from pymongo import MongoClient
# from langchain.agents import Tool,create_tool_calling_agent
import asyncio
from threading import Thread
import time
# from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain_openai import ChatOpenAI
from db_helper import query_dish
# from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import OpenAI
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain_core.prompts import MessagesPlaceholder
from dotenv import load_dotenv
# from langchain.agents import initialize_agent
# from langchain.agents.format_scratchpad.openai_tools import (
#     format_to_openai_tool_messages,
# )
# from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from openai import OpenAI
load_dotenv()
import os
app = Flask(__name__)

sid='AC3e292184730e217e546f085c5b697da5'
authToken="3e09df5f2f47432cae7f1d421d2c7c5e"

tclient=Client(sid,authToken)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def searchforDishes(text):
    # dish_cache={}
    # if text in dish_cache:
    #     return dish_cache[text]
    
    # If not in cache, perform the search and store the result
    dishes = query_dish(text)
    # dish_cache[text] = dishes
    return dishes

def PlaceFinalOrder(text):

    with open("order.txt",'w') as f:
        f.write(text)

    return "Order Recorded."

def getFinalOrder():
    with open("order.txt",'r') as f:
        order=f.read()
    orders=[]
    for i in order:
        orders.append(i)
    return orders

class FoodNest:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # self.chat_history = []
    def searchforDishes(self,text):    
        dishes = query_dish(text)
        
        return dishes

    def PlaceFinalOrder(self,text):
        self.chat_history=[]
        with open("order.txt",'w') as f:
            f.write(text)

        return "Order Recorded."

    def getFinalOrder(self):
        with open("order.txt",'r') as f:
            order=f.read()
        orders=[]
        for i in order:
            orders.append(i)
        return orders
    def run_conversation(self, user_prompt):
            self.chat_history = []
            function_discriptions = [
                {
                    "name": "searchforDishes",
                    "description":"Useful when u want you want to fetch restaurant, dish,portion sizing, price, address of restaurant for user. It return at least four Restaurant Name, Dish Name, Portion Sizing, Price in rupees and Address which we have to recomment to user.",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Contain text which is the final order.",
                        },
                    },
                    "required": ["text"],
                    }
                },
            {
                "name": "PlaceFinalOrder",
                "description": "Useful for storing the Final order of the user. It will not return any significant information but, this has to be used when user decided to store the information of the order to finally place the order. Once this function is used, you have to infrom the user that, your order has been placed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Contain text which is probably a keyword or dish to search.",
                        },
                    },
                    "required": ["text"],
                    }
            },
            {
                "name": "getFinalOrder",
                "description": "Retrieves the final order recorded in the text file.",
            }

            ]
            firstmessages = [
                        {"role": "system", "content": "You are a Food Ordering agent, which conversates with user what they want to eat. Your work is to call different functions or tools to do different task like asking user what they want to eat, giving relevant choices, making temporary order, confirming order. So, your flow will be first asking the user what they want to eat then giving them at least 4 choices according to the user requirement, then you have to ask what they want to order, when they tell you what they want to order, you have to store the order in the temporary memory, and add or subtract from the order if user wants, and finally place the order after asking to user and tell the final order to user what they have ordered and store the order in the orderFood function."},
                        {"role": "user", "content": user_prompt}] + self.chat_history
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0613",
                messages=firstmessages,
                functions=function_discriptions,
                function_call="auto",
            )
            response = completion.choices[0].message
            if response.function_call is not None:
                params = json.loads(response.function_call.arguments)
                chosen_function = getattr(self, response.function_call.name)
                weather_content = chosen_function(**params)
                secondmessage=[
                         {"role": "system", "content": "You are a Food Ordering agent, which conversates with user what they want to eat. Your work is to call different functions or tools to do different task like asking user what they want to eat, giving relevant choices, making temporary order, confirming order. So, your flow will be first asking the user what they want to eat then giving them choices according to the user requirement, then you have to ask what they want to order, when the tell you what they want to order, you have to store the order in the temporary memory, and add or subtract from the order if user wants, and finally place the order after asking to user and tell the final order to user what they have ordered and store the order in the orderFood function. Always give complete info of dishes in good text formatting."},
                         {"role": "user", "content": user_prompt},
                        {"role": "function", "name": response.function_call.name, "content": str(weather_content)},
                    ]+self.chat_history
                second_completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=secondmessage,
                    functions=function_discriptions,
                )
                response = second_completion.choices[0].message.content
                print(response)

                self.chat_history.append({"role": "user", "content": user_prompt})
                self.chat_history.append({"role": "assistant", "content": response})

                return response
            else:
                return response.content
@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg=request.form.get("Body",' ').strip().lower()
    receiver_contact=request.form.get("From")
    froms="whatsapp:+14155238886"

    existing_user = get_user_from_db(receiver_contact)
    if existing_user:
        weather_assistant = FoodNest()
        response = weather_assistant.run_conversation(incoming_msg)
        respond(response,receiver_contact,froms)
    else:
        createProfile(incoming_msg,receiver_contact=receiver_contact,froms=froms)
    
    return "OK", 200

def hellofunction(n):
    print(f"Hello world {n}")

def createProfile(incoming_msg, receiver_contact,froms):
    
    print(incoming_msg)
    
    if incoming_msg == 'hello':
        user_state = get_user_state(receiver_contact)
        if user_state is None or user_state['state'] == 'done':
            user_state = {'state': 'name', 'data': {}}
            update_user_state(receiver_contact, user_state)
            respond("What is your name?",receiver_contact,froms)
        else:
            respond("You're already in the process of setting up your profile. Please complete the current step.",receiver_contact,froms)
    else:
        user_state = get_user_state(receiver_contact)
        if user_state is None:
            respond("Hello! Please type 'hello' to start setting up your profile.",receiver_contact,froms)
        elif user_state['state'] == 'name':
            user_state['data']['name'] = incoming_msg
            user_state['state'] = 'dob'
            update_user_state(receiver_contact, user_state)
            respond("What is your DOB?",receiver_contact,froms)
        elif user_state['state'] == 'dob':
            user_state['data']['dob'] = incoming_msg
            user_state['state'] = 'email'
            update_user_state(receiver_contact, user_state)
            respond("What is your email address?",receiver_contact,froms)
        elif user_state['state'] == 'email':
            user_state['data']['email'] = incoming_msg
            user_state['state'] = 'address'
            update_user_state(receiver_contact, user_state)
            respond("What is your address?",receiver_contact,froms)
        elif user_state['state'] == 'address':
            user_state['data']['address'] = incoming_msg
            user_state['state'] = 'pincode'
            update_user_state(receiver_contact, user_state)
            respond("What is your PINCODE?",receiver_contact,froms)
        elif user_state['state'] == 'pincode':
            user_state['data']['pincode'] = incoming_msg
            user_state['state'] = 'Address Desig'
            update_user_state(receiver_contact, user_state)
            respond("Is this you home/office/P.G or anything else?",receiver_contact,froms)
        elif user_state['state'] == 'Address Desig':
            user_state['data']['Address Desig'] = incoming_msg
            user_state['state'] = 'Food Choice'
            update_user_state(receiver_contact, user_state)
            respond("Are you Veg or Non-Veg",receiver_contact,froms)
        elif user_state['state'] == 'Food Choice':
            user_state['data']['Food Choice'] = incoming_msg
            user_state['state'] = 'done'
            update_user_state(receiver_contact, user_state)
            create_user_in_db(receiver_contact, user_state['data'])
            # orderFood(incoming_msg,receiver_contact,froms)
            respond("Thank you! Your profile has been created. What do you want to eat.",receiver_contact,froms)
        else:
            respond("Hello! Please type 'hello' to start setting up your profile.",receiver_contact,froms)
    return "Completed"

# def orderFood(incoming_msg,receiver_contact, froms):
#     text=f"Your {incoming_msg} is uder process."
#     respond(text,receiver_contact,froms)
    

def respond(message,receiver_contact,froms):
    # client.messages.create(body=message, to=receiver_contact)
    _ = tclient.messages.create(
        from_=froms,
        body=message,
        to=receiver_contact
    )

def get_user_from_db(senderId):
    mongodb_client = connect_to_mongodb()
    if mongodb_client is None:
        return None
    db = mongodb_client.get_database('FoodNest')
    collection = db.get_collection('User')
    existing_user = collection.find_one({'phone_number': senderId})
    return existing_user

def get_user_state(senderId):
    mongodb_client = connect_to_mongodb()
    db = mongodb_client.get_database('FoodNest')
    collection = db.get_collection('UserState')
    existing_state = collection.find_one({'phone_number': senderId})
    return existing_state

def update_user_state(senderId, user_state):
    mongodb_client = connect_to_mongodb()
    db = mongodb_client.get_database('FoodNest')
    collection = db.get_collection('UserState')
    collection.update_one({'phone_number': senderId}, {'$set': user_state}, upsert=True)

def create_user_in_db(senderId, user_data):
    mongodb_client = connect_to_mongodb()
    db = mongodb_client.get_database('FoodNest')
    collection = db.get_collection('User')
    user_data['phone_number'] = senderId
    collection.insert_one(user_data)

def connect_to_mongodb():
    uri = "mongodb+srv://mohdadeeb110:mongodb123#@cluster0.8ibfe9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        # print("Connected to MongoDB successfully!")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")  
        return None

if __name__ == "__main__":
    app.run(port=5000, debug=True)