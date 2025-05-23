import boto3
import pandas as pd
import io
from textblob import TextBlob

s3 = boto3.client("s3")

def classify(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def lambda_handler(event, context):
    bucket = event["bucket"]
    key = "processed_data/reviews.csv"

    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj["Body"])

    df["Sentiment"] = df["Text"].astype(str).apply(classify)

    # Write to processed_data/sentiment.csv
    out_key = "processed_data/sentiment.csv"
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=out_key, Body=csv_buffer.getvalue())

    return {
        "message": "Sentiment analysis complete",
        "output_key": out_key
    }