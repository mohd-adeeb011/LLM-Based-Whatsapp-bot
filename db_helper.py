from pymongo import MongoClient
from pymongo.server_api import ServerApi
from openai import OpenAI
from data import restaurants
from dotenv import load_dotenv
load_dotenv()
import os

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

restaurants_data=restaurants

def add_restaurant_data(restaurants_data):
    restaurants = restaurants_data

    mongodb_client = connect_to_mongodb()
    if mongodb_client is None:
        return
    db = mongodb_client.get_database('FoodNest')
    collection = db.get_collection('Dishes')
    collection.insert_many(restaurants)
    print("Restaurant Data added Successfully.")

    for restaurant in restaurants:
        # Assuming 'menu' is now an object, not an array
        dish = restaurant['menu']
        key_embeddings = generate_embedding(' '.join(dish['key']))
        
        # Update the embeddings for the dish within the menu
        collection.update_one(
            {'_id': restaurant['_id']},
            {'$set': {'embeddings': key_embeddings}}
        )

    return "Restaurants Data and Embeddings Successfully stored."

def generate_embedding(text: str) -> list[float]:
    model='text-embedding-3-small'
    print("Embedding Started")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def connect_to_mongodb():
    uri = "mongodb+srv://mohdadeeb110:mongodb123#@cluster0.8ibfe9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")  
        return None
    
    
def query_dish(query):
    mongodb_client = connect_to_mongodb()
    if mongodb_client is None:
        return
    db = mongodb_client.get_database('FoodNest')
    collection = db.get_collection('Restaurants')
    # print("Vector Searching started.")
    embeddings=generate_embedding(query)
    # print(embeddings)
    result=db.Dishes.aggregate([
        {
            "$vectorSearch": {
            "index": "dishes_index",
            "path": "embeddings",
            "queryVector": embeddings,
            "numCandidates": 100,
            "limit": 4
            }
        }
        ])
    dishes = {}
    for index, i in enumerate(result, start=1):
        dish_info = {
            "Restaurant": i["name"],
            "Dish": i["menu"]["name"],
            "Portion_sizing": i["menu"]["portion_sizing"],
            "Price": i["menu"]["price"],
            "Address": i["address"]
        }
        dishes[index] = dish_info
    return dishes
    
def deconstructing():
    mongodb_client = connect_to_mongodb()
    if mongodb_client is None:
        return
    db = mongodb_client.get_database('FoodNest')
    print("aggregation started")
    db.Restaurants.aggregate([
        { "$unwind": "$menu" },
        { "$project": { "_id": 0 } },
        { "$out": "flattenedRestaurants" }
        
    ])
    return "Deconstructing done."


if __name__ == "__main__":
    print("Hello World")
    # print(add_restaurant_data(restaurants_data))

    response=query_dish("Chicken me kya kay hai.")
    results = list(response)
    if len(results) == 0:
        print("Empty Cursor")
    else:
        print("Cursor is Not Empty")
    dishes = {}
    for index, i in enumerate(results, start=1):
        dish_info = {
            "Restaurant": i["name"],
            "Dish": i["menu"]["name"],
            "Portion_sizing": i["menu"]["portion_sizing"],
            "Price": i["menu"]["price"],
            "Address": i["address"]
        }
        dishes[index] = dish_info
    print(dishes)