import findspark

findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, udf, from_json, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define JSON schema because Kafka value is JSON
schema = StructType([StructField("text", StringType(), True)])

# Spark session
spark = SparkSession.builder.appName("KafkaNERStreaming").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Read from Kafka topic1
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "topic1")
    .load()
)

# Convert Kafka's byte values into String and JSON parse
df = df.selectExpr("CAST(value AS STRING) as json_str")
df = df.withColumn("data", from_json(col("json_str"), schema)).select("data.text")


# Extract named entities
def get_entities(text):
    doc = nlp(text if text else "")
    return [ent.text for ent in doc.ents]


entity_udf = udf(get_entities, ArrayType(StringType()))

entities_df = df.withColumn("entities", entity_udf(col("text"))).select(
    explode(col("entities")).alias("entity")
)

# Count entities
entity_counts = entities_df.groupBy("entity").count()

# Correct way: Write entity + count as JSON into Kafka topic2
query = (
    entity_counts.select(to_json(struct(col("entity"), col("count"))).alias("value"))
    .writeStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("topic", "topic2")
    .option("checkpointLocation", "/tmp/spark_checkpoint")
    .outputMode("complete")
    .start()
)

query.awaitTermination()
