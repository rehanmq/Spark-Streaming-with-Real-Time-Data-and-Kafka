# Real-Time Named Entity Recognition Streaming Pipeline

This project builds a real-time streaming pipeline to extract and visualize the most frequently mentioned named entities from live news articles.

We used:

- NewsAPI to fetch real-time news
- Apache Kafka for message streaming
- Apache Spark Structured Streaming for Named Entity Recognition (NER)
- Logstash to ship data into Elasticsearch
- Elasticsearch to store the data
- Kibana to visualize top named entities

---

## How to Run the Project

1. Make sure Docker and Docker Compose are installed on your machine.
2. Open a terminal inside the directory.
3. Run the following command to start the entire setup:

```bash
docker-compose up --build -d
```

This will start:

- Zookeeper
- Kafka
- Elasticsearch
- Kibana
- Logstash
- News Producer
- Spark App

4. Open Kibana in your browser:

```
http://localhost:5601
```

5. Create a new index pattern:

- Go to **Management → Stack Management → Data Views**.
- Create a new data view for `ner-entities*`.
- No time field is required.

6. Visualize the Data:

- Use Kibana Lens to create a bar chart.
- Set X-Axis to `entity.keyword` (Top 10 values).
- Set Y-Axis to Sum of `count`.
- No breakdown.
- Label the axes for clarity.

---

## Notes

- The News Producer fetches articles about random topics (technology, sports, health, politics, etc.) every minute.
- Spark extracts named entities from the news text and counts how often they are mentioned.
- Logstash parses and ships the entity counts into Elasticsearch.
- Kibana visualizes the live entity mentions.

<!-- # Project Report: Real-Time Named Entity Recognition Pipeline -->

## Data Source

We used [NewsAPI](https://newsapi.org/) to fetch real-time news articles.
Instead of just fetching top headlines, the producer queries random keywords (technology, sports, business, health, politics, etc.) using the `/v2/everything` endpoint.
This ensures more diverse news articles come through the stream.

---

## Pipeline Components

- **Producer**: A Python application that fetches fresh news articles every minute and sends them into Kafka topic `topic1`.
- **Spark Structured Streaming App**: Reads from Kafka topic `topic1`, uses SpaCy to extract named entities from the text, counts the entities, and writes the counts to Kafka topic `topic2`.
- **Logstash**: Consumes from Kafka topic `topic2`, parses the JSON entity counts, and ships them into Elasticsearch.
- **Elasticsearch**: Stores the named entities and their counts.
- **Kibana**: Visualizes the top 10 most frequently mentioned entities over time.

All components were containerized using Docker for a smooth setup.

---

## Results and Observations

We captured the bar plots of top named entities at different time intervals:

| Time Interval    | Observations                                                                                 |
| :--------------- | :------------------------------------------------------------------------------------------- |
| After 15 minutes | Entities like "KSL-news", "1-year-old", and "10" were dominant from tech and political news. |
| After 30 minutes | More sports and health-related entities appeared as news topics rotated.                     |
| After 45 minutes | Education and business-related entities started showing up.                                  |
| After 60 minutes | A well-distributed range of entities from multiple topics was visible.                       |

Entities changed based on the random topics fetched, showing that the pipeline adapted to incoming live data dynamically.

---

## Challenges and Improvements

- **Duplicate News**: Initially the news fetched repeated every minute. Solved by switching from `/v2/top-headlines` to `/v2/everything` and adding random keyword searches.
- **Kibana Visualization**: Adjusted to show Top 10 entities cleanly without breakdown confusion.


Spark Streaming with Real Time Data and Kafka

<img width="1900" height="895" alt="15 minutes" src="https://github.com/user-attachments/assets/dc7858d0-aa3f-477e-8bba-69709276470c" />


<img width="1900" height="895" alt="15 minutes" src="https://github.com/user-attachments/assets/c5e912c3-bba9-4e06-bfaa-aebf7537f7f5" />


<img width="1900" height="898" alt="45 minutes" src="https://github.com/user-attachments/assets/cd5fc7bd-a659-4fc3-9727-0ae56d96f7b6" />


<img width="1900" height="886" alt="60 minutes" src="https://github.com/user-attachments/assets/a67e1f55-8801-4539-8742-9103d3ecd8ed" />
