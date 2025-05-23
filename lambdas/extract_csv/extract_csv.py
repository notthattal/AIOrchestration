import boto3
import pandas as pd
import io

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = event["bucket"]
    key = event["key"]

    # Read CSV into pandas DataFrame
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj["Body"])

    # Filter only 'Id' and 'Text' columns
    df_filtered = df[["Id", "Text"]].dropna()

    # Save to buffer
    csv_buffer = io.StringIO()
    df_filtered.to_csv(csv_buffer, index=False)

    # Upload to new key
    output_key = "processed_data/reviews.csv"
    s3.put_object(Bucket=bucket, Key=output_key, Body=csv_buffer.getvalue())

    return {
        "message": "Processed and saved filtered CSV",
        "output_key": output_key
    }