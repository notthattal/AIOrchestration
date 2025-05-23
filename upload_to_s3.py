import pandas as pd
import boto3

def main():
    # Load just the first 10K rows
    df = pd.read_csv("./data/Reviews.csv", nrows=10000)

    # Save to a new CSV file
    df.to_csv("./data/reviews_10k.csv", index=False)

    # Upload to S3
    s3 = boto3.client("s3")
    s3.upload_file("./data/reviews_10k.csv", "ai-orchestration-bucket", "raw_data/reviews.csv")

if __name__=='__main__':
    main()