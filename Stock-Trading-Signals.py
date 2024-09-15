import json
import requests
from kafka import KafkaConsumer, KafkaProducer
import pandas as pd

# Constants
API_KEY = 'YOUR_API_KEY'  # Place your Alpha Vantage API key here
STOCK_SYMBOL = 'IBM'
URL = "https://www.alphavantage.co/query"

# Setup Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Function to fetch stock data
def fetch_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(URL, params=params)
    data = response.json()
    return data['Time Series (5min)']

# Function to publish stock data to Kafka
def produce_data():
    stock_data = fetch_stock_data(STOCK_SYMBOL)
    for time_stamp, data in stock_data.items():
        message = {'timestamp': time_stamp, 'price': float(data['4. close'])}
        producer.send('stock_prices', value=message)
        print(f"Sent data: {message}")

# Setup Kafka consumer
consumer = KafkaConsumer(
    'stock_prices',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Function to consume data and calculate MA50
# Function to consume data and calculate MA50
def consume_and_calculate_ma50():
    prices = pd.DataFrame(columns=['timestamp', 'price'])
    for message in consumer:
        new_data = pd.DataFrame([message.value])  # Convert the message value to a DataFrame
        prices = pd.concat([prices, new_data], ignore_index=True)  # Use pd.concat to add the new data

        # Calculate MA50 if we have at least 50 data points
        if len(prices) >= 50:
            prices['MA50'] = prices['price'].rolling(window=50).mean()
            current_price = prices.iloc[-1]['price']
            ma50 = prices.iloc[-1]['MA50']

            # Trading logic
            if current_price > ma50:
                print(f"Buy signal at {new_data['timestamp'].item()}")
            elif current_price < ma50:
                print(f"Sell signal at {new_data['timestamp'].item()}")


# Function to run the producer and consumer
if __name__ == "__main__":
    produce_data()  # You might want to run this in a separate thread or process
    consume_and_calculate_ma50()
