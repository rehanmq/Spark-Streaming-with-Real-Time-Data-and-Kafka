import time
import requests
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# Replace this with your own NewsAPI key
API_KEY = "24eccd05a5fd40c5a8e6dad91251b7c3"

# Retry Kafka connection
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        print("Kafka connection successful!")
        break
    except NoBrokersAvailable:
        print("Kafka not available, retrying in 5 seconds...")
        time.sleep(5)


def fetch_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        return [
            article["title"] + " " + (article.get("description") or "")
            for article in articles
        ]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


while True:
    news = fetch_news()
    for text in news:
        if text:
            producer.send("topic1", {"text": text})
            print(f"Sent news: {text}")
    time.sleep(60)  # Fetch every minute
