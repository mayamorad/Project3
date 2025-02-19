import pandas as pd
from pymongo import MongoClient

# Define MongoDB Atlas connection
MONGO_URI = "mongodb+srv://chrisbushelman:i7wPfB8sRMNlsCQT@cluster0.0gkw8.mongodb.net/"

# Connect to MongoDB Atlas
mongo = MongoClient(MONGO_URI)
db = mongo['Project_3']  # Use your actual database name

# Load data from MongoDB
def load_data(collection_name):
    collection = db[collection_name]
    document = collection.find_one({}, {"_id": 0})  # Retrieve the single document
    
    all_data = []
    
    if document:  # Ensure data exists
        for ticker, details in document.items():  # Iterate through ticker keys
            if isinstance(details, dict):  # Ensure it's an object
                company_name = details.get("Company Name", "Unknown")
                market_cap = details.get("Market Cap", "Unknown")
                address = details.get("Address", "Unknown")
                city = details.get("City", "Unknown")
                state = details.get("State", "Unknown")
                country = details.get("Country", "Unknown")
                
                if "Stock Data" in details:
                    for entry in details["Stock Data"]:
                        all_data.append({
                            "Ticker": ticker,
                            "Company Name": company_name,
                            "Market Cap": market_cap,
                            "Address": address,
                            "City": city,
                            "State": state,
                            "Country": country,
                            "Date": entry.get("Date"),
                            "Close": entry.get("Close")
                        })
    
    return pd.DataFrame(all_data)

# Extract data from both Trump_Presidency and Biden_Presidency collections
df_trump = load_data("Trump_Presidency")
df_biden = load_data("Biden_Presidency")

# Print DataFrames
print("Trump DataFrame:")
print(df_trump.head())

print("Biden DataFrame:")
print(df_biden.head())
