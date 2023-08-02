import sys

import boto3
import os
import datetime
import logging
import json

"""
Different filetypes (e.g. funds, prices) would be placed in different prefixes,
by use of prefix in the rule - currently this is hardcoded to avoid cost of deploying lots of lambda functions
todo add aws lambda powertools
"""
logger = logging.getLogger()
logger.info("Initialising instance... imports complete")

source_bucket = os.environ.get("SOURCE_BUCKET", "data-engineering-technical-task")
destination_bucket = os.environ["DESTINATION_BUCKET"]
data_grade = os.environ.get("DATA_GRADE", "bronze")

files = [
    "data/outputs/Fund_Details.csv",
    "data/outputs/Fund_Prices.csv"
]

file_types = {
    "Details.csv": "funds",
    "Prices.csv": "prices",
}


def lambda_handler(event, context):
    logger.info("Lambda handler called")
    # better to initialise inside lambda_handler - refreshes for each call, avoids expired sessions
    s3r = boto3.resource("s3")
    destination_bucket_s3r = s3r.Bucket(destination_bucket)
    key_to_copy = event["detail"]["object"]["key"]
    file_key = key_to_copy.rsplit("/", 1)[1]
    file_type = file_key.rsplit("_", 1)[1] # todo remove this temp line of code
    logger.info(f"File to copy - {key_to_copy} - with file key {file_key} of type {file_type}")

    # todo remove temporary line - implement event triggers, there should be a separate trigger per file type
    source_name = file_types[file_type] # source_name would be fixed per lambda function - set in env var
    copy_source = {"Bucket": source_bucket, "Key": key_to_copy}
    current_time = datetime.datetime.now().strftime("%Y/%m/%d")
    dest_key = f"{data_grade}/{source_name}/{current_time}/{file_key}"

    logger.info(f"File to be copied - {copy_source} to {dest_key}")
    destination_bucket_s3r.copy(copy_source, dest_key)
    logger.info(f"Copy finished")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    with open("sample.json") as file:
        dummy_event = json.load(file)
    lambda_handler(dummy_event, {})

    with open("sample2.json") as file:
        dummy_event = json.load(file)
    lambda_handler(dummy_event, {})
    pass
